import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np

from rivers2stratigraphy.channel import ActiveChannel, ChannelState, ChannelBody
from rivers2stratigraphy.gui import GUI
from rivers2stratigraphy.strat import Strat

gui = GUI()
strat = Strat(gui)


def test_intial_ActiveChannel():
    
    activeChannel = strat.activeChannel
    
    assert activeChannel.Bast == 0
    assert activeChannel.age == 0
    assert activeChannel.avul_num == 0
    assert len(activeChannel.stateList) == 1
    

def test_ActiveChannel_timestep():
    
    avul_timer0 = strat.activeChannel.avul_timer

    strat.activeChannel.timestep()

    expected_ll = np.round( strat.activeChannel.stateList[1].ll[1] - strat.sm.sig * strat.sm.dt , 4)
    new_ll = np.round( strat.activeChannel.stateList[0].ll[1] , 4)

    assert new_ll == expected_ll
    assert strat.activeChannel.avul_timer == avul_timer0 + strat.sm.dt
