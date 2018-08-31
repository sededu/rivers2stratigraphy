def get_response():
    resp = input("Would you like to launch the module now? [y/n] ").lower()
    if resp == "y":
        return True
    elif resp == "n":
        return False
    else:
        raise ValueError("invalid input: select [y/n]")


def import_runnner():
    """
    a super simple method to run the gui from a Python shell
    """

    # from . import rivers2stratigraphy_gui as rtsrun
    # 
    # rtsrun()
    print("\n\n")
    print("SedEdu -- rivers2stratigraphy Module")
    print("\n\n")

    resp = get_response()
    if resp:
        import rivers2stratigraphy

        import os

        ## initialize the GUI
        thisDir = os.path.dirname(__file__)
        thisPath = os.path.join(thisDir,'')
        execFile = os.path.join(thisPath, 'rivers2stratigraphy.py')
        exec(open(execFile).read())

    # rivers2stratigraphy_gui()

import_runnner()
