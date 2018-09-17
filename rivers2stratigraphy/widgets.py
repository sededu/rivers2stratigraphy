"""
module to provide customized versions of the matplotlib widgets
"""

import numpy as np
from matplotlib.widgets import AxesWidget
from matplotlib.patches import Circle
import six

class MinMaxSlider(AxesWidget):
    """
    A slider representing a floating point range.
    Create a slider from *valmin* to *valmax* in axes *ax*. For the slider to
    remain responsive you must maintain a reference to it. Call
    :meth:`on_changed` to connect to the slider event.
    Attributes
    ----------
    val : float
        Slider value.
    """
    def __init__(self, ax, label, valmin, valmax, valinit=0.5, valfmt='%1.2f',
                 closedmin=True, closedmax=True, slidermin=None,
                 slidermax=None, dragging=True, valstep=None, **kwargs):
        """
        Parameters
        ----------
        ax : Axes
            The Axes to put the slider in.
        label : str
            Slider label.
        valmin : float
            The minimum value of the slider.
        valmax : float
            The maximum value of the slider.
        valinit : float, optional, default: 0.5
            The slider initial position.
        valfmt : str, optional, default: "%1.2f"
            Used to format the slider value, fprint format string.
        closedmin : bool, optional, default: True
            Indicate whether the slider interval is closed on the bottom.
        closedmax : bool, optional, default: True
            Indicate whether the slider interval is closed on the top.
        slidermin : Slider, optional, default: None
            Do not allow the current slider to have a value less than
            the value of the Slider `slidermin`.
        slidermax : Slider, optional, default: None
            Do not allow the current slider to have a value greater than
            the value of the Slider `slidermax`.
        dragging : bool, optional, default: True
            If True the slider can be dragged by the mouse.
        valstep : float, optional, default: None
            If given, the slider will snap to multiples of `valstep`.
        Notes
        -----
        Additional kwargs are passed on to ``self.poly`` which is the
        :class:`~matplotlib.patches.Rectangle` that draws the slider
        knob.  See the :class:`~matplotlib.patches.Rectangle` documentation for
        valid property names (e.g., `facecolor`, `edgecolor`, `alpha`).
        """
        AxesWidget.__init__(self, ax)

        if slidermin is not None and not hasattr(slidermin, 'val'):
            raise ValueError("Argument slidermin ({}) has no 'val'"
                             .format(type(slidermin)))
        if slidermax is not None and not hasattr(slidermax, 'val'):
            raise ValueError("Argument slidermax ({}) has no 'val'"
                             .format(type(slidermax)))
        self.closedmin = closedmin
        self.closedmax = closedmax
        self.slidermin = slidermin
        self.slidermax = slidermax
        self.drag_active = False
        self.valmin = valmin
        self.valmax = valmax
        self.valstep = valstep
        valinit = self._value_in_bounds(valinit)
        if valinit is None:
            valinit = valmin
        self.val = valinit
        self.valinit = valinit
        self.poly = ax.axvspan(valmin, valinit, 0, 1, **kwargs)
        self.vline = ax.axvline(valinit, 0, 1, color='r', lw=1)

        self.valfmt = valfmt
        ax.set_yticks([])
        ax.set_xlim((valmin, valmax))
        ax.set_xticks([])
        ax.set_navigate(False)

        self.connect_event('button_press_event', self._update)
        self.connect_event('button_release_event', self._update)
        if dragging:
            self.connect_event('motion_notify_event', self._update)
        self.label = ax.text(0.5, -0.5, label, transform=ax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='center')
        self.mintext = ax.text(-0.02, 0.5, valfmt % valmin,
                               transform=ax.transAxes,
                               verticalalignment='center',
                               horizontalalignment='right')
        self.maxtext = ax.text(1.02, 0.5, valfmt % valmax,
                               transform=ax.transAxes,
                               verticalalignment='center',
                               horizontalalignment='left')
        self.valtext = ax.text(0.5, 0.45, valfmt % valinit,
                               transform=ax.transAxes,
                               verticalalignment='center',
                               horizontalalignment='center',
                               weight='bold')

        self.cnt = 0
        self.observers = {}

        self.set_val(valinit)

    def _value_in_bounds(self, val):
        """ Makes sure self.val is with given bounds."""
        if self.valstep:
            val = np.round((val - self.valmin)/self.valstep)*self.valstep
            val += self.valmin

        if val <= self.valmin:
            if not self.closedmin:
                return
            val = self.valmin
        elif val >= self.valmax:
            if not self.closedmax:
                return
            val = self.valmax

        if self.slidermin is not None and val <= self.slidermin.val:
            if not self.closedmin:
                return
            val = self.slidermin.val

        if self.slidermax is not None and val >= self.slidermax.val:
            if not self.closedmax:
                return
            val = self.slidermax.val
        return val

    def _update(self, event):
        """update the slider position"""
        if self.ignore(event):
            return

        if event.button != 1:
            return

        if event.name == 'button_press_event' and event.inaxes == self.ax:
            self.drag_active = True
            event.canvas.grab_mouse(self.ax)

        if not self.drag_active:
            return

        elif ((event.name == 'button_release_event') or
              (event.name == 'button_press_event' and
               event.inaxes != self.ax)):
            self.drag_active = False
            event.canvas.release_mouse(self.ax)
            return
        val = self._value_in_bounds(event.xdata)
        if (val is not None) and (val != self.val):
            self.set_val(val)

    def set_val(self, val):
        """
        Set slider value to *val*
        Parameters
        ----------
        val : float
        """
        xy = self.poly.xy
        xy[2] = val, 1
        xy[3] = val, 0
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % val)
        if self.drawon:
            self.ax.figure.canvas.draw_idle()
            # stratcanv = fig.canvas.copy_from_bbox(ax.bbox)
            # fig.canvas.restore_region(stratcanv)
        self.val = val
        if not self.eventson:
            return
        for cid, func in six.iteritems(self.observers):
            func(val)

    def on_changed(self, func):
        """
        When the slider value is changed call *func* with the new
        slider value
        Parameters
        ----------
        func : callable
            Function to call when slider is changed.
            The function must accept a single float as its arguments.
        Returns
        -------
        cid : int
            Connection id (which can be used to disconnect *func*)
        """
        cid = self.cnt
        self.observers[cid] = func
        self.cnt += 1
        return cid

    def disconnect(self, cid):
        """
        Remove the observer with connection id *cid*
        Parameters
        ----------
        cid : int
            Connection id of the observer to be removed
        """
        try:
            del self.observers[cid]
        except KeyError:
            pass

    def reset(self):
        """Reset the slider to the initial value"""
        if (self.val != self.valinit):
            self.set_val(self.valinit)


class NoDrawButton(AxesWidget):
    """
    A GUI neutral button.
    For the button to remain responsive you must keep a reference to it.
    Call :meth:`on_clicked` to connect to the button.
    Attributes
    ----------
    ax :
        The :class:`matplotlib.axes.Axes` the button renders into.
    label :
        A :class:`matplotlib.text.Text` instance.
    color :
        The color of the button when not hovering.
    hovercolor :
        The color of the button when hovering.
    """

    def __init__(self, ax, label, image=None,
                 color='0.85', hovercolor='0.95'):
        """
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The :class:`matplotlib.axes.Axes` instance the button
            will be placed into.
        label : str
            The button text. Accepts string.
        image : array, mpl image, Pillow Image
            The image to place in the button, if not *None*.
            Can be any legal arg to imshow (numpy array,
            matplotlib Image instance, or Pillow Image).
        color : color
            The color of the button when not activated
        hovercolor : color
            The color of the button when the mouse is over it
        """
        AxesWidget.__init__(self, ax)

        if image is not None:
            ax.imshow(image)
        self.label = ax.text(0.5, 0.5, label,
                             verticalalignment='center',
                             horizontalalignment='center',
                             transform=ax.transAxes)

        self.cnt = 0
        self.observers = {}

        self.connect_event('button_press_event', self._click)
        self.connect_event('button_release_event', self._release)
        # self.connect_event('motion_notify_event', self._motion)
        ax.set_navigate(False)
        ax.set_facecolor(color)
        ax.set_xticks([])
        ax.set_yticks([])
        self.color = color
        self.hovercolor = hovercolor

        self._lastcolor = color

    def _click(self, event):
        if self.ignore(event):
            return
        if event.inaxes != self.ax:
            return
        if not self.eventson:
            return
        if event.canvas.mouse_grabber != self.ax:
            event.canvas.grab_mouse(self.ax)

    def _release(self, event):
        if self.ignore(event):
            return
        if event.canvas.mouse_grabber != self.ax:
            return
        event.canvas.release_mouse(self.ax)
        if not self.eventson:
            return
        if event.inaxes != self.ax:
            return
        for cid, func in self.observers.items():
            func(event)

    # def _motion(self, event):
        # if self.ignore(event):
        #     return
        # if event.inaxes == self.ax:
        #     c = self.hovercolor
        #     return
        # else:
        #     c = self.color
        # if c != self._lastcolor:
        #     self.ax.set_facecolor(c)
        #     self._lastcolor = c
        #     if self.drawon:
        #         self.ax.figure.canvas.draw()

    def on_clicked(self, func):
        """
        When the button is clicked, call this *func* with event.
        A connection id is returned. It can be used to disconnect
        the button from its callback.
        """
        cid = self.cnt
        self.observers[cid] = func
        self.cnt += 1
        return cid

    def disconnect(self, cid):
        """remove the observer with connection id *cid*"""
        try:
            del self.observers[cid]
        except KeyError:
            pass


class RadioButtons(AxesWidget):
    """
    A GUI neutral radio button.
    For the buttons to remain responsive
    you must keep a reference to this object.
    The following attributes are exposed:
     *ax*
        The :class:`matplotlib.axes.Axes` instance the buttons are in
     *activecolor*
        The color of the button when clicked
     *labels*
        A list of :class:`matplotlib.text.Text` instances
     *circles*
        A list of :class:`matplotlib.patches.Circle` instances
     *value_selected*
        A string listing the current value selected
    Connect to the RadioButtons with the :meth:`on_clicked` method
    """
    def __init__(self, ax, labels, active=0, activecolor='blue'):
        """
        Add radio buttons to :class:`matplotlib.axes.Axes` instance *ax*
        *labels*
            A len(buttons) list of labels as strings
        *active*
            The index into labels for the button that is active
        *activecolor*
            The color of the button when clicked
        """
        AxesWidget.__init__(self, ax)
        self.activecolor = activecolor
        self.value_selected = None

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)
        dy = 1. / (len(labels) + 1)
        ys = np.linspace(1 - dy, dy, len(labels))
        cnt = 0
        axcolor = ax.get_facecolor()

        # scale the radius of the circle with the spacing between each one
        circle_radius = (dy / 2) - 0.01

        # defaul to hard-coded value if the radius becomes too large
        if(circle_radius > 0.05):
            circle_radius = 0.05

        self.labels = []
        self.circles = []
        for y, label in zip(ys, labels):
            t = ax.text(0.25, y, label, transform=ax.transAxes,
                        horizontalalignment='left',
                        verticalalignment='center')

            if cnt == active:
                self.value_selected = label
                facecolor = activecolor
            else:
                facecolor = axcolor

            p = Circle(xy=(0.15, y), radius=circle_radius, edgecolor='black',
                       facecolor=facecolor, transform=ax.transAxes)

            self.labels.append(t)
            self.circles.append(p)
            ax.add_patch(p)
            cnt += 1

        self.connect_event('button_press_event', self._clicked)

        self.cnt = 0
        self.observers = {}

    def _clicked(self, event):
        if self.ignore(event) or event.button != 1 or event.inaxes != self.ax:
            return
        xy = self.ax.transAxes.inverted().transform_point((event.x, event.y))
        pclicked = np.array([xy[0], xy[1]])
        for i, (p, t) in enumerate(zip(self.circles, self.labels)):
            if (t.get_window_extent().contains(event.x, event.y)
                    or np.linalg.norm(pclicked - p.center) < p.radius):
                self.set_active(i)
                break

    def set_active(self, index):
        """
        Trigger which radio button to make active.
        *index* is an index into the original label list
            that this object was constructed with.
            Raise ValueError if the index is invalid.
        Callbacks will be triggered if :attr:`eventson` is True.
        """
        if 0 > index >= len(self.labels):
            raise ValueError("Invalid RadioButton index: %d" % index)

        self.value_selected = self.labels[index].get_text()

        for i, p in enumerate(self.circles):
            if i == index:
                color = self.activecolor
            else:
                color = self.ax.get_facecolor()
            p.set_facecolor(color)

        if self.drawon:
            self.ax.figure.canvas.draw()

        if not self.eventson:
            return
        for cid, func in self.observers.items():
            func(self.labels[index].get_text())

    def on_clicked(self, func):
        """
        When the button is clicked, call *func* with button label
        A connection id is returned which can be used to disconnect
        """
        cid = self.cnt
        self.observers[cid] = func
        self.cnt += 1
        return cid

    def disconnect(self, cid):
        """remove the observer with connection id *cid*"""
        try:
            del self.observers[cid]
        except KeyError:
            pass
