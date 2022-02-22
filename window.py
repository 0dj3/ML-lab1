import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from main import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        height = 597
        width = 806
        # Главное окно
        MainWindow.setObjectName("MainWindow")
        MainWindow.setAnimated(True)
        MainWindow.setFixedSize(width, height)

        # Контент
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Поле для вывода картинки
        self.labelImage = QLabel(self.centralwidget)
        self.labelImage.setGeometry(QtCore.QRect(10, 10, 781, 550))
        self.labelImage.setStyleSheet(
            "QLabel {background-color: white; border: 1px solid "
            "gray;}")
        self.labelImage.setObjectName("graphicsView")
        self.labelImage.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.stockImage = "res/empty.png"
        self.openImage(self.stockImage)

        # Инициализация меню-бара
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 806, 21))
        self.menubar.setObjectName("menubar")

        # Меню "File"
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        # Меню "Help"
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        # Какой-то статус-бар
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # File -> Open
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        # File -> Close
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        # File -> Save frame
        self.actionSave_frame = QtWidgets.QAction(MainWindow)
        self.actionSave_frame.setObjectName("actionSave_frame")

        # File -> Quit
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        # Help -> About
        # ToDo 1) - Создать дочернее окно и расписать "О программе"
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        # Привязка объектов к меню
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionSave_frame)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # Устанавка текста и заголовков виджетов
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionSave_frame.setText(_translate("MainWindow", "Save frame"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

        # Закрывает программу
        self.actionQuit.triggered.connect(QCoreApplication.instance().quit)
        # Открывает изображение и отображает на экране
        self.actionOpen.triggered.connect(self.openFile)
        # Очистка поля с изображением
        self.actionClose.triggered.connect(self.closeImage)
        # Сохранение изображения
        self.actionSave_frame.triggered.connect(self.saveFrame)
        # Открыть окно о программе
        self.actionAbout.triggered.connect(self.openDialog)

    def paintEvent(self, event):
        super().paintEvent(event)
        qp = QPainter(self)
        br = QBrush(QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.drawRect(QRect(self.begin, self.end))

    # Функция открывающая файл и отображающая её на экране
    def openImage(self, image):

        boxes, classes, scores = mainClass.predictImg(image)        
        
        pixmapImage = QPixmap(image)
        # pixmapImage = pixmapImage.scaled(
        #     self.labelImage.width(), self.labelImage.height(),
        #     Qt.KeepAspectRatio,
        #     Qt.SmoothTransformation
        # )
        painter = QPainter(pixmapImage)
        
        for box, _cls, score in zip(boxes, classes, scores):
            painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
            text = "{}: {:.2f}".format(_cls, score)
            x1, y1, x2, y2 = box
            w, h = x2 - x1, y2 - y1
            rect = QRect(int(x1), int(y1), int(w), int(h))
            painter.drawRect(rect)
            
            painter.setPen(QPen(Qt.blue,2,Qt.SolidLine))
            pos = QPoint(int(x1), int(y1))
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(pos, text)

        painter.end()

        self.labelImage.setPixmap(pixmapImage)
        

    # Функция, которая получает название файла (Формат png, jpg и bmp)
    # ToDo 1) - Исправить баг, который крашит программу при нажатии на кнопку "Отмена"
    def openFile(self):
        fileName = QFileDialog.getOpenFileName(filter="Image Files (*.png *.jpg *.bmp)")[0]
        if len(fileName) > 0:
            self.openImage(fileName)
        else:
            print("eee na, ti 4e delaesh na?")

    # Функция вызывающая стоковое изображение "Empty"
    def closeImage(self):
        pixmapImage = QPixmap('res/empty.png')
        self.labelImage.setPixmap(pixmapImage)

    # Функция сохранения изображения
    def saveFrame(self):
        fileName = str(QFileDialog.getSaveFileName(filter="Image Files (*.png)", directory="image.png")[0])
        ui.labelImage.pixmap().save(fileName)

    def openDialog(self):
        self.helpwin = HelpWindow()
        self.helpwin.show()

class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 300)
        #self.setGeometry(100, 60, 1000, 800)
        self.setWindowTitle("About")

        l1 = QLabel(self)
        l2 = QLabel(self)
        l3 = QLabel(self)
        l4 = QLabel(self)
        l5 = QLabel(self)

        l1.move(140, 50)
        l1.setText("Recognizes objects using RetinaNet")
        l1.setAlignment(Qt.AlignCenter)
        l1.adjustSize()

        l2.setText("Developers:")
        l2.setAlignment(Qt.AlignCenter)
        l2.move(175, 75)

        l3.setText("Egorov Aital")
        l3.setAlignment(Qt.AlignCenter)
        l3.move(175, 100)

        l4.setText("Innokentiev Vladimir")
        l4.setAlignment(Qt.AlignCenter)
        l4.move(175, 125)

        l5.setText("Lukovtsev Alexey")
        l5.setAlignment(Qt.AlignCenter)
        l5.move(175, 150)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

