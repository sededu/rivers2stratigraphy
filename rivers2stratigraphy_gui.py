# rivers2stratigraphy GUI -- build river stratigraphy interactively
#   Stratigraphic model based on LAB models, i.e., geometric channel body is  is deposited in "matrix" of floodplain mud.
#   The channel is always fixed to the basin surface and subsidence is only control on vertical stratigraphy.
#   Horizontal stratigraphy is set by 1) lateral migration (drawn from a pdf) and dampened for realism, and 2) avulsion that is parameterized by sediment input.
#   Default parameters are based on measurements for Piceance and Big Horn basins from Foreman et al., 2012 and Foreman, 2014
#
#   written by Andrew J. Moodie
#   amoodie@rice.edu
#   May 2017
#
#   TODO:
#    - lateral migration as a function of sediment input
#    - aggradation as a function of sediment input
#    - avulsion as a function of superelevation

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import geom, sedtrans, utils

# model run params
# TIME = 20000 # model duration
dt = 10 # timestep in yrs
# T = TIME / dt # number of timesteps
# QwInit = 200 # starting flood discharge
# fact = 10 # factor increase in discharge through PETM release phase
# dur = 10000 # duration of PETM release phase
# sigInit = 0.001 # subsidence
# Qw = set_Qw('lin', Qwinit, fact, dur, dt, T) # create curve for flood discharges
Bb = 2000 # width of belt

# setup params
Cf = 0.004 # friction coeff
D50 = 300*1e-6
Beta = 1.5 # exponent to avulsion function
Gamma = 1e-2 # factor for avulsion timing
# Ta = 500 # timescale of avulsion, [yr]
Df = 0.001 # dampening factor to lateral migration rate change
dxstd = 0.5 # stdev of lateral migration dist, [m/yr]?

conR = 1.65 
cong = 9.81
conrhof = 1000
connu = 1.004e-6
    
# initial conditions
yView = 100
QwInit = 300
Qhat = geom.Qhatfun(QwInit, D50, cong) # dimensionless Qw
Rep = geom.Repfun(D50, conR, cong, connu) # particle Reynolds num
Hbar = geom.Hbarfun(Qhat, Rep) # dimensionless depth
Hnbf = geom.dimless2dimfun(Hbar, QwInit, cong) # depth
Bast = -yView + Hnbf # Basin top level
Ccc = np.array([ (Bb / 2), (0 - (Hnbf / 2)) ]) # Channel center center
avulct = 0 # count time since last avul (for triggering)
dx = dt * (dxstd * np.random.randn()) # lateral migration per timestep [m/yr]


# sig = sigInit
# Qw = QwInit

# setup the figure
plt.rcParams['toolbar'] = 'None'
plt.rcParams['figure.figsize'] = 8, 6
plt.ion()
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.075, bottom=0.1, top=0.95, right=0.5)
ax.set_xlabel("channel belt (m)")
ax.set_ylabel("stratigraphy (m)")
plt.ylim(-yView, 0.1*yView)
plt.xlim(0, Bb)

# add plot elements
BastLine, = plt.plot([0, Bb*2], [Bast, Bast], 'k--') # plot basin top

# zedLine = plt.plot(x[:mouIdx]/1000, eta[:mouIdx]+zed[:mouIdx], \
# 'k--', lw=1.2) # plot levee
# waterLine, = plt.plot(x/1000, eta+H, lw=2, color='blue') # plot initial condition
# QwValue = plt.text(0.7, 0.9, "Qw = " + utils.format_number(Qw), transform=ax.transAxes)
# BwValue = plt.text(( (Xs[1]-Xs[0])/4 + Xs[0])/1000, 52, \
# "backwater from \n" + "RK " + str(L*mou/1000-round(Xs[0]/1000)) + " to " + str(L*mou/1000-round(Xs[1]/1000)), \
# horizontalalignment="center", backgroundcolor="white")
# BwBracket, = plt.plot(np.array([Xs[0], Xs[0], Xs[1], Xs[1]])/1000, np.array([36, 40, 40, 36]), 'k-', lw=1.2)



# add sliders
slide_color = 'lightgoldenrodyellow'

QwInit = QwInit
Qwmin = 100
Qwmax = 2000
Qwstep = 100
slide_Qw_ax = plt.axes([0.575, 0.85, 0.36, 0.05], facecolor=slide_color)
slide_Qw = utils.MinMaxSlider(slide_Qw_ax, 'water discharge (m$^3$/s)', Qwmin, Qwmax, 
valinit=QwInit, valstep=Qwstep, valfmt="%0.0f", transform=ax.transAxes)
QwCmapIdx = np.linspace(Qwmin, Qwmax, (Qwmax-Qwmin)/Qwstep+1)
QwCmap = plt.cm.viridis(QwCmapIdx)

sigInit = 0.005
sigmin = 0.0001
sigmax = 0.05
slide_sig_ax = plt.axes([0.575, 0.7, 0.36, 0.05], facecolor=slide_color)
slide_sig = utils.MinMaxSlider(slide_sig_ax, 'subsidence (m/yr)', sigmin, sigmax, 
valinit=sigInit, valstep=0.0005, valfmt="%g", transform=ax.transAxes)

TaInit = 500
Tamin = 10
Tamax = 2000
slide_Ta_ax = plt.axes([0.575, 0.55, 0.36, 0.05], facecolor=slide_color)
slide_Ta = utils.MinMaxSlider(slide_Ta_ax, 'avulsion timescale (yr)', Tamin, Tamax, 
valinit=TaInit, valstep=10, valfmt="%i", transform=ax.transAxes)


# Qwmap = parula(length(unique(Qw))) # map to color by discharge
# [~, ~, Qwidx] = unique(Qw) # get ref index
# strat = figure()


loopcnt = 0 # loop counter
avulcnt = 0 # avulsion timer 
avulrec = 0 # number avulsion


chanAct = np.zeros(1, dtype=[('coords', float, (4,2)),
                             ('sig',     float, 1),
                             ('avul',   int, 1),
                             ('Qw',    float, 4),
                             ('age',    int, 1)])
chanList = chanAct # all channels in memory
chanListPoly = []
chanColl = PatchCollection(chanListPoly)
ax.add_collection(chanColl)
# print("chanAct = ", chanAct)

# time looping
while plt.fignum_exists(1):
    # update position of old channels
    # for c in 

    # get new values from sliders
    Qw = slide_Qw.val
    sig = slide_sig.val
    Ta = slide_Ta.val

    # find new geom
    Qhat = geom.Qhatfun(Qw, D50, cong)
    Hbar = geom.Hbarfun(Qhat, Rep)
    Bcbar = geom.Bbarfun(Qhat, Rep)
    Sbar = geom.Sbarfun(Qhat, Rep)
    Hnbf = geom.dimless2dimfun(Hbar, Qw, cong) # new depth
    Bc = geom.dimless2dimfun(Bcbar, Qw, cong) # new width
    S = Sbar
    
    # update model configurations
    qsin = sedtrans.qsEH(D50, Cf, sedtrans.taubfun(Hnbf, S, cong, conrhof), conR, cong, conrhof)  # sedment transport rate based on new geom
    dx = (dt * dxstd * np.random.randn()) + ((1-Df)*dx) # lateral migration for dt
    Bast = Bast + (sig * dt)
    # Bast = Bast
    while Ccc[0] + dx > Bb-(Bc/2) or Ccc[0] + dx < 0+(Bc/2): # keep channel within belt
        dx = (dt * dxstd * np.random.randn()) + ((1-Df)*dx)
    Ccc = [Ccc[0] + dx, Bast - (Hnbf/2)] # new channel center
    
    # avulsion handler
    avulcnt += 1 # increase since avul count
    if avulcnt > Ta: # if time since is more than Ta: due for one
        Ccc = np.hstack([np.random.uniform(Bc/2, Bb-Bc/2, 1), Ccc[1]])
        dx = 0 # reset dampening to 0 for new channel
        avulcnt = 0 # reset count
        avulrec += 1 # increment avulsion number
        # chanList = np.vstack((chanList, chanAct))
    
    # store data
    # rec(t, :) = [Qw, Bc, Hnbf, S, dx, sig, qsin, Fa, avulrec] # store data
    
    # update plot
    if loopcnt % 5 == 0:
        BastLine.set_ydata([Bast, Bast])

        newCoords = geom.Ccc2coordsfun(Ccc, Bc, Hnbf)
        chanAct['coords'] = newCoords
        chanAct['sig'] = sig
        chanAct['avul'] = avulrec
        chanAct['Qw'] = plt.cm.viridis(utils.normalizeColor(Qw, Qwmin, Qwmax))
        chanAct['age'] = loopcnt
        chanActPoly = Polygon(newCoords, facecolor='0.5', edgecolor='black')

        chanList = np.vstack((chanList, chanAct))
        chanListPoly.append(chanActPoly)

        chanColl.remove()
        chanColl = PatchCollection(chanListPoly)
        chanColl.set_edgecolor('0')
        chanColl.set_facecolor( np.vstack(chanList['Qw']) )
        ax.add_collection(chanColl) 

    plt.pause(0.001)
    avulcnt += dt
    loopcnt += dt