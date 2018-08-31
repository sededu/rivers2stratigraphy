def get_response():
    resp = input("Would you like to launch the module now? [y/n] ").lower()
    print(resp)
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
    print(resp)
    if resp:
        import os

        ## initialize the GUI
        # thisDir = os.path.dirname(__file__)
        # thisPath = os.path.join(thisDir,'')
        # execFile = os.path.join(thisPath, 'rivers2stratigraphy.py')
        # exec(open(execFile).read())

        exec(open('rivers2stratigraphy.py').read())

    # rivers2stratigraphy_gui()

if __name__ == "__main__":
    import_runnner()