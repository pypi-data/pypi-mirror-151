"""
Application for plotting electronic density of states (eDOS) graphs
from VASP calculation output
Frontend based on PyQt6
Backend is handled by VASP-DOS-tools mini-library
Developed by AG
(C) 2022
"""

from sys import exit
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtTest import QTest
from PyQt6.QtCore import pyqtSignal, QObject
from vaspplotsuite.dos.qtdesign import DosAppWindow
import vaspplotsuite.dos.vaspdostools as vdt
from vaspplotsuite.mainwindow.controller import AppController
from os import path as ospath
import numpy as np


class Signal(QObject):
    closed = pyqtSignal()


class DosAppView(QDialog, DosAppWindow):
    """
    Main window object for DosApp
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.signal = Signal()

    def closeEvent(self, e):
        self.signal.closed.emit()


class DosAppController(AppController):

    def __init__(self, view):
        super().__init__(view)
        # Connecting buttons to functions
        self.view.add_total_btn.clicked.connect(self.add_total_dos)
        self.view.export_data_btn.clicked.connect(self.export_dataset)
        self.view.refresh_plot_btn.clicked.connect(self.toggle_plot)

    def load_data(self):
        """
        Load VASP output into a Dos object
        """
        for line in self.view.ax.lines:
            self.view.ax.lines.remove(line)
        self.toggle_plot()
        QTest.qWait(5)
        self.view.load_label.setText("Loading...")
        QTest.qWait(5)
        self.active_path = self.view.load_txt.text()
        try:
            path_to_file = self.view.load_txt.text()
            self.loaded_data = vdt.extract(path_to_file)
            # account for different shorthands for dx2-y2 orbital depending on VASP version
            if "x2-y2" in self.loaded_data.levels:
                self.loaded_data.levels[np.where(self.loaded_data.levels == "x2-y2")] = "dx2"
                self.loaded_data.leveldict["dx2"] = self.loaded_data.leveldict.pop("x2-y2")
            QTest.qWait(5)
            msg = f"<b>{self.loaded_data.name}</b> system was loaded successfully"
            QTest.qWait(5)
            self.view.load_label.setText(msg)
            self.adjust_window()
        except Exception as e:
            self.view.load_label.setText(e.args[0])
            QTest.qWait(2000)
            self.view.load_label.setText("Browse files and load a system")
            self.disable_window()

    def plot_added_data(self, atoms, states, spin, name, color):
        """
        Plot selected resolved data
        """
        sel_dataset = self.loaded_data.select(atoms, states, spin, name)
        self.view.ax.plot(sel_dataset.dos[:, 0], sel_dataset.dos[:, 1],
                          color=color, label=sel_dataset.name,
                          linewidth=4)

    def add_total_dos(self):
        """
        Select total DOS from the Dos object and
        add it to dataset list
        """
        if self.view.spin_box.isEnabled() and self.view.spin_btn_group.checkedButton() is not None:
            spin = self.view.spin_btn_group.checkedButton().text()
        else:
            spin = "both"
        color = self.view.color_comb.currentText()
        if color == "":
            color = "black"
        sel_dataset = self.loaded_data.get_total(spin)
        self.view.ax.plot(sel_dataset.dos[:, 0], sel_dataset.dos[:, 1],
                          color=color, label=sel_dataset.name,
                          linewidth=4)
        self.view.dataset_label.setText("Dataset successfully added")
        self.reset_input()
        self.populate_items()
        self.toggle_plot()
        QTest.qWait(2000)
        self.view.dataset_label.setText("Select atoms and states, and add them to datasets")

    def populate_items(self):
        """
        Refresh content of dataset list
        """
        self.view.datasets_list.clear()
        for line in self.view.ax.lines:
            self.view.datasets_list.addItem(f"{line._label}")

    def remove_dataset(self):
        """
        Remove a dataset from dataset list
        """
        if self.view.ax.lines:
            self.view.ax.lines.remove(self.view.ax.lines[self.view.datasets_list.currentRow()])
            self.populate_items()
        self.toggle_plot()

    def export_dataset(self):
        """
        Save the selected dataset to .csv file
        """
        if len(self.view.ax.lines) > 0:
            to_save = self.view.ax.lines[self.view.datasets_list.currentRow()]
            path_to_save = ospath.dirname(self.active_path)
            np.savetxt(f"{path_to_save}/{to_save._label}.csv", to_save._xy, fmt='%.7f', delimiter=",")

    def toggle_plot(self):
        """
        Refresh plot area
        """
        try:
            if len(self.view.ax.lines) > 0:
                low, high = self.view.ax.get_xlim()
                ymax = max([(line._y[np.where((line._x >= low) & (line._x <= high))]).max() for line in self.view.ax.lines]) * 1.1
                self.view.ax.set_ylim(0, ymax)
                self.view.ax.vlines(0, 0, ymax, colors='gray', linestyles='dashed', linewidth=4)
                self.legend = self.view.ax.legend(prop={'size': 15})
            else:
                if self.view.ax.get_legend():
                    self.view.ax.get_legend().remove()
        except Exception as e:
            self.view.dataset_label.setText(e.args[0])
            QTest.qWait(2000)
            self.view.dataset_label.setText("Add datasets by selecting atoms and states, or plot datasets")
        self.view.canvas.draw()
        self.populate_items()


def main():
    """
    Main function - creates an instance of window (view)
    and applies controller to it
    """
    app = QApplication([])
    view = DosAppView()
    DosAppController(view)
    view.show()
    exit(app.exec())


if __name__ == "__main__":
    main()
