from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

from main import find_em_all


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Poszukiwacz ZAiKS-u'
        self.folder_path = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()
        self.label = QLabel("")

        self.button1 = QPushButton('Wybierz folder', self)
        self.button1.clicked.connect(self.select_folder)

        self.button2 = QPushButton('Start', self)
        self.button2.clicked.connect(find_em_all)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Wybierz folder')
        self.label.setText(f"Wybrany folder: {self.folder_path}")


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    ex.show()
    app.exec_()

