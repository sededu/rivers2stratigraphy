import pytest
import platform

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np
import matplotlib


# def test_get_matplotlib_backend():

#     ans = matplotlib.get_backend()
#     platType = platform.system()

#     if platType in {'Linux'}:
#         assert ans in {'Qt5Agg', 'Qt4Agg'}

#     elif platType in {'Darwin'}:
#         assert ans in {'Qt5Agg', 'MacOSX'}

#     elif platType in {'Windows'}:
#         assert ans in {'Qt5Agg', 'Qt4Agg'}



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_launch_fig():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_line_into_strat_ax():

    from rivers2stratigraphy.gui import GUI
    from rivers2stratigraphy.strat import Strat

    gui = GUI()
    gui.strat_ax.plot([-2000, 2000], [-100, 10])

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_change_Qw_slider():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    gui.sm.slide_Qw.set_val(gui.config.Qwmax)
    gui.fig.canvas.draw_idle()

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_change_sig_slider():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    gui.sm.slide_sig.set_val(gui.config.sigmax)
    gui.fig.canvas.draw_idle()

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_change_Ta_slider():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    gui.sm.slide_Ta.set_val(gui.config.Tamax)
    gui.fig.canvas.draw_idle()

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_change_yView_slider():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    gui.sm.slide_yView.set_val(gui.config.yViewmax)
    gui.fig.canvas.draw_idle()

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_change_Bb_slider():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    gui.sm.slide_Bb.set_val(gui.config.Bbmax)
    gui.fig.canvas.draw_idle()

    return gui.fig


@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_change_rad_col():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    gui.sm.rad_col.set_active(2)
    gui.fig.canvas.draw_idle()

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_reset_sliders_button_image():

    from rivers2stratigraphy.gui import GUI

    gui = GUI()
    gui.sm.slide_Qw.set_val(gui.config.Qwmax)
    gui.sm.slide_sig.set_val(gui.config.sigmax)
    gui.sm.slide_Ta.set_val(gui.config.Tamax)
    gui.sm.slide_yView.set_val(gui.config.yViewmax)
    gui.sm.slide_Bb.set_val(gui.config.Bbmax)
    gui.sm.rad_col.set_active(2)
    gui.fig.canvas.draw_idle()

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', tolerance=20)
def test_gui_convert_to_channel_body_call():

    from rivers2stratigraphy.gui import GUI
    from rivers2stratigraphy.strat import Strat

    np.random.seed(0)

    gui = GUI()
    gui.strat = Strat(gui)

    for i in np.arange(int(gui.sm.Ta / gui.sm.dt)+2):
        gui.strat(i=i)

    return gui.fig



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_reset_strat_button_image():

    from rivers2stratigraphy.gui import GUI
    from rivers2stratigraphy.strat import Strat
    from rivers2stratigraphy.utils import strat_reset

    np.random.seed(0)

    gui = GUI()
    gui.strat = Strat(gui)

    for i in np.arange(int(gui.sm.Ta / gui.sm.dt)*5):
        gui.strat(i=i)

    strat_reset(None, gui)
    gui.strat(i=i+1)

    return gui.fig
