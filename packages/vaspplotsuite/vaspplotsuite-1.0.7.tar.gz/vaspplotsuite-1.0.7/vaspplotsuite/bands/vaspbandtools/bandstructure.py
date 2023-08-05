import numpy as np
from vaspplotsuite.bands.vaspbandtools.simplebands import SimpleBands


class BandStructure(SimpleBands):
    """
    BandStructure for reading orbital- and ion-resolved data.
    Inherits from SimpleBands and adds data selection funcionality.
    Initialize as:
    data = BandStructure(<path to your vasprun.xml file>)
    If the data is spin-polarized, the array of projected bands is of the shape:
    (2 (up and down spin), number of kpoints, number of bands, number of atoms/ions, number of levels (subshells or orbitals))
    If it is not spin-polarized, the shape is:
    (number of kpoints, number of bands, number of atoms/ions, number of levels (subshells or orbitals))
    """

    def __init__(self, path, load_all=True):
        """
        Constructor
        :param str path_to_file: address of vasprun.xml file
        """
        super().__init__(path)
        self.leveldict, self.spindict = self._get_level_dict()
        if load_all:
            self._get_proj_bands_verbose()

    def select(self, atoms, states, spin="both", name=None):
        """
        selects atoms and/or states for band projection \n
        :param iterable atoms: 1D array of selected atoms, by name or by number, matching atoms in simplebands
        :param iterable states: 1D array of selected states, matching levels in simplebands
        :param str spin: "up", "down" or "both"
        :param str name: name for the dataset
        :return: ProjectedBands object, where data is of the shape (number of kpoints, number of bands)
        """

        selected = self.proj_bands
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

        # selecting states
        if (np.vectorize(len)(states) == 1).all():
            states = np.concatenate([np.argwhere(np.char.find(self.levels, c) != -1) for c in states]).flatten()
        if np.issubdtype(states.dtype, np.integer):
            states = self.levels[states]
        st_ind = []
        for s in states:
            st_ind += self.leveldict[s]

        # selecting spin and finalizing
        if self.spin:
            spin_ind = self.spindict[spin]
            selected = selected[:,:,:,at_ind,:][:,:,:,:,st_ind][spin_ind,:,:,:,:]
            selected = selected.sum(0).sum(-1).sum(-1)
        else:
            self.spin = None
            selected = selected[:,:,at_ind,:][:,:,:,st_ind]
            selected = selected.sum(-1).sum(-1)

        return ProjectedBands(selected, name)
        
    def _get_level_dict(self):
        """
        Create dictionary of levels and spins for selection
        """
        leveldict = {}
        for i in range(len(self.levels)):
            leveldict[self.levels[i]] = [i]
            if self.spin:
                spindict = {"up": [0], "down": [1], "both": [0, 1]}
            else:
                spindict = None
        return leveldict, spindict

    def _get_proj_bands(self):
        """
        Read orbital- and ion-resolved data in the background.
        """
        data = list(self._datagen())
        self._set_data(data)
    
    def _get_proj_bands_verbose(self):
        """
        Read orbital- and ion-resolved data verbosely.
        """
        data_per_point = self.nbands * 2 * self.nions
        gen = self._datagen()
        data = []
        i = 0
        for r in gen:
            i += 1
            if i % data_per_point == 0:
                print(f"Processed {i // data_per_point}/{self.nkpts} k-points...", end="\r")
            data.append(r)
        print()
        print("Finishing up...")
        self._set_data(data)
        print("Done.")

    def _datagen(self):
        """
        Create generator object with data.
        """
        data = self.xml.findall("calculation/projected/array/set/set/set/set/r")
        for r in data:
            yield np.array(r.text.split()).astype(np.float32)

    def _set_data(self, data):
        """
        Assign data created with a verbose progress-tracking loop.
        """
        proj = np.vstack(data)
        if self.spin:
            proj = proj.reshape(2, self.nkpts, self.nbands, self.nions, -1)
        else:
            proj = proj.reshape(1, self.nkpts, self.nbands, self.nions, -1)
        self.proj_bands = proj


class ProjectedBands:
    """
    Object for storing projected bands after selecting them.
    Consists simply of the data array and of the designated name.
    """
    def __init__(self, data, name):
        self.data = data
        self.name = name
