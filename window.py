import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QFileDialog
# from main import *

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

        # Кнопка сохранения кадра
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 41, 41))
        self.pushButton.setMouseTracking(False)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/SaveFrame.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(24, 24))
        self.pushButton.setShortcut("")
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")

        # Текст-бокс для записи времени
        # ToDo 1) - добавить верхнюю границу секунд и минут в 59
        # ToDo 2) - максимальное значени времени по продолжительности видео
        self.line = QtWidgets.QLineEdit(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(60, 10, 121, 41))
        self.line.setText("00:00:00")
        self.line.setInputMask("99:99:99")
        self.line.setObjectName("line")

        # Ползунок для перемотки
        # ToDo 1) - Добавить управление временем
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(190, 20, 601, 21))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        # Поле для вывода картинки
        self.labelImage = QLabel(self.centralwidget)
        self.labelImage.setGeometry(QtCore.QRect(10, 60, 781, 491))
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
        self.pushButton.clicked.connect(self.saveFrame)

    # Функция открывающая файл и отображающая её на экране
    def openImage(self, image):

        # image1 = mainClass.predictImg('res/anton.jpg')
        # image1 = np.array(image1, dtype=np.uint8)
        # plt.imshow(image1)
        # plt.show()
        
        pixmapImage = QPixmap(image)
        pixmapImage = pixmapImage.scaled(
            self.labelImage.width(), self.labelImage.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
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
        self.openImage(self.stockImage)

    # Функция сохранения изображения
    def saveFrame(self):
        # ToDo Потом доделаю
        fileName = str(QFileDialog.getSaveFileName(filter="Image Files (*.png)", directory="image.png")[0])
        ui.labelImage.pixmap().save(fileName)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())