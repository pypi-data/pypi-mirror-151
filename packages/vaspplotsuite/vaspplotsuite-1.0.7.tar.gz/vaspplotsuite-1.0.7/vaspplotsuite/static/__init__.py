from PyQt6.QtGui import QFontDatabase, QGuiApplication
from os import path

a = QGuiApplication([])
font_path = path.dirname(__file__)
font_path = path.join(font_path, "Montserrat-Regular.ttf")
font = QFontDatabase.addApplicationFont(font_path)
font = QFontDatabase.applicationFontFamilies(font)
