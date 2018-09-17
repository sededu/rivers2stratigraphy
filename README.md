# rivers2stratigraphy


Explore how a river becomes stratigraphy

<img src="https://github.com/amoodie/rivers2stratigraphy/blob/master/private/rivers2stratigraphy_demo.gif" alt="demo_gif">


This readme file provides an overview of the installation and setup process, as well as a brief description of the module worksheets available.

This repository is also linked into the [SedEdu suite of education modules](https://github.com/amoodie/sededu), and can be accessed there as well.



## About the model
Stratigraphic model based on LAB models, i.e., geometric channel body is deposited in "matrix" of floodplain mud. 
The channel is always fixed to the basin surface and subsidence is only control on vertical stratigraphy.
Horizontal stratigraphy is set by 1) lateral migration (drawn from a pdf) and dampened for realism, and 2) avulsion that is set to a fixed value.



## Installation and running the module

Visit the section of the text below for more information on installing and executing the `rivers2stratigraphy` program on your computer. 


### Requirements

This module depends on Python 3, `tkinter`, and the Python packages `numpy`, `scipy`, `matplotlib`. 

#### Installing Python 3

If you are new to Python, it is recommended that you install Anaconda, which is an open source distribution of Python. 
It comes with many basic scientific libraries, some of which are used in the module. Anaconda can be downloaded at https://www.anaconda.com/download/ for Windows, macOS, and Linux. 
Please follow the instruction provided in the website as to how to install and setup Python on your computer.
Be sure to select the Python 3.x installation.


__Linux users:__ you will need to also install `tkinter` before trying to install the module below package through `conda` or `pip3`.
On Ubuntu this is done with `sudo apt install python3-tk`.
Windows and Mac distributions should come with `python3-tk` installed.

Note that if you do not want to install the complete Anaconda Python distribution you can install [Miniconda](https://conda.io/miniconda.html) (a smaller version of Anaconda), or you can install Python alone and use a package manager called pip to do the installation. 
You can get [Python and pip together here](https://www.python.org/downloads/).


#### Installing the module

If you installed Anaconda Python or Miniconda, you can install the module by opening a terminal on Linux or OSX (command prompt in Windows) and typing the following command.

To install with `conda` use:
```
conda install -c amoodie rivers2stratigraphy
```

If asked to proceed, type `Y`  and press enter to continue installation. This process may take a few minutes as the necessary source code is downloaded.
If the installation succeeds proceed below to the "Run the module" section.


To install with `pip` from Pypi use (not recommended for entry-level users):
```
pip3 install rivers2stratigraphy
```

Note that you may need to use `sudo` on OSX and Linux or run as administrator on Windows.

See below instructions for downloading the source code if you wish to be able to modify the source code for development.

Please [open an issue](https://github.com/amoodie/rivers2stratigraphy/issues) if you encounter any additional error messages! 
Please include 1) operating system, 2) installation method, and 3) copy-paste the error.


### Run the module

Now, open a Python shell by typing `python3` at the terminal (or command prompt) prompt.

Finally, run the module from the Python shell with:
```
import rivers2stratigraphy
```

Instructions will indicate to use the following command to then run the module:
```
rivers2stratigraphy.run()
```


Alternatively, run the module with provided script (this is the hook used for launching from SedEdu):
```
python3 <path-to-installation>/run_rivers2stratigraphy.py
```


Please [open an issue](https://github.com/amoodie/rivers2stratigraphy/issues) if you encounter any additional error messages! 
Please include 1) operating system, 2) installation method, and 3) copy-paste the error.



## Development

This module is under ongoing development to improve stability and features and optimize performance.
If you are interested in contributing to code please see below for instructions.

If you are interested in contributing to the the accompanying activites (which would be greatly appreciated!) please see [Writing Activites for SedEdu](https://github.com/amoodie/sededu/blob/develop/docs/writing_activities.md)


#### Download the source code

You can download this entire repository as a `.zip` by clicking the "Clone or download button on this page", or by [clicking here](https://github.com/amoodie/rivers2stratigraphy/archive/master.zip) to get a `.zip` folder. Unzip the folder in your preferred location.

If you have installed `git` and are comfortable working with it, you can simply clone the repository to your preferred location.

```
git clone https://github.com/amoodie/rivers2stratigraphy.git
```

Open a pull request when you want a review or some comments!
