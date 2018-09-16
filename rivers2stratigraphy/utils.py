# utilities for drawing the gui etc
import numpy as np
from matplotlib.widgets import AxesWidget
import six


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



