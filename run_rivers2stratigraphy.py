import os

## initialize the GUI
thisDir = os.path.dirname(__file__)
thisPath = os.path.join(thisDir,'')
execFile = os.path.join(thisPath, 'rivers2stratigraphy', 'rivers2stratigraphy_gui.py')
exec(open(execFile).read())