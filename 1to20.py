import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
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
counter = 1
ring = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11,
        14, 9, 12, 5]  # Number Ring
MAX_DARTS = 60
score = np.zeros([21, 3])
hits = np.zeros([MAX_DARTS, 4])

def increase_counter():
    # increases darts counter and finishes game after 60 darts
    global counter
    counter += 1
    if counter > MAX_DARTS:
        print_statistics()


def draw_dartboard():
    # Draws a dartboard shape in the graph
    c0 = Circle((0, 0), rt, color='black', alpha=0.2)
    c1 = Circle((0, 0), ro, color='blue', alpha=0.2)
    c2 = Circle((0, 0), ro - rw, color='white')
    c3 = Circle((0, 0), ri, color='blue', alpha=0.2)
    c4 = Circle((0, 0), ri - rw, color='white')
    c5 = Circle((0, 0), rb, color='blue', alpha=0.2)
    c6 = Circle((0, 0), rb - rw, color='C2', alpha=0.5)
    for circle in [c0, c1, c2, c3, c4, c5, c6]:
        ax.add_patch(circle)
    # plt.axis('equal')
    # Display the number ring
    for i in range(20):
        plt.text(190 * np.sin(labels[i]),
                 190 * np.cos(labels[i]),
                 ring[i],
                 ha="center",
                 va="center",
                 rotation=-(i) / 20 * 360)
        plt.plot(
            [rb * np.sin(labels[i] + offset), rt * np.sin(labels[i] + offset)],
            [rb * np.cos(labels[i] + offset), rt * np.cos(labels[i] + offset)],
            'k-',
            linewidth='0.5')


def onclick(event):
    # Checks where the dart landed, draws a point on the map
    # and evaluates score
    x = event.xdata
    y = event.ydata
    global counter

    hits[counter-1, 0] = x
    hits[counter-1, 1] = y
    sec = (int)(np.ceil(counter / 3))
    rad = np.sqrt(x**2 + y**2)
    if (rad < ro):
        # Dart landed inside scoring area
        if (rad < rw):
            # Double Bull
            #print("hit double bull!")
            plt.plot(x, y, 'xk')
            score[20, 1] += 1
        elif (rad < rb):
            # Single bull
            #print("hit single bull!")
            score[20, 0] += 1
            plt.plot(x, y, 'xk')
        else:
            # check if the correct segment was hit
            arctan = (90 - np.arctan2(y, x) * 360 /
                      (2 * np.pi)) % 360  # calculates the angle of the dart
            offset = (labels[2] - labels[1]) * 360 / (2 * np.pi)
            expected = (ring.index(sec)) * 18  # Allowed angles
            if arctan > expected - offset / 2 and arctan < expected + offset / 2:
                print("hit!")
                hits[counter-1,2] = 1
                plt.plot(x, y, 'xg')
                if is_double(rad):
                    score[sec - 1, 1] += 1
                elif is_triple(rad):
                    score[sec - 1, 2] += 1
                else:
                    score[sec - 1, 0] += 1
            else:
                #Wrong Segment hit
                hits[counter-1, 2] = 0
                plt.plot(x, y, 'xr')
    else:
        #Dart landed outside the scoring area
        plt.plot(x, y, 'xr')

    hits[counter-1, 3] = np.datetime64('today')
    increase_counter()
    fig.canvas.draw()
    if (counter % 3 == 1):
        print("SECTOR ", (int)(np.ceil((counter) / 3)) )


""" Can Maybe be used lated on
def which_segment(x,y):
    arctan = (90 - np.arctan2(y, x) * 360 / (2 * np.pi)) % 360
    offset = (labels[2] - labels[1]) * 360 / (2 * np.pi)

    for val in ring:
        expected = ring.index(val)*18
        if arctan > expected - offset/2 and arctan < expected + offset/2:
            #print("hit sector ", val)
            pass
"""


def is_triple(rad):
    return rad < ri and rad > (ri - rw)


def is_double(rad):
    return rad < ro and rad > (ro - rw)


def print_statistics():
    # TODO: Add statistics to file
    # Prints statistics and saves chart
    filename = str(date.today())
    #plt.savefig(filename)
    print("Reached End, saved plot in ", filename)
    print("Overview :")
    print_array(score)
    with open("data.csv", "a") as myfile:
        csvfile = csv.writer(myfile, delimiter=',')
        csvfile.writerows(hits)
        myfile.close()
        print("wrote to file")
    plt.close()


def print_array(array):
    # For every field this array stores three values
    # [single, double, triple] hits
    for i in range(len(array)):
        sum = array[i, 0] + array[i, 1] + array[i, 2]
        print("Field ", i + 1, "\t single ", int(array[i, 0]), "\t double ",
              int(array[i, 1]), "\t triple ", int(array[i, 2]), "\t total ",
              int(sum))


# PROGRAM STARTS HERE
print("3 darts on every sector from 1 to 20. \n All hits count the same")
print("SECTOR 1: ")
# Graph Cosmetics
fig = plt.figure(facecolor='lightgray', figsize=(8, 8))
plt.axis('off')
ax = fig.add_subplot(111)
# Draw dartboard and wait for Mouse Intercation
draw_dartboard()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.title("Progress " + str(date.today()))
plt.show()
