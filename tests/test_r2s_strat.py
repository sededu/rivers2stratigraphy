import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np


def test_single_strat_call():

    from rivers2stratigraphy.gui import GUI
    from rivers2stratigraphy.strat import Strat

    gui = GUI()
    gui.strat = Strat(gui)

    gui.strat(i=0)

    assert len(gui.strat.activeChannelPatches) == 2
    assert not gui.strat.channelBodyList # list is empty



def test_convert_active_channel_to_channel_body():

    from rivers2stratigraphy.gui import GUI
    from rivers2stratigraphy.strat import Strat

    gui = GUI()
    gui.strat = Strat(gui)

    for i in range(int(gui.sm.Ta / gui.sm.dt)+2):
        gui.strat(i=i)

    assert len(gui.strat.channelBodyList) == 1



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_gui_strat_call():

    from rivers2stratigraphy.gui import GUI
    from rivers2stratigraphy.strat import Strat

    np.random.seed(0)

    gui = GUI()
    gui.strat = Strat(gui)

    gui.strat(i=0)

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_gui_convert_to_channel_body_call():

    from rivers2stratigraphy.gui import GUI
    from rivers2stratigraphy.strat import Strat

    np.random.seed(0)

    gui = GUI()
    gui.strat = Strat(gui)

    for i in np.arange(gui.sm.Ta / gui.sm.dt + 3):
        gui.strat(i=i)

    return gui.fig
