import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("金刚线扫描器")
        self.setGeometry(100, 100, 1000, 707)

        self.label = QLabel("选择图片文件", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 1px solid #aaa;")
        self.label.setFixedSize(400, 300)

        self.select_button = QPushButton("选择文件", self)
        self.select_button.clicked.connect(self.select_file)

        self.threshold_input = QLineEdit(self)
        self.threshold_input.setPlaceholderText("输入阈值(可选)")

        self.execute_button = QPushButton("执行", self)
        self.execute_button.clicked.connect(self.execute_python_file)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        self.real_value_input = QLineEdit(self)
        self.real_value_input.setPlaceholderText("输入真实值 (如需矫正，选择图片后在此输入真实值,在运行矫正后在图中画出真实值所在直线，按任意键退出)")

        self.plot_button = QPushButton("矫正", self)
        self.plot_button.clicked.connect(self.run_get_plot_data)

        top_right_layout = QHBoxLayout()
        top_right_layout.addWidget(self.real_value_input)
        top_right_layout.addWidget(self.plot_button)
        top_right_layout.setAlignment(Qt.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_right_layout)
        main_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.threshold_input, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.execute_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.output_text)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

        self.file_path = None
        self.process = None

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.python_file = os.path.join(self.script_dir, "main.py")
        self.plot_file = os.path.join(self.script_dir, "test_file", "get_plot_data.py")

        self.threshold_input.setFocus()

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
            threshold = self.threshold_input.text()
            if not threshold:
                threshold = "49"

            self.process = QProcess(self)
            self.process.setProgram("python3")
            self.process.setArguments([self.python_file, self.file_path, threshold])

            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.finished.connect(self.process_finished)

            self.process.start()

            self.output_text.clear()
        else:
            self.label.setText("没有选择任何文件，请选择一个图片文件")
            self.output_text.setPlainText("没有选择任何文件，请选择一个图片文件")
            print("没有选择任何文件，请选择一个图片文件")

    def run_get_plot_data(self):
        if self.file_path:
            real_value = self.real_value_input.text()
            if not real_value:
                self.output_text.setPlainText("请输入真实值")
                return

            # 初始化 QProcess
            self.process = QProcess(self)
            self.process.setProgram("python3")
            self.process.setArguments([self.plot_file, self.file_path, real_value])

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
