import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

from rivers2stratigraphy.channel import ActiveChannel, ChannelState, ChannelBody
from rivers2stratigraphy.gui import GUI
from rivers2stratigraphy.strat import Strat

gui = GUI()
strat = Strat(gui)


def test_default_ActiveChannel():
    
    activeChannel = ActiveChannel()
    
    assert activeChannel.x_centi == 0
    assert activeChannel.Bast == 0
    assert activeChannel.age == 0
    assert activeChannel.avul_num == 0
    assert activeChannel.sm == None
    assert activeChannel.avul_num == 0
    

def test_ActiveChannel_timestep():
    
    ymax0 = max(strat.activeChannel)
    avul_timer0 = strat.activeChannel.avul_timer

    strat.activeChannel.timestep()
    
    assert strat.activeChannel.stateList[0].ll == strat.activeChannel.stateList[0].ll - strat.sm.sig * strat.sm.dt
    assert strat.activeChannel.avul_timer == avul_timer0 + strat.sm.dt