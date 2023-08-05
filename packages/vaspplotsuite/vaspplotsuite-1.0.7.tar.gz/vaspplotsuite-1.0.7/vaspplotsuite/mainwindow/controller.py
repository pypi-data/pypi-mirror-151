from functools import partial
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtTest import QTest
from os import name as osname
from os import path as ospath
import numpy as np


class AppController:
    """
    Generic controller class for use in DosApp and BandsApp modules.
    """

    def __init__(self, view):
        self.view = view
        self.disable_window()
        osys = osname
        if osys == "posix":
            self.home_path = "/Users"
        else:
            self.home_path = "C:\\"
        # Connecting buttons to functions
        self.view.atom_tabs.currentChanged.connect(self.clear_atom_tabs)
        self.view.states_tabs.currentChanged.connect(self.clear_states_tabs)
        self.view.browse_btn.clicked.connect(partial(self.browse, self.view))
        self.view.load_btn.clicked.connect(self.load_data)
        self.view.add_data_btn.clicked.connect(self.add_dataset)
        self.view.remove_data_btn.clicked.connect(self.remove_dataset)

    def browse(self, view):
        """
        Browse directories
        """
        chosen_file = QFileDialog.getOpenFileName(view, "Choose file:", self.home_path, "(vasprun.xml)")[0]
        self.view.load_txt.setText(chosen_file)
        new_home_path = ospath.dirname(ospath.dirname(chosen_file))
        self.home_path = new_home_path

    def load_data(self):
        pass

    def add_dataset(self):
        """
        Generic method for loading data based on selection from the window.
        Details that differ between eDOS and bands are defined in plot_added_data within
        both controller subclasses
        """
        if self.view.atom_tabs.currentIndex() == 0:
            atoms = [self.view.atom_comb.currentText()]
        else:
            atoms = self.view.atom_text.text().split()
            try:
                atoms = np.array(atoms).astype(int)
            except ValueError:
                atoms = np.array(atoms)
        states = []
        if self.view.states_tabs.currentIndex() == 0:
            for box in self.view.subshell_box_list:
                if box.isChecked():
                    states.append(box.text())
        else:
            for box in self.view.orbital_box_list:
                if box.isChecked():
                    states.append(box.text())
        states = np.array(states)
        if len(states) > 0:
            states[np.where(states == "dx2-y2")] = "dx2"
        if self.view.spin_box.isEnabled() and self.view.spin_btn_group.checkedButton() is not None:
            spin = self.view.spin_btn_group.checkedButton().text()
        else:
            spin = "both"
        color = self.view.color_comb.currentText()
        name = self.view.name_text.text()
        condition = (len(states) > 0) and (len(atoms) > 0) and \
                    (not np.isin("", atoms)) and (name != "") and (color != "")
        if condition:
            try:
                self.plot_added_data(atoms, states, spin, name, color)
                self.view.dataset_label.setText("Dataset successfully added")
                self.reset_input()
            except Exception as e:
                self.view.dataset_label.setText(e.args[0])
        else:
            self.view.dataset_label.setText("Make sure you made a valid (non-null) selection")
        self.toggle_plot()
        self.populate_items()
        QTest.qWait(2000)
        self.view.dataset_label.setText("Select atoms and states, and add them to datasets")

    def plot_added_data(self, *args):
        pass

    def remove_dataset(self):
        pass

    def toggle_plot(self):
        pass

    def populate_items(self):
        pass

    def clear_atom_tabs(self):
        """
        Reset input in atom tabs
        """
        self.view.atom_comb.setCurrentIndex(0)
        self.view.atom_text.clear()

    def clear_states_tabs(self):
        """
        Reset input in states tabs
        """
        for box in self.view.subshell_box_list:
            box.setChecked(False)
        for box in self.view.orbital_box_list:
            box.setChecked(False)

    def reset_input(self):
        """
        Reset selection in the window
        """
        self.clear_atom_tabs()
        self.clear_states_tabs()
        self.view.name_text.clear()
        self.view.color_comb.setCurrentIndex(0)
        self.view.spin_btn_group.setExclusive(False)
        for btn in self.view.spin_btn_list:
            btn.setChecked(False)
        self.view.spin_btn_group.setExclusive(True)

    def disable_window(self):
        """
        Disable functions in the window
        """
        self.view.atom_sel_box.setDisabled(True)
        self.reset_input()
        self.view.states_box.setDisabled(True)
        self.view.spin_box.setDisabled(True)
        for btn in self.view.dataset_btns:
            btn.setDisabled(True)
        self.view.datasets_list.clear()
        self.view.datasets_list.setDisabled(True)
        for box in self.view.subshell_box_list:
            box.setDisabled(True)
        for box in self.view.orbital_box_list:
            box.setDisabled(True)
        self.view.properties_box.setDisabled(True)

    def adjust_window(self):
        """
        Selectively enabling functionalities in the window
        based on the loaded VASP data
        """
        self.disable_window()
        # enable and load atoms
        self.view.atom_sel_box.setEnabled(True)
        self.view.atom_comb.clear()
        self.view.atom_comb.addItems([""] + self.loaded_data.atomnames)
        # enable spin if spin-polarized
        if self.loaded_data.spin:
            self.view.spin_box.setEnabled(True)
        else:
            self.view.spin_box.setDisabled(True)
        # enable states and subshells
        self.view.states_box.setEnabled(True)
        self.view.subshell_tab.setEnabled(True)
        for level in self.loaded_data.subshells:
            self.view.subshell_box_dict[level].setEnabled(True)
        # enable orbitals if lorbit is 11
        if self.loaded_data.lorbit == 10:
            self.view.orbital_tab.setDisabled(True)
        else:
            self.view.orbital_tab.setEnabled(True)
            for level in self.loaded_data.subshells:
                for box in self.view.orbital_box_dict[level]:
                    box.setEnabled(True)
        # enable processing buttons
        for btn in self.view.dataset_btns:
            btn.setEnabled(True)
        self.view.datasets_list.setEnabled(True)
        self.view.datasets_list.clear()
        self.view.properties_box.setEnabled(True)
