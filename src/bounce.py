import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.widgets as widget

def simData():
    t_max = 10.0
    dt = 0.05
    x = 0.0
    t = 0.0
    while t < t_max:
        x = np.sin(np.pi*t)
        t = t + dt
        yield x, t


def pause_anim(event):
    if ani.running:
        ani.event_source.stop()
    else:
        ani.event_source.start()
    ani.running ^= True

def simPoints(simData):
    x, t = simData[0], simData[1]
    time_text.set_text(time_template%(t))
    line.set_data(t, x)
    return line, time_text

fig = plt.figure()
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.085, bottom=0.1, top=0.95, right=0.5)
line, = ax.plot([], [], 'bo', ms=10)
ax.set_ylim(-1, 1)
ax.set_xlim(0, 10)

btn_pause_ax = plt.axes([0.565, 0.03, 0.2, 0.04])
btn_pause = widget.Button(btn_pause_ax, 'Pause')
btn_pause.on_clicked(pause_anim)

time_template = 'Time = %.1f s'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
# fig.canvas.mpl_connect('button_press_event', onClick)
ani = animation.FuncAnimation(fig, simPoints, simData, blit=False, interval=10,
    repeat=True)
ani.running = True
plt.show()