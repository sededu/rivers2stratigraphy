import pytest
import platform

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np
import matplotlib


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


@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_launch_fig_compare():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    return gui.fig
