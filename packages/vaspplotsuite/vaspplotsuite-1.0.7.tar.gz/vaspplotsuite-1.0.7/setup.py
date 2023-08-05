from setuptools import setup, find_packages

description = """# VASP Plot Suite
### (C) AG 2022

Vasp Plot Suite is a program for processing and plotting electronic structure data
from VASP calculations output. It has two modules:

a) DosApp: for plotting electronic density of states (eDOS),<br>
b) BandsApp: for plotting electronic band structure.

Instructions for each of module can be found in their respective README files.

This library is available via pip:
<code>pip install vaspplotsuite</code>

After that, you can run it from your command line by typing <code>vaspplot</code>.

### Executables
This program can be compliled into an executable.
I can provide ones for Windows or MacOS upon request.

### This program is still being tested
If you notice any errors or discrepancies, or if you have any practical suggestions,
I would be grateful if you report them.
I have also included sample data for AgF2 system if you want to give it a try.

### Contact
contact@adamgrzelak.com

### Update history
15.05.2022 - updated fonts<br>
13.05.2022 - added command line script<br>
12.05.2022 - publication of version 1.0 Vasp Plot Suite as a whole on PyPI<br>
11.05.2022 - publication of functional BandsApp<br>
10.05.2022 - incorporated <code>matplotlib</code> widget into the main window<br>
05.05.2022 - refactored the application to read <code>vasprun.xml</code><br>
21.03.2022 - incorporated exception handling into vasp-dos-tools and refactored frontend to
display them
"""

setup(
    name="vaspplotsuite",
    packages=find_packages(),
    package_data={"": ["*.png", "*.ttf"]},
    entry_points={"console_scripts": ["vaspplot=vaspplotsuite:run"]},
    version="1.0.7",
    license="MIT",
    description="A program for analysis and plotting of electronic from VASP output data",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/adam-bialy/vasp-plot-suite",
    author="Adam Grzelak",
    author_email="contact@adamgrzelak.com",
    keywords=["VASP", "eDOS", "band structure", "density of states"],
    install_requires=["PyQt6", "matplotlib", "numpy", "scipy", "lxml"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)