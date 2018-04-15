# rivers2stratigraphy GUI -- build river stratigraphy interactively
#   Stratigraphic model based on LAB models, i.e., geometric channel body is  
#   deposited in "matrix" of floodplain mud. The channel is always fixed to the 
#   basin surface and subsidence is only control on vertical stratigraphy.
#   Horizontal stratigraphy is set by 1) lateral migration (drawn from a pdf) 
#   and dampened for realism, and 2) avulsion that is set to a fixed value.
#   Default parameters are based on measurements for Piceance and Big Horn 
#   basins from Foreman et al., 2012 and Foreman, 2014
#
#   written by Andrew J. Moodie
#   amoodie@rice.edu
#   Feb 2018
#
#   TODO:
#    - control for "natural" ad default where lateral migration 
#       and Ta are a function of sediment transport (Qw)
#    - support for coloring by subsidence
#    - fix runtime warnings on startup

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.animation import FuncAnimation
import shapely.geometry as sg
import shapely.ops as so
from itertools import compress
import geom, sedtrans, utils

import time # DELETE FOR RELEASE

# model run params
dt = 50 # timestep in yrs

# setup params
Cf = 0.004 # friction coeff
D50 = 300*1e-6
Beta = 1.5 # exponent to avulsion function
Gamma = 1e-2 # factor for avulsion timing
Df = 0.0005 # dampening factor to lateral migration rate change
dxstd = 0.5 # stdev of lateral migration dist, [m/yr]?

conR = 1.65 
cong = 9.81
conrhof = 1000
connu = 1.004e-6
    
# initial conditions
Bb = BbInit = 4000 # width of belt (m)
yView = yViewInit = 100
Qw = QwInit = 1000
Qhat = geom.Qhatfun(Qw, D50, cong) # dimensionless Qw
Rep = geom.Repfun(D50, conR, cong, connu) # particle Reynolds num
Hbar = geom.Hbarfun(Qhat, Rep) # dimensionless depth
Hnbf = geom.dimless2dimfun(Hbar, Qw, cong) # depth
Bast = -yView + Hnbf # Basin top level
Bast = 0 # Basin top level
Ccc = np.array([ 0, (0 - (Hnbf / 2)) ]) # Channel center center
avulct = 0 # count time since last avul (for triggering)
dx = dt * (dxstd * np.random.randn()) # lateral migration per timestep [m/yr]

class Channel(object):
    # rand_dxdt = (dxstd * np.random.randn()) 

    def __init__(self, cent_x0=0, dxdt0=0, Bast=0, parent=None):
        # self.read_sliders()
        self.char = SliderManager()

        self.geometry = self.Geometry()
        self.dxdt = (dxstd * np.random.randn()) + ((1-Df) * dxdt0)
        self.dx = self.dxdt * dt

        self.cent_x = cent_x0 + self.dx
        self.cent_y = Bast - self.geometry.H
        self.ll = np.array([(self.cent_x - self.geometry.Bc), (Bast - (self.geometry.H / 2))])
        self.max_x_abs = abs(self.cent_x + self.geometry.Bc)
        # self.ur = 1


    class Geometry(object):
        def __init__(self):
            Qhat = geom.Qhatfun(Qw, D50, cong)
            Hbar = geom.Hbarfun(Qhat, Rep)
            Bbar = geom.Bbarfun(Qhat, Rep)
            Sbar = geom.Sbarfun(Qhat, Rep)
            H = geom.dimless2dimfun(Hbar, Qw, cong) # new depth
            Bc = geom.dimless2dimfun(Bbar, Qw, cong) # new width
            S = Sbar
            # self.geometry = {'Qhat': Qhat, 'Hbar': Hbar, 'Bbar': Bbar,
            #             'Sbar': Sbar, 'H': H, 'Bc': Bc, 'S': S}
            self.Bc = Bc
            self.H = H

    # class Characteristics(object):
    #     def __init__(self):
    #         self.sig = sig


class SliderManager(object):
    def __init__(self):
        # read the sliders for values
        self.get_all()

    def get_basin(self):
        self.yView = slide_yView.val
        self.Bb = slide_Bb.val * 1000
        self.colFlag = col_dict[rad_col.value_selected]

    def get_channel(self):
        self.Qw = slide_Qw.val
        self.sig = slide_sig.val / 1000
        self.Ta = slide_Ta.val

    def get_all(self):
        self.get_basin()
        self.get_channel()


class Strat(object):

    def __init__(self, ax):
        # self.read_sliders()
        self.ax = ax
        self.Bast = 0
        # self.Ccc = Ccc
        self.sm = SliderManager()

        self.channel = Channel(cent_x0 = 0, dxdt0 = 0,
                               Bast = self.Bast,
                               parent=self)
        self.chanAct = np.zeros(1, dtype=[('coords', float, (4,2)),
                             ('sig',    float,  4),
                             ('avul',   float,  4),
                             ('Qw',     float,  4),
                             ('age',    int,    1)])
        self.chanList = self.chanAct # all channels in memory
        # chanListPoly = []
        # chanColl = PatchCollection(chanListPoly)

        self.BastLine, = ax.plot([-Bbmax*1000/2, Bbmax*1000/2], 
                                 [Bast, Bast], 'k--') # plot basin top
        self.VE_val = plt.text(0.675, 0.025, 'VE = ' + str(round(self.sm.Bb/self.sm.yView, 1)),
                               fontsize=12, transform=ax.transAxes, 
                               backgroundcolor='white')


    def func_init(self):
        self.BastLine.set_ydata([Bast, Bast])

        return self.BastLine,


    def __call__(self, i):

        print(i)

        # get new values from sliders
        # self.read_sliders()
        self.channel0 = self.channel

        # find new geom
        self.channel = Channel(cent_x0 = self.channel0.cent_x,
                               dxdt0 = self.channel0.dxdt)
        self.sm.get_all()

        
        # update model configurations

        # this validates channel position with basin resizing
        # if abs(channel.Ccc[0]) + channel.geometry.Bc/2 > self.sm.Bb/2: 
            # self.Ccc = np.hstack([np.random.uniform(-self.Bb/2+(Bc/2), self.Bb/2-(Bc/2), 1),
                             # self.Ccc[1]])

        # qsin = sedtrans.qsEH(D50, Cf, 
                             # sedtrans.taubfun(Hnbf, S, cong, conrhof), 
                             # conR, cong, conrhof)  # sedment transport rate based on new geom

        # channel.dx = (dt * dxstd * np.random.randn()) + ((1-Df) * channel.dxdt) # lateral migration for dt
        self.Bast = self.Bast + (self.sm.sig * dt)
        while self.channel.max_x_abs > self.sm.Bb/2-(self.channel.geometry.Bc/2): # keep channel within belt
            dx = (dt * dxstd * np.random.randn()) + ((1-Df)*dx)

        # self.Ccc = [self.Ccc[0] + dx, self.Bast - (Hnbf/2)] # new channel center
        
        # # update plot
        # if loopcnt % 10 == 0 or avulcnt == 0:
        self.BastLine.set_ydata([self.Bast, self.Bast])

        # newCoords = geom.Ccc2coordsfun(Ccc, Bc, Hnbf)
        # newActShp = sg.box(self.Ccc[0]-Bc/2, self.Ccc[1]-Hnbf/2, 
                           # self.Ccc[0]+Bc/2, self.Ccc[1]+Hnbf/2)
        # chanAct['coords'] = newCoords
        # chanAct['sig'] = plt.cm.viridis(utils.normalizeColor(sig*1000, sigmin, sigmax))
        # chanAct['avul'] = avulCmap[avulrec % 9]
        # chanAct['Qw'] = plt.cm.viridis(utils.normalizeColor(Qw, Qwmin, Qwmax))
        # chanAct['age'] = loopcnt

        chanActPoly = Rectangle(self.channel.ll, self.channel.geometry.Bc, 
                                self.channel.geometry.H)
        # chanActPoly = Polygon(newCoords, facecolor='0.5', edgecolor='black')
        self.chanList = np.vstack((self.chanList, self.chanAct))
        chanListPoly.append(chanActPoly)

        # chanColl.remove()
        chanColl = PatchCollection(chanListPoly)
        chanColl.set_edgecolor('0')
        # if colFlag == 'Qw':
        #     chanColl.set_facecolor( np.vstack(chanList['Qw']) )
        # elif colFlag == 'avul':
        #     chanColl.set_facecolor( np.vstack(chanList['avul']) )
        # elif colFlag == 'age':
        #     inViewIdx = [ all( c['coords'][0][:,1] > (Bast - yView) ) 
        #                   for c in chanList ]
        #     # color age to visible strat:
        #     ageCmap = plt.cm.viridis( utils.normalizeColor(
        #         chanList['age'], chanList['age'][inViewIdx].min(), loopcnt).flatten() )
        #     # color age to all strat in memory:
        #     # ageCmap = plt.cm.viridis( utils.normalizeColor(
        #     #     chanList['age'], chanList['age'].min(), loopcnt).flatten() )
        #     chanColl.set_facecolor( ageCmap )
        # elif colFlag == 'sig':
        #     chanColl.set_facecolor( np.vstack(chanList['sig']) )
        self.ax.add_collection(chanColl)

        # # scroll the view
        self.ax.set_ylim(utils.new_ylims(self.sm.yView, self.Bast))
        self.ax.set_xlim(-self.sm.Bb/2, self.sm.Bb/2)
        self.VE_val.set_text('VE = ' + str(round(self.sm.Bb/self.sm.yView, 1)))

        # # avulsion handler
        # avulcnt += 1 # increase since avul count
        # if avulcnt > Ta: # if time since is more than Ta: due for one
        # # abs(Ccc[0] + dx) > Bb/2-(Bc/2)
        #     Ccc = np.hstack([np.random.uniform(-Bb/2+(Bc/2), Bb/2-(Bc/2), 1),
        #                      Ccc[1]])
        #     dx = 0 # reset dampening to 0 for new channel
        #     avulcnt = 0 # reset count
        #     avulrec += 1 # increment avulsion number
        #     chanActShp = sg.box(Ccc[0]-Bc/2, Ccc[1]-Hnbf/2, Ccc[0]+Bc/2, Ccc[1]+Hnbf/2)

        # # remove outdated channels
        # stratMax = Bast - yViewmax
        # chanListOutdatedIdx = geom.outdatedIndex(chanList, stratMax)
        # chanList = chanList[ ~chanListOutdatedIdx ]
        # chanListPoly = [i for (i, v) in 
        #                 zip(chanListPoly, chanListOutdatedIdx) if not v]

        # # draw and update counts
        # # plt.pause(0.000001)
        # avulcnt += dt
        # loopcnt += dt

        return self.BastLine, 




# setup the figure
plt.rcParams['toolbar'] = 'None'
plt.rcParams['figure.figsize'] = 8, 6
fig, ax = plt.subplots()
fig.canvas.set_window_title('SedEdu -- Rivers to Stratigraphy')
plt.subplots_adjust(left=0.085, bottom=0.1, top=0.95, right=0.5)
ax.set_xlabel("channel belt (km)")
ax.set_ylabel("stratigraphy (m)")
plt.ylim(-yViewInit, 0.1*yViewInit)
plt.xlim(-Bb/2, Bb/2)
ax.xaxis.set_major_formatter( plt.FuncFormatter(
                             lambda v, x: str(v / 1000).format('%0.0f')) )

# define reset functions, must operate on global vars
def slide_reset(event):
    slide_Qw.reset()
    slide_sig.reset()
    slide_Ta.reset()
    rad_col.set_active(0)
    slide_yView.reset()
    slide_Bb.reset()


def axis_reset(event):
    global chanList, chanListPoly, Bast
    Bast = 0
    chanList = chanList[-1]
    chanListPoly = []


# add sliders
widget_color = 'lightgoldenrodyellow'

QwInit = QwInit
Qwmin = 200
Qwmax = 4000
Qwstep = 100
slide_Qw_ax = plt.axes([0.565, 0.875, 0.36, 0.05], facecolor=widget_color)
slide_Qw = utils.MinMaxSlider(slide_Qw_ax, 'water discharge (m$^3$/s)', Qwmin, Qwmax, 
valinit=QwInit, valstep=Qwstep, valfmt="%0.0f", transform=ax.transAxes)

sigInit = 2
sigmin = 0
sigmax = 5
sigstep = 0.2
slide_sig_ax = plt.axes([0.565, 0.770, 0.36, 0.05], facecolor=widget_color)
slide_sig = utils.MinMaxSlider(slide_sig_ax, 'subsidence (mm/yr)', sigmin, sigmax, 
valinit=sigInit, valstep=sigstep, valfmt="%g", transform=ax.transAxes)

TaInit = 500
Tamin = dt
Tamax = 1500
slide_Ta_ax = plt.axes([0.565, 0.665, 0.36, 0.05], facecolor=widget_color)
slide_Ta = utils.MinMaxSlider(slide_Ta_ax, 'avulsion timescale (yr)', Tamin, Tamax, 
valinit=TaInit, valstep=10, valfmt="%i", transform=ax.transAxes)
avulCmap = plt.cm.Set1(range(9))

rad_col_ax = plt.axes([0.565, 0.45, 0.225, 0.15], facecolor=widget_color)
rad_col = widget.RadioButtons(rad_col_ax, ('Deposit age', 'Water discharge', 'Subsidence rate', 'Avulsion number'))

yViewInit = yViewInit
yViewmin = 25
yViewmax = 250
slide_yView_ax = plt.axes([0.565, 0.345, 0.36, 0.05], facecolor=widget_color)
slide_yView = utils.MinMaxSlider(slide_yView_ax, 'stratigraphic view (m)', yViewmin, yViewmax, 
valinit=yViewInit, valstep=25, valfmt="%i", transform=ax.transAxes)

BbInit = BbInit # width of belt
Bbmin = 1
Bbmax = 10
slide_Bb_ax = plt.axes([0.565, 0.24, 0.36, 0.05], facecolor=widget_color)
slide_Bb = utils.MinMaxSlider(slide_Bb_ax, 'Channel belt width (km)', Bbmin, Bbmax, 
valinit=BbInit/1000, valstep=0.5, valfmt="%g", transform=ax.transAxes)

# VE_val = plt.text(0.675, 0.025, 'VE = ' + str(round(Bb/yView, 1)),
#                   fontsize=12, transform=ax.transAxes, 
#                   backgroundcolor='white')

btn_slidereset_ax = plt.axes([0.565, 0.14, 0.2, 0.04])
btn_slidereset = widget.Button(btn_slidereset_ax, 'Reset sliders', color=widget_color, hovercolor='0.975')
btn_slidereset.on_clicked(slide_reset)

btn_axisreset_ax = plt.axes([0.565, 0.09, 0.2, 0.04])
btn_axisreset = widget.Button(btn_axisreset_ax, 'Reset stratigraphy', color=widget_color, hovercolor='0.975')
btn_axisreset.on_clicked(axis_reset)

# add plot elements
# BastLine, = ax.plot([-Bbmax*1000/2, Bbmax*1000/2], 
#                      [Bast, Bast], 'k--') # plot basin top

# initialize a few more things
loopcnt = 0 # loop counter
avulcnt = 0 # avulsion timer 
avulrec = 0 # number avulsion
    
chanAct = np.zeros(1, dtype=[('coords', float, (4,2)),
                             ('sig',    float,  4),
                             ('avul',   float,  4),
                             ('Qw',     float,  4),
                             ('age',    int,    1)])
chanList = chanAct # all channels in memory
chanListPoly = []
chanColl = PatchCollection(chanListPoly)
ax.add_collection(chanColl)

chanActShp = sg.box(Ccc[0], Ccc[1], Ccc[0], Ccc[1])

col_dict = {'Water discharge': 'Qw', 
            'Avulsion number': 'avul',
            'Deposit age': 'age',
            'Subsidence rate':'sig'}

# time looping
# while plt.fignum_exists(1):
strat = Strat(ax)
anim = FuncAnimation(fig, strat, init_func=strat.func_init,
                     interval=100, blit=False)

plt.show()