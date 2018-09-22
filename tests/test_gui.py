import pytest
import platform

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np
import matplotlib

# from rivers2stratigraphy.gui import GUI, Runner
# from rivers2stratigraphy.strat import Strat

# gui = GUI()


def test_get_matplotlib_backend():
    ans = matplotlib.get_backend()
    platType = platform.system()
    if platType in {'Linux'}:
        assert ans == 'Qt5Agg'
    elif platType in {'Darwin'}:
        assert ans == 'MacOSX'
    

def test_set_matplotlib_backend():
    matplotlib.use('Qt5Agg', warn=False)

    ans = matplotlib.get_backend()
    assert ans == 'Qt5Agg'
