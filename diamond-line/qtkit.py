import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("金刚线扫描器")
        self.setGeometry(100, 100, 1000, 600)

        self.label = QLabel("选择图片文件", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 1px solid #aaa;")
        self.label.setFixedSize(400, 300)

        self.select_button = QPushButton("选择文件", self)
        self.select_button.clicked.connect(self.select_file)

        self.execute_button = QPushButton("执行", self)
        self.execute_button.clicked.connect(self.execute_python_file)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.select_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.execute_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.output_text)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.file_path = None
        self.process = None

    def select_file(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
                                                   options=options)
        if file_path:
            self.file_path = file_path
            self.label.setPixmap(QPixmap(self.file_path).scaled(self.label.size(), Qt.KeepAspectRatio))
        else:
            self.label.setText("No file selected")

    def execute_python_file(self):
        if self.file_path:
            # 在这里添加要执行的 Python 文件路径
            python_file = "main.py"

            # 初始化 QProcess
            self.process = QProcess(self)
            self.process.setProgram("python3")
            self.process.setArguments([python_file, self.file_path])

            # 连接信号到槽
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.finished.connect(self.process_finished)

            # 启动进程
            self.process.start()

            self.output_text.clear()
        else:
            self.label.setText("没有选择任何文件，请选择一个图片文件")
            self.output_text.setPlainText("没有选择任何文件，请选择一个图片文件")
            print("没有选择任何文件，请选择一个图片文件")

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.output_text.append(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.output_text.append(stderr)

    def process_finished(self):
        self.process = None
        print("执行完毕")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())