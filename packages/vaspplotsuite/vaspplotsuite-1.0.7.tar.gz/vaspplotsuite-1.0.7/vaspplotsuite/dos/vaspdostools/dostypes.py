import numpy as np
from scipy.integrate import trapz
from scipy.interpolate import interp1d
from lxml import etree


class RawDos:
    """
    Main DOS object, into which data is loaded from a directory and
    process to obtain: \n
    - array of total DOS \n
    - array of atomic DOS \n
    - spin-polarization (yes/no) and resolution (subshell/orbital) \n
    - Fermi energy \n
    Initialize as:
    data = RawDos(<path to vasprun.xml file>)
    In order to get atom and/or orbital resolved DOS, use "select" method as:
    selected = data([atoms], [states], spin(, name))
    """

    def __init__(self, path_to_file):
        """
        Constructor
        :param str path_to_file: address of vasprun.xml file
        """

        try:
            self.xml = etree.parse(path_to_file)
        except OSError:
            raise FileNotFoundError("vasprun.xml not present")

        self.name = self.xml.find("incar/i[@name='SYSTEM']").text.strip()

        # get atomic info
        self.atomdict, self.atomnames, self.atomnumbers = self._atom_info()

        # get electronic DOS info
        self.spin = None
        self.nedos, self.fermi = self._dos_info()
        self.totaldos, self.atomicdos, self.e = self._load_dos()
        self.e = self.e - self.fermi

        # get names of levels
        self.levels = self._load_levels()
        # check if subshell- or orbital-resolved
        if "px" in self.levels:
            self.lorbit = 11
        else:
            self.lorbit = 10

        # list subshells
        self.subshells = list(set(s[0] for s in self.levels) & {"s", "p", "d", "f"})

        # creating dictionaries of levels and their indices
        self.leveldict = {}
        for i in range(len(self.levels)):
            if self.spin:
                self.leveldict[self.levels[i]] = [2 * i, 2 * i + 1]
                self.spindict = {"up": [0], "down": [1], "both": [0, 1]}
            else:
                self.leveldict[self.levels[i]] = [i]
                self.spindict = None
        del self.xml

    def __str__(self):
        return f"DOS for {self.name} system"

    def get_total(self, spin="both"):
        """
        returns total DOS as array of energy and DOS \n
        :return: Dos
        """
        # selects the appropriate spin column
        if self.spin:
            if spin == "up":
                total = self.totaldos[:, 0]
            elif spin == "down":
                total = self.totaldos[:, 1]
            else:
                total = self.totaldos[:, [0, 1]].sum(1)
            name = f"{self.name}-total-{spin}"
        else:
            total = self.totaldos[:, 0]
            name = f"{self.name}-total"
        dos = np.column_stack([self.e, total])
        return Dos(dos, name)

    def integrate_total(self, lower, upper):
        """
        returns integrated total DOS \n
        somewhat reduntant, but the integrated values come from VASP,
        so we are keeping them \n
        :param float lower: lower bound
        :param float upper: upper bound
        :return: float
        """
        total = self.totaldos[:, -(1 + int(self.spin)):]
        if total.shape[-1] > 1:
            total = total.sum(1)
        inter = interp1d(self.e.flatten(), total.flatten())
        p1 = inter(lower)
        p2 = inter(upper)
        return p2 - p1

    def _atom_info(self):
        """
        read atomic info, used in constructor
        """

        atom_names = [a.text.strip() for a in self.xml.findall("atominfo/array[@name='atomtypes']/set/rc/c")][1::5]
        atom_numbers = [a.text.strip() for a in self.xml.findall("atominfo/array[@name='atomtypes']/set/rc/c")][0::5]
        atom_numbers = [int(n) for n in atom_numbers]
        atom_dict = {}
        cnt = 0
        for atom, number in zip(atom_names, atom_numbers):
            atom_dict[atom] = list(range(cnt, cnt + number))
            cnt = cnt + number
        return atom_dict, atom_names, atom_numbers

    def _dos_info(self):
        """
        read preliminary DOS info
        """
        nedos = int(self.xml.find("*/*/*[@name='NEDOS']").text)
        fermi = float(self.xml.find("*/*/*[@name='efermi']").text.strip())
        return nedos, fermi

    def _load_dos(self):
        """
        read actual DOS, used in constructor
        """
        totaldos = self.xml.findall("calculation/dos/total/array/set/set")
        if len(totaldos) == 2:
            self.spin = True
            totaldosup = self.xml.find("calculation/dos/total/array/set/set[@comment='spin 1']")
            totaldosup = np.array([i.text.split() for i in totaldosup]).astype(np.float32)
            totaldosdown = self.xml.find("calculation/dos/total/array/set/set[@comment='spin 2']")
            totaldosdown = np.array([i.text.split() for i in totaldosdown]).astype(np.float32)
            total_dos = np.column_stack([totaldosup[:, 1], totaldosdown[:, 1], totaldosup[:, 2], totaldosdown[:, 2]])
            e = totaldosup[:, 0]
            atomic = self.xml.findall("calculation/dos/partial/array/set/set/set")
            a_up = [[line.text.split() for line in atom] for atom in atomic[::2]]
            a_down = [[line.text.split() for line in atom] for atom in atomic[1::2]]
            a_up = np.array(a_up).astype(np.float32)
            a_down = np.array(a_down).astype(np.float32)
            zipped = list(
                zip([a_up[:, :, i] for i in range(a_up.shape[-1])], [a_down[:, :, i] for i in range(a_down.shape[-1])]))
            zipped = [i for x in zipped for i in x]
            atomic_dos = np.stack(zipped, axis=-1)[:, :, 2:]
        else:
            self.spin = False
            totaldos = np.array([i.text.split() for i in totaldos[0]]).astype(np.float32)
            total_dos = totaldos[:, 1:]
            e = totaldos[:, 0]
            atomic = self.xml.findall("calculation/dos/partial/array/set/set/set")
            a = [[line.text.split() for line in atom] for atom in atomic]
            atomic_dos = np.array(a).astype(np.float32)[:,:,1:]
        return total_dos, atomic_dos, e

    def _load_levels(self):
        """
        read list of levels, used in constructor
        """
        levels = [f.text.strip() for f in self.xml.findall("calculation/dos/partial/array/field")][1:]
        return np.array(levels)

    def select(self, atoms, states, spin="both", name=None):
        """
        selects atoms and/or states from total DOS \n
        :param iterable atoms: 1D array of selected atoms, by name or by number, matching atoms in raw dos
        :param iterable states: 1D array of selected states, matching levels in raw dos
        :param str spin: "up", "down" or "both"
        :param str name: name for the dataset
        :return: Dos object instance
        """

        selected = self.atomicdos
        if not type(atoms) in [np.ndarray, list]:
            raise TypeError("Invalid input type for atoms selection. List or 1D numpy array is acceptable.")
        if not type(states) in [np.ndarray, list]:
            raise TypeError("Invalid input type for states selection. List or 1D numpy array is acceptable.")
        if type(atoms) == np.ndarray:
            if len(atoms.shape) > 1:
                raise TypeError("Array of atoms has to be 1-dimensional.")
        if type(states) == np.ndarray:
            if len(states.shape) > 1:
                raise TypeError("Array of states has to be 1-dimensional.")
        atoms = np.array(atoms)
        states = np.array(states)

        if not (all(lev in self.levels for lev in states) or all(lev in self.subshells for lev in states)):
            raise ValueError("Some of the selected states are not present in the dataset.")

        if spin not in ["up", "down", "both"]:
            raise ValueError("Incorrect spin value selected. \"up\", \"down\" or \"both\" is accepted.")

        if name is None:
            name = f"[{' '.join(atoms.astype(str))}] - [{''.join(states.astype(str))}] - [{spin}]"

        # selecting atoms
        at_ind = []
        if np.issubdtype(atoms.dtype, str):
            if not all(at in self.atomdict.keys() for at in atoms):
                raise ValueError("Some of the selected atoms are not present in the dataset.")
            else:
                for atom in atoms:
                    at_ind += self.atomdict[atom]
        else:
            atoms = atoms - 1
            if not all(at in list(range(sum(self.atomnumbers))) for at in atoms):
                raise ValueError("Some of the selected atoms are not present in the dataset.")
            at_ind = [i for i in atoms]
        selected = selected[at_ind, :, :]

        # selecting states
        if (np.vectorize(len)(states) == 1).all():
            states = np.concatenate([np.argwhere(np.char.find(self.levels, c) != -1) for c in states]).flatten()
        if np.issubdtype(states.dtype, np.integer):
            states = self.levels[states]
        st_ind = []
        for s in states:
            st_ind += self.leveldict[s]
        if self.spin:
            spin_ind = self.spindict[spin]
            final_st_ind = []
            for spin in spin_ind:
                final_st_ind += st_ind[spin::2]
            selected = selected[:, :, final_st_ind]
        else:
            self.spin = None
            selected = selected[:, :, st_ind]

        # final processing
        selected = selected.sum(0).sum(1)
        selected = np.column_stack([self.e, selected])
        return Dos(selected, name)


class Dos:
    """
    Class for storing general Dos objects, selected from RawDos
    or loaded from a file.
    Data can be integrated using "integrate" method.
    The data can then be plotted using other scripts.
    """

    def __init__(self, dos, name):
        """
        :param np.ndarray dos: Array with E and eDOS values
        :param name: name for the dataset
        """
        self.dos = dos
        self.name = name

    def save(self, path):
        """
        saves eDOS to .csv file
        """
        np.savetxt(f"{path}/{self.name}.csv", self.dos, fmt='%.7f', delimiter=",")

    def integrate(self, lower, upper):
        """
        Integrates DOS in a given energy range
        :param float lower: lower bound for integration
        :param float upper: upper bound for integration
        :return: float
        """
        inter = interp1d(self.dos[:, 0], self.dos[:, 1])
        p1 = np.array([lower, inter(lower)]).reshape(1, 2)
        p2 = np.array([upper, inter(upper)]).reshape(1, 2)
        new = np.concatenate([self.dos, p1, p2])
        new = new[new[:, 0].argsort(), :]
        int_at_lower = trapz(new[new[:, 0] <= lower][:, 1], x=new[new[:, 0] <= lower][:, 0])
        int_at_upper = trapz(new[new[:, 0] <= upper][:, 1], x=new[new[:, 0] <= upper][:, 0])
        return int_at_upper - int_at_lower
