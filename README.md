# rivers2stratigraphy

[![Build Status](https://travis-ci.org/sededu/rivers2stratigraphy.svg?branch=master)](https://travis-ci.org/sededu/rivers2stratigraphy) 
[![Build status](https://ci.appveyor.com/api/projects/status/9twedak77iixanb7/branch/master?svg=true)](https://ci.appveyor.com/project/amoodie/rivers2stratigraphy/branch/master)

[![GitHub version](https://badge.fury.io/gh/sededu%2Frivers2stratigraphy.svg)](https://badge.fury.io/gh/sededu%2Frivers2stratigraphy)
[![Anaconda-Server Badge](https://anaconda.org/sededu/rivers2stratigraphy/badges/version.svg)](https://anaconda.org/sededu/rivers2stratigraphy)
[![PyPI version](https://badge.fury.io/py/rivers2stratigraphy.svg)](https://badge.fury.io/py/rivers2stratigraphy)
[![Anaconda-Server Badge](https://anaconda.org/sededu/rivers2stratigraphy/badges/platforms.svg)](https://anaconda.org/sededu/rivers2stratigraphy)

Explore how a river becomes stratigraphy

<img src="https://github.com/sededu/rivers2stratigraphy/blob/master/private/rivers2stratigraphy_demo.gif" alt="demo_gif">


This readme file provides an overview of the installation and setup process, as well as a brief description of the module worksheets available.

This repository is also linked into the [SedEdu suite of education modules](https://github.com/sededu/sededu), and can be accessed there as well.



## About the model
Stratigraphic model based on LAB models, i.e., geometric channel body is deposited in "matrix" of floodplain mud. 
The channel is always fixed to the basin surface and subsidence is only control on vertical stratigraphy.
Horizontal stratigraphy is set by 1) lateral migration (drawn from a pdf) and dampened for realism, and 2) avulsion that is set to a fixed value.



## Installing and running the module

This module depends on Python 3, `tkinter`, and the Python packages `numpy`, `scipy`, `matplotlib`, and `shapely`. 

### Installing Python 3

If you are new to Python, it is recommended that you install Anaconda, which is an open source distribution of Python which includes many basic scientific libraries, some of which are used in the module. 
Anaconda can be downloaded at https://www.anaconda.com/download/ for Windows, macOS, and Linux. 
If you do not have storage space on your machine for Anaconda or wish to install a smaller version of Python for another reason, see below on options for Miniconda or vanilla Python.

1. Visit the website for Anaconda https://www.anaconda.com/download/ and select the installer for your operating system.
__Be sure to select the Python 3.x installation.__
2. Start the installer.
3. If prompted, select to "install just for me", unless you know what you are doing.
4. When prompted to add Anaconda to the path during installation, select _yes_ if you __know__ you do not have any other Python installed on your computer; otherwise select _no_.

See below for detailed instructions on installing `rivers2stratigraphy` for your operating system.


### Installing the module

If you installed Anaconda Python or Miniconda, you can follow the instructions below for your operating system. 
Otherwise see the instructions for PyPi installation below.

__Please__ [open an issue](https://github.com/sededu/rivers2stratigraphy/issues) if you encounter any troubles installing or any error messages along the way! 
Please include 1) operating system, 2) installation method, and 3) copy-paste the error.


#### Windows users

1. Open your "start menu" and search for the "Anaconda prompt"; start this application.

2. Install with the module type the following command and hit "enter":
```
conda install -c sededu rivers2stratigraphy
```
If asked to proceed, type `Y` and press "enter" to continue installation. 
3. This process may take a few minutes as the necessary source code is downloaded.
If the installation succeeds, proceed below to the "Run the module" section.

__Note on permissions:__ you may need to run as administrator on Windows.


#### Mac OSX and Linux users

__Linux users:__ you will need to also install `tkinter` before trying to install the module below package through `conda` or `pip3`.
On Ubuntu this is done with `sudo apt install python3-tk`.
<!-- Windows and Mac distributions should come with `python3-tk` installed. -->

1. Install the module by opening a terminal and typing the following command.
```
conda install -c sededu rivers2stratigraphy
```
If asked to proceed, type `Y` and press enter to continue installation.

2. This process may take a few minutes as the necessary source code is downloaded.
If the installation succeeds, proceed below to the "Run the module" section.

__Note on permissions:__ you may need to use `sudo` on OSX and Linux.


#### Advanced user installations
To install with `pip` from Pypi use (not recommended for entry-level users):
```
pip3 install pyqt rivers2stratigraphy
```

See below instructions for downloading the source code if you wish to be able to modify the source code for development or for exploration.


### Run the module

1. Open a Python shell by typing `python` (or `python3`) at the terminal (OSX and Linux users) or at the Conda or Command Prompt (Windows users).
2. Run the module from the Python shell with:
```
import rivers2stratigraphy
```
Instructions will indicate to use the following command to then run the module:
```
rivers2stratigraphy.run()
```

Alternatively, you can do this in one line from the standard terminal with:
```
python -c "import rivers2stratigraphy; rivers2stratigraphy.run()"
```

Alternatively, run the module with provided script (this is the hook used for launching from SedEdu):
```
python3 <path-to-installation>run_rivers2stratigraphy.py
```

Please [open an issue](https://github.com/sededu/rivers2stratigraphy/issues) if you encounter any additional error messages! 
Please include 1) operating system, 2) installation method, and 3) copy-paste the error.


#### Smaller Python installation options
Note that if you do not want to install the complete Anaconda Python distribution you can install [Miniconda](https://conda.io/miniconda.html) (a smaller version of Anaconda), or you can install Python alone and use a package manager called pip to do the installation. 
You can get [Python and pip together here](https://www.python.org/downloads/).


## Development

This module is under ongoing development to improve stability and features and optimize performance.
The module also requires occasional maintenance due to dependency updates.
If you are interested in contributing to the code-base please see below for instructions.

If you are interested in contributing to the accompanying worksheets/activities (which would be greatly appreciated!) please see [Writing Activities for SedEdu](https://github.com/sededu/sededu/blob/develop/docs/writing_activities.md)


#### Download the source code

You can download this entire repository as a `.zip` by clicking the "Clone or download button on this page", or by [clicking here](https://github.com/sededu/rivers2stratigraphy/archive/master.zip) to get a `.zip` folder.
Unzip the folder in your preferred location.

If you have installed `git` and are comfortable working with it, you can simply clone the repository to your preferred location.

```
git clone https://github.com/sededu/rivers2stratigraphy.git
```

Open a pull request when you want a review or some comments!
