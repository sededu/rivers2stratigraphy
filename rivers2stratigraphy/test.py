import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anm
import matplotlib.collections as clt

fig, ax = plt.subplots(1,1,figsize=(7,7))

ax.set_xlim(-1,1)
ax.set_ylim(-1,1)

n_of_particles = 30
frames = 10

radius = 0.05
x = 0.5*np.random.randn(frames,n_of_particles)
y = 0.5*np.random.randn(frames,n_of_particles)
z = 0.5*np.random.randn(frames,n_of_particles)

patches = []
for p in range(n_of_particles):
    circle = plt.Circle((x[0,p], y[0,p]), radius)
    patches.append(circle)

collection = clt.PatchCollection(patches, cmap=plt.cm.jet, alpha=0.4)
collection.set_array(z[0,:])
collection.set_clim([-1, 1])
fig.colorbar(collection)

ax.add_collection(collection)

def animate(frame):
    patches = []
    for p in range(n_of_particles):
        circle = plt.Circle((x[frame,p], y[frame,p]), radius)
        patches.append(circle)

    print(patches, '\n')

    collection.set_paths(patches)
    collection.set_array(z[frame,:])

anim = anm.FuncAnimation(fig, animate,
                               frames=10, interval=100, blit=False)
plt.show()