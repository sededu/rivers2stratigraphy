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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection, LineCollection
import matplotlib.animation as animation
from itertools import compress
import geom, sedtrans, utils
import sys


# model run params
dt = 100 # timestep in yrs

# setup params
Cf = 0.004 # friction coeff
D50 = 300*1e-6
Beta = 1.5 # exponent to avulsion function
Gamma = 1e-2 # factor for avulsion timing
Df = 0.6 # dampening factor to lateral migration rate change
dxdtstd = 1 # stdev of lateral migration dist, [m/yr]?

conR = 1.65 
cong = 9.81
conrhof = 1000
connu = 1.004e-6
Rep = geom.Repfun(D50, conR, cong, connu) # particle Reynolds num
    
# initial conditions
Bb = BbInit = 4000 # width of belt (m)
yView = yViewInit = 100
Qw = QwInit = 1000
Bast = 0 # Basin top level



class Channel(object):

    def __init__(self, x_cent0=0, dxdt0=0, Bast=0, 
                 age=0, avul_num=0, avul_timer=0, sm=None):

        self.Bast = Bast
        self.x_cent0 = x_cent0
        self.dxdt0 = dxdt0
        self.Qw = sm.Qw
        self.sig = sm.sig
        self.Ta = sm.Ta
        self.Bb = sm.Bb
        self.avul_timer = avul_timer
        self.avul_num = avul_num
        self.age = age

        if avul_timer > self.Ta:
            self.avulsion()

        self.geometry()

        self.x_outer = self.Bb
        # while self.x_outer >= (self.Bb / 2): # keep channel within belt
        #     self.dxdt = self.new_dxdt()
        #     self.dx = dt * (   ((1-Df) * self.dxdt) + ((Df) * self.dxdt0)   )
        #     self.x_cent = self.x_cent0 + self.dx
        #     self.x_side = np.array([[self.x_cent - (self.Bc/2)], 
        #                             [self.x_cent + (self.Bc/2)]])
        #     self.x_outer = np.max(np.abs(self.x_side))
    
        self.dxdt = self.new_dxdt()
        self.dx = dt * (   ((1-Df) * self.dxdt) + ((Df) * self.dxdt0)   )
        self.x_cent = self.x_cent0 + self.dx
        self.x_side = np.array([[self.x_cent - (self.Bc/2)], 
                                [self.x_cent + (self.Bc/2)]])
        self.x_outer = np.max(np.abs(self.x_side))
        if self.x_outer >= (self.Bb / 2): # keep channel within belt
            self.x_cent = self.x_cent0 - self.dx
            self.x_side = np.array([[self.x_cent - (self.Bc/2)], 
                                    [self.x_cent + (self.Bc/2)]])
            self.x_outer = np.max(np.abs(self.x_side))

        self.y_cent = self.Bast - (self.H / 2)
        self.y_upper = self.Bast
        self.ll = self.lower_left()


    def geometry(self):
        Qhat = geom.Qhatfun(self.Qw, D50, cong)
        Hbar = geom.Hbarfun(Qhat, Rep)
        Bbar = geom.Bbarfun(Qhat, Rep)
        Sbar = geom.Sbarfun(Qhat, Rep)
        self.H = geom.dimless2dimfun(Hbar, self.Qw, cong) # new depth
        self.Bc = geom.dimless2dimfun(Bbar, self.Qw, cong) # new width
        self.S = Sbar


    def new_dxdt(self):
        dxdt = (dxdtstd * (np.random.randn()) )
        return dxdt


    def avulsion(self):
        self.x_cent0 = self.new_xcent(Bb = self.Bb)
        self.dxdt0 = 0 # self.new_dxdt()
        self.avul_timer = 0
        self.avul_num = self.avul_num + 1


    def subside(self, dz):
        self.y_cent -= dz
        self.ll = self.lower_left()


    def lower_left(self):
        return np.array([(self.x_cent - (self.Bc / 2)), 
                         (self.y_cent - (self.H / 2))])


    def new_xcent(self, Bb):
        # avulsion chooser
        self.geometry()
        val = np.random.uniform(-Bb/2 + (self.Bc/2), 
                                 Bb/2 - (self.Bc/2))
        return val



class SliderManager(object):
    def __init__(self):
        # read the sliders for values
        self.get_all()

    def get_display_options(self):
        self.colFlag = col_dict[rad_col.value_selected]
        self.yView = slide_yView.val

    def get_calculation_options(self):
        self.Bb = slide_Bb.val * 1000
        self.Qw = slide_Qw.val
        self.sig = slide_sig.val / 1000
        self.Ta = slide_Ta.val

    def get_all(self):
        self.get_display_options()
        self.get_calculation_options()



class Strat(object):

    def __init__(self, ax):
        '''
        initiation of the main strat object
        '''
        
        self.ax = ax
        self.Bast = 0
        self.avul_num = 0
        self.sm = SliderManager()

        self.channel = Channel(x_cent0 = 0, dxdt0 = 0,
                               Bast = self.Bast,
                               sm = self.sm)
        self.channelList = [self.channel]
        self.channelRectangleList = []
        self.channelPatchCollection = PatchCollection(self.channelRectangleList)

        self.BastLine, = ax.plot([-Bbmax*1000/2, Bbmax*1000/2], 
                                 [Bast, Bast], 'k--', animated=True) # plot basin top
        self.VE_val = plt.text(0.675, 0.025, 'VE = ' + str(round(self.sm.Bb/self.sm.yView, 1)),
                               fontsize=12, transform=ax.transAxes, 
                               backgroundcolor='white')
        # self.yView = slide_yView.val


    def func_init(fig, ax, self):
        '''
        handles the initiation of the figure and axes for blitting
        '''

        return self


    def __call__(self, i):
        '''
        called every loop
        '''

        self.channel0 = self.channel

        # find new geom
        self.sm.get_all()

        # subside the channels by sig
        for c in iter(self.channelList):
            c.subside(self.sm.sig * dt)

        # recalculate the channel bodies
        self.channelRectangleList = [Rectangle(c.ll, c.Bc, c.H) for c in iter(self.channelList)]

        self.channel = Channel(x_cent0 = self.channel0.x_cent,
                               dxdt0 = self.channel0.dxdt,
                               Bast = self.Bast,
                               age = i,
                               avul_num = self.channel0.avul_num,
                               avul_timer = self.channel0.avul_timer + dt,
                               sm = self.sm)
        self.channelRectangle = Rectangle(self.channel.ll, self.channel.Bc, 
                                    self.channel.H)

        self.channelList.append(self.channel)
        self.channelRectangleList.append(self.channelRectangle)

        self.channelPatchCollection = PatchCollection(self.channelRectangleList)
        self.channelPatchCollection.set_edgecolor('0') # remove for speed?

        self.qs = sedtrans.qsEH(D50, Cf, 
                                sedtrans.taubfun(self.channel.H, self.channel.S, cong, conrhof), 
                                conR, cong, conrhof)  # sedment transport rate based on new geom

        # # update plot
        if i % 1 == 0 or self.channel.avul_timer == 0:

            self.BastLine.set_ydata([self.Bast, self.Bast])

            if self.sm.colFlag == 'age':
                age_array = np.array([c.age for c in self.channelList])
                self.channelPatchCollection.set_array(age_array)
                self.channelPatchCollection.set_clim(vmin=age_array.min(), vmax=age_array.max())
                self.channelPatchCollection.set_cmap(plt.cm.viridis)
            elif self.sm.colFlag == 'Qw':
                self.channelPatchCollection.set_array(np.array([c.Qw for c in self.channelList]))
                self.channelPatchCollection.set_clim(vmin=Qwmin, vmax=Qwmax)
                self.channelPatchCollection.set_cmap(plt.cm.viridis)
            elif self.sm.colFlag == 'avul':
                self.channelPatchCollection.set_array(np.array([c.avul_num % 9 for c in self.channelList]))
                self.channelPatchCollection.set_clim(vmin=0, vmax=9)
                self.channelPatchCollection.set_cmap(plt.cm.Set1)
            elif self.sm.colFlag == 'sig':
                sig_array = np.array([c.sig for c in self.channelList])
                self.channelPatchCollection.set_array(sig_array)
                self.channelPatchCollection.set_clim(vmin=sigmin/1000, vmax=sigmax/1000)
                self.channelPatchCollection.set_cmap(plt.cm.viridis)

            self.ax.add_collection(self.channelPatchCollection)

            # yview and xview
            ylims = utils.new_ylims(yView = self.sm.yView, Bast = self.Bast)
            self.ax.set_ylim(ylims)
            self.ax.set_xlim(-self.sm.Bb/2, self.sm.Bb/2)

            # vertical exagg text
            self.VE_val.set_text('VE = ' + str(round(self.sm.Bb/self.sm.yView, 1)))

            # remove outdated channels
            stratMin = self.Bast - yViewmax
            outdatedIdx = [c.y_upper < stratMin for c in self.channelList]
            self.channelList = [c for (c, i) in 
                                zip(self.channelList, outdatedIdx) if not i]
            self.channelRectangleList = [c for (c, i) in 
                                         zip(self.channelRectangleList, outdatedIdx) if not i]

        return self.BastLine, self.channelPatchCollection, \
               self.VE_val



# setup the figure
plt.rcParams['toolbar'] = 'None'
plt.rcParams['figure.figsize'] = 8, 6
fig, ax = plt.subplots()
fig.canvas.set_window_title('SedEdu -- rivers2stratigraphy')
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
    strat.Bast = 0
    strat.channelList = [strat.channelList[-1]]
    strat.channelRectangleList = []



def pause_anim(event):
    if anim.running:
        anim.event_source.stop()
    else:
        anim.event_source.start()
    anim.running ^= True



# def redraw_strat(event):
#     fd = anim.new_saved_frame_seq()
#     anim._draw_frame(fd)



# add sliders
widget_color = 'lightgoldenrodyellow'

QwInit = QwInit
Qwmin = 200
Qwmax = 4000
Qwstep = 100
slide_Qw_ax = plt.axes([0.565, 0.875, 0.36, 0.05], facecolor=widget_color)
slide_Qw = utils.MinMaxSlider(slide_Qw_ax, 'water discharge (m$^3$/s)', Qwmin, Qwmax, 
valinit=QwInit, valstep=Qwstep, valfmt="%0.0f", transform=ax.transAxes)
# slide_Qw.on_changed(redraw_strat)

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

btn_slidereset_ax = plt.axes([0.565, 0.14, 0.2, 0.04])
btn_slidereset = utils.NoDrawButton(btn_slidereset_ax, 'Reset sliders', color=widget_color, hovercolor='0.975')
btn_slidereset.on_clicked(slide_reset)

btn_axisreset_ax = plt.axes([0.565, 0.09, 0.2, 0.04])
btn_axisreset = utils.NoDrawButton(btn_axisreset_ax, 'Reset stratigraphy', color=widget_color, hovercolor='0.975')
btn_axisreset.on_clicked(axis_reset)

btn_pause_ax = plt.axes([0.565, 0.03, 0.2, 0.04])
btn_pause = utils.NoDrawButton(btn_pause_ax, 'Pause', color=widget_color, hovercolor='0.975')
btn_pause.on_clicked(pause_anim)


# initialize a few more things
loopcnt = 0 # loop counter
avulcnt = 0 # avulsion timer 
avulrec = 0 # number avulsion
col_dict = {'Water discharge': 'Qw', 
            'Avulsion number': 'avul',
            'Deposit age': 'age',
            'Subsidence rate':'sig'}

# time looping
strat = Strat(ax)

anim = animation.FuncAnimation(fig, strat,
                                interval=100, blit=True)
anim.running = True

plt.show()
