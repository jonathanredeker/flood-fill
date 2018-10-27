"""
The purpose of this file is to aid debugging of the 3D Flood Fill.
"""
import json
import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator

# Try to load the data from the algorithm, if it fails use dummy data.
try:
    with open("flood_fill_3d.json", "r") as file:
        file.seek(0)
        data = file.readline()
    data = json.loads(data)
except:
    data = {"map": [[[0,0],[0,0]],[[0,0],[0,0]]], "path": []}

# Get the dimensions of the map.
length = len(data["map"][0][0])
width = len(data["map"][0])
height = len(data["map"])

# Create an empty map for our obstacles based upon the dimensions of our
# collision map.
obstacles = np.zeros((height, width, length), dtype=int)

x = []
y = []
z = []

# Split and append our path coordinates to three different arrays.
for coordinate in data["path"]:
    z.append(coordinate[2])
    y.append(coordinate[1])
    x.append(coordinate[0])

# Let our obstacle map take on the coordinates of the obstacles.
for dz in range(len(data["map"])):
    for dy in range(len(data["map"][dz])):
        for dx in range(len(data["map"][dz][dy])):
            if data["map"][dz][dy][dx] == 0 or data["map"][dz][dy][dx] == 1:
                obstacles[dz][dy][dx] = data["map"][dz][dy][dx]
            else:
                obstacles[dz][dy][dx] = 0

# Split and append the obstacle coordinates to three different arrays.
z2, y2, x2 = obstacles.nonzero()

# Create our figure for our graph.
figure = plot.figure()

# Create the axis for the model; give it a title.
ax = figure.add_subplot(111, projection='3d', title="Solved Path & Obstacles")
ax.set_xlim(0,length-1)
ax.set_ylim(0,width-1)
ax.set_zlim(0,height-1)

# Configure our axis:
# - Ticks are only integers
# - Label each axis
# - Invert the y-axis
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.zaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xlabel("x", backgroundcolor="black", color="w")
ax.set_ylabel("y", backgroundcolor="black", color="w")
ax.set_zlabel("z", backgroundcolor="black", color="w")
ax.invert_yaxis()

# If there is a path, plot it.
# - Path is blue, connected and marked as dots
# - Initial position is green, marked with a circle
# - Goal is red, marked with an X
if data["path"]:
    ax.plot(x, y, z, c="b", marker=".")
    ax.plot([x[0]], [y[0]], [z[0]], c="g", marker="o")
    ax.plot([x[-1]], [y[-1]], [z[-1]], c="r", marker="X", markersize=8)

# Scatter/plot the obstacles as black squares.
ax.scatter(x2, y2, z2, c="black", marker="s")

# For debugging collision check
#ax.plot_trisurf([2,2,3],[2,3,2],[0,1,1], cmap='Pastel1', edgecolor='none')
#ax.plot_trisurf([2,2,1],[2,1,2],[0,1,1], cmap='summer', edgecolor='none')
#ax.plot_trisurf([2,2,1],[2,3,2],[0,1,1], cmap='Wistia', edgecolor='none')
#ax.plot_trisurf([2,2,3],[2,1,2],[0,1,1], cmap='autumn', edgecolor='none')

# Show the plotted data
plot.show()
