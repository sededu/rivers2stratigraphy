# utilities for drawing the gui etc


class Config: 
    """
    dummy config class for storing info during generation of GUI
    """

    pass


def format_number(number):
    integer = int(round(number, -1))
    string = "{:,}".format(integer)
    return(string)


def format_table(number):
    integer = (round(number, 1))
    string = str(integer)
    return(string)


def new_ylims(yView, Bast):
    return Bast-yView, Bast+0.1*yView


def normalizeColor(v, minV, maxV):
    return (v-minV)/(maxV-minV)


def strat_reset(event, gui):
    gui.strat.Bast = 0
    gui.strat.channelBodyList = []


def slide_reset(event, gui):
    gui.sm.slide_Qw.reset()
    gui.sm.slide_sig.reset()
    gui.sm.slide_Ta.reset()
    gui.sm.rad_col.set_active(0)
    gui.sm.slide_yView.reset()
    gui.sm.slide_Bb.reset()