import numpy as np
from lxml import etree


class SimpleBands:
    """
    SimpleBands class for reading band structure (not resolved for ions and levels).
    Initialize as:
    data = SimpleBands(<path to your vasprun.xml file>)
    This class is not intended to be used separately; all of its features and more
    are implemented in the child BandStructure class.
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
        self.efermi, self.nions, self.nkpts, self.nbands, self.levels, self.subshells, self.lorbit = self._read_info()
        self.atomdict, self.atomnames, self.atomnumbers = self._read_atom_info()
        self.kpoints = self._get_kpoints()
        self.lattice, self.rec_lattice = self._get_dims()
        self.bands = self._get_data()
        self.xaxis = self._get_xaxis()

    def _read_info(self):
        """
        Read information about the system: Fermi energy, number of atoms, 
        number of k-points, number of bands, and list of levels
        """
        efermi = float(self.xml.find("*/*/*[@name='efermi']").text)
        nions = int(self.xml.find("atominfo/atoms").text)
        nkpts = int(len(self.xml.find("kpoints/varray[@name='kpointlist']")))
        nbands = int(self.xml.find("*/*/*[@name='NBANDS']").text)
        levels = np.array([f.text.strip() for f in self.xml.findall("calculation/dos/partial/array/field")][1:])
        if "x2-y2" in levels:
            levels[np.where(levels == "x2-y2")] = "dx2"
        subshells = list(set(s[0] for s in levels) & {"s", "p", "d", "f"})
        if (np.array(list(map(lambda x: len(x), levels))) > 1).any():
            lorbit = 11
        else:
            lorbit = 10
        return efermi, nions, nkpts, nbands, levels, subshells, lorbit
    
    def _read_atom_info(self):
        """
        Read atomic info - atom names and their number - and put them into a dictionary
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

    def _get_dims(self):
        """
        Get matrices of direct and reciprocal lattice
        """
        lattice = [line.text.split() for line
                   in self.xml.findall("structure[@name='initialpos']/crystal/varray[@name='basis']/v")]
        lattice = np.array(lattice).astype(np.float32)
        rec_lattice = [line.text.split() for line
                       in self.xml.findall("structure[@name='initialpos']/crystal/varray[@name='rec_basis']/v")]
        rec_lattice = np.array(rec_lattice).astype(np.float32)
        return lattice, rec_lattice

    def _get_kpoints(self):
        """
        Get an array of kpoints
        """
        kpoints = np.array([kpoint.text.split() for kpoint
                            in self.xml.findall("kpoints/varray[@name='kpointlist']/v")]).astype(np.float32)
        return kpoints

    def _get_data(self):
        """
        Read eigenvals
        """
        band_sets = self.xml.findall("calculation/projected/eigenvalues/array/set/set/set/r")
        data = np.array([r.text.split()[0] for r in band_sets]).astype(np.float32)
        data = data.reshape(-1, self.nbands)
        data = data - self.efermi
        if data.shape[0] == self.nkpts:
            self.spin = False
            return data
        elif data.shape[0] == 2 * self.nkpts:
            self.spin = True
            data = np.stack([data[:self.nkpts, :], data[self.nkpts:, :]])
            return data
        else:
            raise TypeError("Something went wrong. Is the data set spin-polarized or not?")

    def _get_xaxis(self):
        """
        Process the k-points and reciprocal lattice arrays in order to get
        the x-axis for plotting (with accurate distance in BZ)
        """
        segment_length = int(self.xml.find("kpoints/*/*[@name='divisions']").text)
        ticknum = int(self.nkpts / segment_length)
        diffs = np.dot(self.kpoints, self.rec_lattice)
        segments = []
        for i in range(ticknum):
            segment = diffs[i * segment_length:i * segment_length + segment_length]
            dists = segment[1:] - segment[:-1]
            dists = (dists ** 2).sum(1) ** (1 / 2)
            dists = np.insert(dists, 0, 0)
            segments.append(dists)
        segments = np.concatenate(segments)
        axis = segments.cumsum()
        return axis
