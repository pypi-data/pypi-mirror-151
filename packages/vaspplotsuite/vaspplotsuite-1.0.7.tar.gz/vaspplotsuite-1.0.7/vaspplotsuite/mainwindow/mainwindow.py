from sys import exit
from os import path
from os import name as oname
from PyQt6.QtWidgets import QSizePolicy, QPushButton, QApplication, QDialog, QLabel, QFrame, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QMetaObject, QCoreApplication, QRect, QSize
from PyQt6.QtCore import Qt
from vaspplotsuite.static import font


def buttonstyle(color):
    return f"background-color: {color}; color: white; border-radius: 5px; " \
           f"border: solid; border-width: 1px;"


class MainWindow(object):

    if oname == "nt":
        q = 0.75
    else:
        q = 1
    font1 = QFont(font[0])
    font1.setPointSize(int(36*q))
    font2 = QFont(font[0])
    font2.setPointSize(int(24*q))
    font3 = QFont(font[0])
    font3.setPointSize(int(20*q))
    font4 = QFont(font[0])
    font4.setPointSize(int(12*q))

    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(600, 415)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Window.sizePolicy().hasHeightForWidth())
        Window.setSizePolicy(sizePolicy)
        Window.setMinimumSize(QSize(600, 415))
        Window.setMaximumSize(QSize(600, 415))
        Window.setStyleSheet("")
        self.DosButton = QPushButton(Window)
        self.DosButton.setGeometry(QRect(30, 220, 240, 81))
        self.DosButton.setFont(self.font1)
        self.DosButton.setAutoFillBackground(False)
        self.DosButton.setStyleSheet(buttonstyle("#d90d1f"))
        self.DosButton.setIconSize(QSize(20, 20))
        self.DosButton.setObjectName("DosButton")
        self.BandsButton = QPushButton(Window)
        self.BandsButton.setGeometry(QRect(330, 220, 240, 81))
        self.BandsButton.setFont(self.font1)
        self.BandsButton.setStyleSheet(buttonstyle("#642870"))
        self.BandsButton.setObjectName("BandsButton")
        self.label = QLabel(Window)
        self.label.setGeometry(QRect(25, 20, 550, 30))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFont(self.font2)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QLabel(Window)
        self.label_2.setGeometry(QRect(10, 170, 580, 25))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFont(self.font3)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(Window)
        self.label_3.setGeometry(QRect(100, 340, 400, 30))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setFont(self.font4)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(Window)
        self.label_4.setGeometry(QRect(100, 380, 400, 30))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFont(self.font4)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QLabel(Window)
        self.label_5.setGeometry(QRect(100, 360, 400, 30))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setFont(self.font4)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.line = QFrame(Window)
        self.line.setGeometry(QRect(23, 320, 559, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.widget = QWidget(Window)
        self.widget.setGeometry(QRect(255, 75, 92, 80))
        path_to_img = path.join(path.dirname(__file__), "app-logo.png")
        self.widget.setStyleSheet(f"background-image: url({path_to_img});")
        print(self.widget.styleSheet())
        self.widget.setObjectName("widget")

        self.retranslateUi(Window)
        QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "VASP Plot Suite © AG"))
        self.DosButton.setText(_translate("Window", "eDOS"))
        self.BandsButton.setText(_translate("Window", "Bands"))
        self.label.setText(_translate("Window", "Welcome to VASP Plot Suite!"))
        self.label_2.setText(_translate("Window", "What kind of output data would you like to analyze?"))
        self.label_3.setText(_translate("Window", "© Adam Grzelak"))
        self.label_4.setText(_translate("Window", "For questions and support: contact@adamgrzelak.com"))
        self.label_5.setText(_translate("Window", "www.adamgrzelak.com"))


if __name__ == "__main__":
    app = QApplication([])
    Window = QDialog()
    ui = MainWindow()
    ui.setupUi(Window)
    Window.show()
    exit(app.exec())
