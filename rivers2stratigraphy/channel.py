
import numpy as np
from matplotlib.patches import Polygon, Rectangle
import shapely.geometry as sg
import shapely.ops as so

from . import geom, sedtrans, utils


class ActiveChannel(object):
    def __init__(self, Bast = 0, age = 0, Ta = 100, 
                 avul_num = 0, sm = None, parent = None):
        
        self.sm = sm
        self.avul_num = avul_num
        self.avulsed = False
        self.avul_timer = 0
        self.Ta = Ta
        self.age = age
        self.parent = parent
        self.Bast = Bast
            
        self.state = ChannelState(new_channel = True, dxdt =0, Bast = Bast, age = 0, sm = self.sm)
        self.stateList = [self.state]

    def timestep(self):
        self.state0 = self.state

        # do all calculations here, and pass needed values to State
        self.subside()
        x_cent, dxdt = self.migrate()

        self.state = ChannelState(x_cent = x_cent, dxdt = dxdt,
                           Bast = self.state0.Bast, sm = self.sm)
        self.stateList.append(self.state)

        if self.avul_timer >= self.Ta:
            self.avulsion()
        else:
            self.avul_timer += self.sm.dt

    def migrate(self):
        dxdt = (self.sm.dxdtstd * (np.random.randn()) )
        dx = self.sm.dt * ( ((1-self.sm.Df) * dxdt) + ((self.sm.Df) * self.state0.dxdt) )
        x_cent = self.state0.x_cent + dx
        return x_cent, dxdt

    def avulsion(self):
        self.avulsed = True

    def subside(self):
        # subside method to be called each iteration
        dz = (self.sm.sig * self.sm.dt)
        for s in iter(self.stateList):
            s.state_subside(dz)
            s.ll = s.lower_left()



class ChannelBody(object):
    '''
    when the channel is avulsed, convert it to a ChannelBody type
    '''
    def __init__(self, channel):
        nState = len(channel.stateList)
        # shapeState = np.shape(channel.stateList)
        stateBoxes = []
        QwList = np.zeros((nState, 1))
        sigList = np.zeros((nState, 1))

        for s, i in zip(iter(channel.stateList), np.arange(nState)):
            stateBoxes.append(self.rect2box(s.ll, s.Bc, s.H)) # different way to do this?
            # instead go straight polygon to union?

            QwList[i] = s.Qw
            sigList[i] = s.sig

        self.y_upper = channel.stateList[-1].y_upper

        self.conversionFlag = "same" # option to select how to convert states to bodies
        if self.conversionFlag == "same":
            # same method for all
            stateSeriesConvexHull = []
            for i, j in zip(stateBoxes[1:], stateBoxes[:-1]):
                seriesUnionTemp = so.cascaded_union([i, j])
                stateSeriesConvexHull.append(seriesUnionTemp.convex_hull)
            stateUnion = so.cascaded_union(stateSeriesConvexHull)
            self.polygonAsArray = np.asarray(stateUnion.exterior)
        elif self.conversionFlag == "diff":
            # different methods for polygon and multipolygon
            stateUnion = so.cascaded_union(stateBoxes) # try so.cascaded_union(stateBoxes[::2]) for speed?
            # if type is polygon
            uniontype = stateUnion.geom_type
            if uniontype == 'Polygon':
                self.polygonAsArray = np.asarray(stateUnion.exterior)
            elif uniontype == 'MultiPolygon':
                stateSeriesConvexHull = []
                for i, j in zip(stateBoxes[1:], stateBoxes[:-1]):
                    seriesUnionTemp = so.cascaded_union([i, j])
                    stateSeriesConvexHull.append(seriesUnionTemp.convex_hull)
                stateUnion = so.cascaded_union(stateSeriesConvexHull)
                self.polygonAsArray = np.asarray(stateUnion.exterior)
        else:
            raise ValueError("invalid conversionFlag in ChannelBody")

        

        self.polygonXs = self.polygonAsArray[:,0]
        self.polygonYs = self.polygonAsArray[:,1]

        self.patch = Polygon(self.polygonAsArray)

        # get all the "means" of variables for coloring values
        self.age = channel.age
        self.Qw = QwList.mean()
        self.avul_num = channel.avul_num
        self.sig = sigList.mean()

    def subside(self, dz):
        # subside method to be called each iteration
        self.polygonYs -= dz
        # self.y_upper = self.polygonYs.max()
        xsys = np.column_stack((self.polygonXs, self.polygonYs))
        self.patch.set_xy(xsys)

    def get_patch(self):
        return self.patch

    def rect2box(self, ll, Bc, H):
        box = sg.box(ll[0], ll[1], 
                     ll[0] + Bc, ll[1] + H)
        return box


class ChannelState(object):

    def __init__(self, new_channel = False, x_cent = 0, dxdt = 0, Bast = 0, age = 0, sm = None):

        self.Bast = Bast
        self.dxdt = dxdt
        self.Qw = sm.Qw
        self.sig = sm.sig
        self.Ta = sm.Ta
        self.Bb = sm.Bb
        self.age = age
        self.sm = sm

        self.calc_geometry()

        if new_channel:
            self.x_cent = self.pick_x_cent(self.Bb)
        else:
            self.x_cent = x_cent

        self.x_side = np.array([[self.x_cent - (self.Bc/2)], 
                                [self.x_cent + (self.Bc/2)]])
        self.x_outer = np.max(np.abs(self.x_side))
        if self.x_outer >= (self.Bb / 2): # keep channel within belt
            self.x_cent = self.x_cent
            self.x_side = np.array([[self.x_cent - (self.Bc/2)], 
                                    [self.x_cent + (self.Bc/2)]])
            self.x_outer = np.max(np.abs(self.x_side))

        self.y_cent = self.Bast - (self.H / 2)
        self.y_upper = self.Bast
        self.ll = self.lower_left()


    def calc_geometry(self):
        Qhat = geom.Qhatfun(self.Qw, self.sm.D50, self.sm.cong)
        Hbar = geom.Hbarfun(Qhat, self.sm.Rep)
        Bbar = geom.Bbarfun(Qhat, self.sm.Rep)
        Sbar = geom.Sbarfun(Qhat, self.sm.Rep)
        self.H = geom.dimless2dimfun(Hbar, self.Qw, self.sm.cong) # new depth
        self.Bc = geom.dimless2dimfun(Bbar, self.Qw, self.sm.cong) # new width
        self.S = Sbar


    def state_subside(self, dz):
        # subside method to be called each iteration
        self.y_cent -= dz
        self.ll = self.lower_left()


    def lower_left(self):
        # method to calculate the lower left corner of channel
        return np.array([(self.x_cent - (self.Bc / 2)), 
                         (self.y_cent - (self.H / 2))])

    def pick_x_cent(self, Bb):
        new_x_cent = np.random.uniform(-Bb/2 + (self.Bc/2), 
                                 Bb/2 - (self.Bc/2))
        return new_x_cent
