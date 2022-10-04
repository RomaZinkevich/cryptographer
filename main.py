from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL.ImageQt import *
from PIL import *
from PyQt5.QtCore import *
from process import in_pic, out_pic


class AuthWindow(QWidget):
    def __init__(self):
        super(AuthWindow, self).__init__()
        self.setWindowTitle('Шифр')
        self.setFixedSize(800, 800)
        self.mainlayout = QVBoxLayout(self)

        self.image = QLabel(self)
        self.image2 = QLabel(self)

        self.tabwidget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabwidget.addTab(self.tab1, "Зашифровать текст")
        self.tabwidget.addTab(self.tab2, "Вытащить текст")

        self.mainlayout.addWidget(self.tabwidget)
        self.tabwidget.tabBarClicked.connect(self.tabbarclicked)

        self.tab1.layout = QVBoxLayout(self)
        self.btn1 = QPushButton("Выбрать изображение")
        self.btn1.clicked.connect(self.choose_image1)
        self.btn2 = QPushButton("Начать шифровку")
        self.btn2.clicked.connect(self.cipher)
        self.line1 = QLineEdit(self)
        self.label1 = QLabel(self)
        self.label1.setText('Введите текст для шифровки')
        self.line2 = QLineEdit(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label2.setText('Введите название конечного файла')

        self.tab1.layout.addWidget(self.label1)
        self.tab1.layout.addWidget(self.line1)
        self.tab1.layout.addWidget(self.label3)
        self.tab1.layout.addWidget(self.btn1)
        self.tab1.layout.addWidget(self.image)
        self.tab1.layout.addWidget(self.label3)
        self.tab1.layout.addWidget(self.label2)
        self.tab1.layout.addWidget(self.line2)
        self.tab1.layout.addWidget(self.btn2)
        self.tab1.layout.addStretch()
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout2 = QVBoxLayout(self)
        self.btn3 = QPushButton("Выбрать изображение")
        self.btn3.clicked.connect(self.choose_image2)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.btn2 = QPushButton("Дешифровка")
        self.btn2.clicked.connect(self.decipher)

        self.tab2.layout2.addWidget(self.label5)
        self.tab2.layout2.addWidget(self.btn3)
        self.tab2.layout2.addWidget(self.image2)
        self.tab2.layout2.addWidget(self.label6)
        self.tab2.layout2.addWidget(self.label4)
        self.tab2.layout2.addWidget(self.btn2)
        self.tab2.layout2.addStretch()
        self.tab2.setLayout(self.tab2.layout2)

    def choose_image1(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

        self.image.setText(fname.split('/')[-1])

    def choose_image2(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

        self.image2.setText(fname.split('/')[-1])

    def cipher(self):
        in_pic(self.line1.text(), self.image.text(),
               self.line2.text() + '.png')

    def decipher(self):
        res = out_pic(self.image2.text())
        self.label4.setText(res)

    def tabbarclicked(self, index):
        if index == 0:
            self.setWindowTitle('Шифр')
        else:
            self.setWindowTitle('Дешифр')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = AuthWindow()
    wnd.show()
    sys.exit(app.exec())
