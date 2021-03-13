import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from matplotlib.patches import Circle

# Constants and global variables
# Measures of the Dartboard
rt = 250  # total board radius
ro = 170  # outer radius
ri = 107  # inner radius
rw = 15  # Radius of Special fields
rb = 2 * rw  # bullseye radius
labels = np.linspace(0, 2 * np.pi, 20, endpoint=False)  # Label Ring
offset = (labels[2] - labels[1]) / 2
ring = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11,
        14, 9, 12, 5]  # Number Ring

# Create data
N = 500
x = np.random.rand(N)
y = np.random.rand(N)
colors = (0,0,0)
area = np.pi*3

def draw_dartboard():
    # Draws a dartboard shape in the graph
    c0 = Circle((0, 0), rt, color='black', alpha=0.2)
    c1 = Circle((0, 0), ro, color='blue', alpha=0.2)
    c2 = Circle((0, 0), ro - rw, color='white')
    c3 = Circle((0, 0), ri, color='blue', alpha=0.2)
    c4 = Circle((0, 0), ri - rw, color='white')
    c5 = Circle((0, 0), rb, color='blue', alpha=0.2)
    c6 = Circle((0, 0), rb - rw, color='C2', alpha=0.5)
    phi = np.linspace(0, 2 * np.pi, 200)
    for r in [ro, ro-rw, ri, ri-rw, 2*rw, rw]:
        ax.plot(r*np.cos(phi), r*np.sin(phi), 'k', linewidth='0.5')

    # Display the number ring
    for i in range(20):
        plt.text(190 * np.sin(labels[i]),
                 190 * np.cos(labels[i]),
                 ring[i],
                 ha="center",
                 va="center",
                 rotation=-(i) / 20 * 360,)
        plt.plot(
            [rb * np.sin(labels[i] + offset), (rt-rb) * np.sin(labels[i] + offset)],
            [rb * np.cos(labels[i] + offset), (rt-rb) * np.cos(labels[i] + offset)],
            'k-', linewidth='0.5')

data = np.genfromtxt('data.csv', delimiter=',', skip_header=1)
#print(data[:,0])
x = data[:,0]
y = data[:,1]

plot_heatmap=True
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set(xticks=[])
ax.set(yticks=[])

if(plot_heatmap):
    samples = data[:,0:2]
    #Extract hits only
    hits = data[np.where(data[:,2])]
    # HEATMAP
    density_func = st.gaussian_kde(samples.T, bw_method=0.2)
    X, Y = np.mgrid[-rt:rt:1000j,-rt:rt:1000j]
    positions = np.stack([X.flat, Y.flat])
    Z = np.reshape(density_func(positions), X.shape)

    heatmap = ax.contourf(X, Y, Z, cmap='Blues')
    ax.contour(X, Y, Z, linewidths=0.1, colors='k')
    ax.set(title="Heatmap of all thrown darts")
    fig.colorbar(heatmap)


#plt.figure(facecolor='lightgray', figsize=(8, 8))
#fig, ax = plt.subplots()
#plt.imshow(data, cmap='hot', interpolation='nearest')
else:
    #SCATTER PLOT
    plt.scatter(x, y, s=area, c=data[:,2], cmap='RdYlGn', marker='x', linewidths=0.5)
draw_dartboard()
plt.show()