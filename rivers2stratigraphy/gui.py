"""
rivers2stratigraphy GUI -- build river stratigraphy interactively
  Stratigraphic model based on LAB models, i.e., geometric channel body is  
  deposited in "matrix" of floodplain mud. The channel is always fixed to the 
  basin surface and subsidence is only control on vertical stratigraphy.
  Horizontal stratigraphy is set by 1) lateral migration (drawn from a pdf) 
  and dampened for realism, and 2) avulsion that is set to a fixed value.
  
  written by Andrew J. Moodie
  amoodie@rice.edu
  Feb 2018

"""

# import matplotlib
# matplotlib.use('TkAgg', warn=False)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from .strat import Strat
from .slider_manager import SliderManager
from . import geom, sedtrans, utils


class GUI(object):

    """     
    main GUI object that selects parameters for initialization and
    handles creation of all the needed parts of the model. This class is
    initialized below by class Runner if this file is run as __main__ 
    """

    def __init__(self):
        # initial conditions
        
        config = utils.Config()

        # model run params
        config.dt = 100 # timestep in yrs
        self._paused = False

        # setup params
        config.Cf = 0.004 # friction coeff
        config.D50 = 300*1e-6
        config.Beta = 1.5 # exponent to avulsion function
        config.Df = 0.6 # dampening factor to lateral migration rate change
        config.dxdtstd = 1 # stdev of lateral migration dist, [m/yr]?

        # constants
        config.conR = 1.65
        config.cong = 9.81
        config.conrhof = 1000
        config.connu = 1.004e-6
        config.Rep = geom.Repfun(config.D50, config.conR, config.cong, config.connu) # particle Reynolds num
            
        # water discharge slider params
        config.Qw = config.Qwinit = 1000
        config.Qwmin = 200
        config.Qwmax = 4000
        config.Qwstep = 100

        # subsidence slider params
        config.sig = config.siginit = 2
        config.sigmin = 0
        config.sigmax = 5
        config.sigstep = 0.2

        # avulsion timescale slider params
        config.Ta = config.Tainit = 500
        config.Tamin = config.dt
        config.Tamax = 1500
        config.Tastep = 10

        # yView slider params
        config.yView = config.yViewinit = 100
        config.yViewmin = 25
        config.yViewmax = 250
        config.yViewstep = 25

        # basin width slider params
        config.Bb = config.Bbinit = 4000 # width of belt (m)
        config.Bbmin = 1
        config.Bbmax = 10
        config.Bbstep = 0.5
        
        # additional initializations
        config.Bast = 0 # Basin top level

        # setup the figure
        plt.rcParams['toolbar'] = 'None'
        plt.rcParams['figure.figsize'] = 8, 6
        self.fig, self.strat_ax = plt.subplots()
        self.fig.canvas.set_window_title('SedEdu -- rivers2stratigraphy')
        plt.subplots_adjust(left=0.085, bottom=0.1, top=0.95, right=0.5)
        self.strat_ax.set_xlabel("channel belt (km)")
        self.strat_ax.set_ylabel("stratigraphy (m)")
        plt.ylim(-config.yView, 0.1*config.yView)
        plt.xlim(-config.Bb/2, config.Bb/2)
        self.strat_ax.xaxis.set_major_formatter( plt.FuncFormatter(
                            lambda v, x: str(v / 1000).format('%0.0f')) )

        # add sliders
        self.config = config
        self.sm = SliderManager(self)

        
    def pause_anim(self, event):
        """
        pause animation by altering hidden var
        """
        if self._paused:
            self._paused = False
        else:
            self._paused = True



class Runner(object):
    def __init__(self):
        gui = GUI()

        # time looping
        gui.strat = Strat(gui)

        anim = animation.FuncAnimation(gui.fig, gui.strat, 
                                       interval=100, blit=False,
                                       save_count=None)

        plt.show()



if __name__ == '__main__':
    runner = Runner()

    
