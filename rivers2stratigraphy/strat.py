import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection, LineCollection
import matplotlib.animation as animation
import shapely.geometry as sg
import shapely.ops as so

from .channel import ActiveChannel, ChannelState, ChannelBody
from . import utils

class Strat(object):

    def __init__(self, gui):
        '''
        initiation of the main strat object
        '''
        
        self.gui = gui
        # self.gui.strat_ax = gui.strat_ax
        self.fig = gui.fig

        self.sm = gui.sm
        self.config = gui.config

        self.Bast = self.sm.Bast

        self.avul_num = 0
        self.color = False
        self.avulCmap = plt.cm.Set1(range(9))
        
        # self._paused = gui._paused

        # create an active channel and corresponding PatchCollection
        self.activeChannel = ActiveChannel(Bast = self.Bast, age = 0, 
                                           Ta = self.sm.Ta, avul_num = 0, 
                                           sm = self.sm)
        self.activeChannelPatchCollection = PatchCollection([Rectangle(self.activeChannel.state.ll, 
                                                                       self.activeChannel.state.Bc, 
                                                                       self.activeChannel.state.H)])
        
        # create a channelbody and corresponding PatchCollection
        self.channelBodyList = []
        self.channelBodyPatchCollection = PatchCollection(self.channelBodyList)

        # add PatchCollestions
        self.gui.strat_ax.add_collection(self.channelBodyPatchCollection)
        self.gui.strat_ax.add_collection(self.activeChannelPatchCollection)

        # set fixed color attributes of PatchCollections
        self.channelBodyPatchCollection.set_edgecolor('0')
        self.activeChannelPatchCollection.set_facecolor('0.6')
        self.activeChannelPatchCollection.set_edgecolor('0')

        self.BastLine, = self.gui.strat_ax.plot([-self.sm.Bbmax*1000/2, gui.sm.Bbmax*1000/2], 
                                 [self.Bast, self.Bast], 'k--', animated=False) # plot basin top
        self.VE_val = plt.text(0.675, 0.025, 'VE = ' + str(round(self.sm.Bb/self.sm.yView, 1)),
                               fontsize=12, transform=self.gui.strat_ax.transAxes, 
                               backgroundcolor='white')


    def __call__(self, i):
        '''
        called every loop
        '''

        # find new slider vals
        self.sm.get_all()

        if not self.gui._paused:
            # timestep the current channel objects
            dz = self.sm.sig * self.sm.dt
            for c in self.channelBodyList:
                c.subside(dz)

            if not self.activeChannel.avulsed:
                # when an avulsion has not occurred:
                self.activeChannel.timestep()

            else:
                # once an avulsion has occurred:
                self.channelBodyList.append( ChannelBody(self.activeChannel) )
                self.avul_num += 1
                self.color = True

                # create a new Channel
                self.activeChannel = ActiveChannel(Bast = self.Bast, age = i, 
                                                   Ta = self.sm.Ta, avul_num = self.avul_num, 
                                                   sm = self.sm)

                # remove outdated channels
                stratMin = self.Bast - self.sm.yViewmax
                outdatedIdx = [c.polygonYs.max() < stratMin for c in self.channelBodyList]
                self.channelBodyList = [c for (c, i) in 
                                        zip(self.channelBodyList, outdatedIdx) if not i]

        # generate new patch lists for updating the PatchCollection objects
        self.activeChannelPatches = [Rectangle(s.ll, s.Bc, s.H) for s 
                                in iter(self.activeChannel.stateList)]
        self.channelBodyPatchList = [c.get_patch() for c in self.channelBodyList]

        # set paths of the PatchCollection Objects
        self.channelBodyPatchCollection.set_paths(self.channelBodyPatchList)
        self.activeChannelPatchCollection.set_paths(self.activeChannelPatches)

        # self.qs = sedtrans.qsEH(D50, Cf, 
        #                         sedtrans.taubfun(self.channel.H, self.channel.S, cong, conrhof), 
        #                         conR, cong, conrhof)  # sedment transport rate based on new geom

        # update plot
        if self.color:
            if self.sm.colFlag == 'age':
                age_array = np.array([c.age for c in self.channelBodyList])
                if age_array.size > 0:
                    self.channelBodyPatchCollection.set_array(age_array)
                    self.channelBodyPatchCollection.set_clim(vmin=age_array.min(), vmax=age_array.max())
                    self.channelBodyPatchCollection.set_cmap(plt.cm.viridis)
            elif self.sm.colFlag == 'Qw':
                self.channelBodyPatchCollection.set_array(np.array([c.Qw for c in self.channelBodyList]))
                self.channelBodyPatchCollection.set_clim(vmin=self.config.Qwmin, vmax=self.config.Qwmax)
                self.channelBodyPatchCollection.set_cmap(plt.cm.viridis)
            elif self.sm.colFlag == 'avul':
                self.channelBodyPatchCollection.set_array(np.array([c.avul_num % 9 for c in self.channelBodyList]))
                self.channelBodyPatchCollection.set_clim(vmin=0, vmax=9)
                self.channelBodyPatchCollection.set_cmap(plt.cm.Set1)
            elif self.sm.colFlag == 'sig':
                sig_array = np.array([c.sig for c in self.channelBodyList])
                self.channelBodyPatchCollection.set_array(sig_array)
                self.channelBodyPatchCollection.set_clim(vmin=self.config.sigmin/1000, vmax=self.config.sigmax/1000)
                self.channelBodyPatchCollection.set_cmap(plt.cm.viridis)
        
        # yview and xview
        ylims = utils.new_ylims(yView = self.sm.yView, Bast = self.Bast)
        self.gui.strat_ax.set_ylim(ylims)
        self.gui.strat_ax.set_xlim(-self.sm.Bb/2, self.sm.Bb/2)

        # vertical exagg text
        if i % 10 == 0:
            self.axbbox = self.gui.strat_ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
            width, height = self.axbbox.width, self.axbbox.height
            self.VE_val.set_text('VE = ' + str(round((self.sm.Bb/width)/(self.sm.yView/height), 1)))

        return self.BastLine, self.VE_val, \
               self.channelBodyPatchCollection, self.activeChannelPatchCollection

