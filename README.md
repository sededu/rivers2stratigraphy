# rivers2stratigraphy


Explore how a river becomes stratigraphy.


<!--
![demo image](./private/demo.png "Demo of GUI")
-->
<img src="https://github.com/amoodie/rivers2stratigraphy/blob/master/private/rivers2stratigraphy_demo.gif" alt="demo_gif">


This readme file provides an overview of the installation and setup process, as well as a brief description of the module worksheets available.

This repository is also linked into the [SedEdu suite of education modules](https://github.com/amoodie/sededu), and can be accessed there as well.



## Installation and running the module

Visit the section of the text below for more information on installing and executing the `rivers2stratigraphy` program on your computer. 


### Requirements

This module depends on Python3, `tkinter`, and the Python packages `numpy`, `scipy`, `matplotlib`. 

__Linux users:__ you will need to install `tkinter` before trying to install the package through `pip3`.
On Ubuntu this is done with `sudo apt install python3-tk`.


<!--
#### Anaconda installation
It is recommended that you install Anaconda, which is an open source distribution of Python. It comes with many basic scientific libraries, some of which are used in the module. Anaconda can be downloaded at https://www.anaconda.com/download/ for Windows, macOS, and Linux. Please follow the instruction provided in the website as to how to install and setup Python on your computer.

#### Custom Python installation
If you want a more flexible and lightweight Python distribution, you can use whatever your favorite package manager is distributing (e.g., `homebrew` or `apt`), check the [Windows downloads here](https://www.python.org/downloads/windows/), or compile [from source](https://www.python.org/downloads/source/).

Whatever method you choose, you will need to install the dependencies. installation by `pip` is easiest, and probably supported if you used anything but compiling from source.
-->


### Installation

To install with `conda` use:
```
conda install -c amoodie rivers2stratigraphy
```

To install globally with `pip` from Pypi use:
```
pip3 install rivers2stratigraphy
```

Note that you may need to use `sudo` on OSX and Linux or run as administrator on Windows.

See below instructions for downloading the source code.


### Run the module

Run the module from the Python shell with:
```
import rivers2stratigraphy
rivers2stratigraphy.run()
```

Alternatively, run the module with provided script:
```
python3 <path-to-installation>/run_rivers2stratigraphy.py
```

Note that this may throw an error on closing the window, but this is not a problem to functionality.

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
