"""
Vasp Plot Suite
main script
"""


from PyQt6.QtWidgets import QApplication, QDialog
from sys import exit
from vaspplotsuite.mainwindow.mainwindow import MainWindow, buttonstyle
from vaspplotsuite.dos import DosAppView, DosAppController
from vaspplotsuite.bands import BandsAppView, BandsAppController


color1a = "#d90d1f"
color1d = "#D98088"
color2a = "#642870"
color2d = "#6C5870"


class MainView(QDialog, MainWindow):
    """
    Main window object. Details of the functioning of each of the modules
    can be found in their respective files and folders (dos and bands).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.DosButton.clicked.connect(self.open_dos_window)
        self.BandsButton.clicked.connect(self.open_bands_window)

    def open_dos_window(self):
        """
        Create and open new DosApp window
        """
        self.dos_window = DosAppView()
        DosAppController(self.dos_window)
        self.DosButton.setDisabled(True)
        self.DosButton.setStyleSheet(buttonstyle(color1d))
        self.dos_window.signal.closed.connect(self.close_dos_window)
        self.dos_window.show()

    def close_dos_window(self):
        self.DosButton.setEnabled(True)
        self.DosButton.setStyleSheet(buttonstyle(color1a))

    def open_bands_window(self):
        """
        Create and open new BandsApp window
        """
        self.bands_window = BandsAppView()
        BandsAppController(self.bands_window)
        self.BandsButton.setDisabled(True)
        self.BandsButton.setStyleSheet(buttonstyle(color2d))
        self.bands_window.signal.closed.connect(self.close_bands_window)
        self.bands_window.show()

    def close_bands_window(self):
        self.BandsButton.setEnabled(True)
        self.BandsButton.setStyleSheet(buttonstyle(color2a))


def main():
    """
    Main function - creates an instance of window (view)
    and applies controller to it
    """
    app = QApplication([])
    view = MainView()
    view.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
