import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from point import Point

#------------------------------------------------------------------------------
def are_coplanar(a, b, c):
    return np.dot(a, np.cross(b, c)) == 0;
#------------------------------------------------------------------------------
# Nije zavrseno
def plot_line(p1, p2, axis):
    axis

#------------------------------------------------------------------------------
def plot_grid(minX, maxX, minY, maxY, density, axis = plt):
    left = int(min(minX, minY))
    size = int(max(maxX - minX, maxY - minY))

    # Broj cvorova ose
    nodes = int(size / density) + 1
    grid = np.linspace(left, size, nodes)

    for i in range(nodes):
        axis.plot(grid, np.repeat(grid[i], nodes), 'c-')
        axis.plot(np.repeat(grid[i], nodes), grid, 'c-')
#------------------------------------------------------------------------------
# Ideja sa manje parametara
'''
def plot_grid(axs, density, axis = plt, transform = []):
    plot_grid(axs.get_xlim, axs.get_ylim, density, axis , transform)
'''
#------------------------------------------------------------------------------
def adjust_to_points(axis, points, aspect = 'equal'):
    x = points[:,0]
    y = points[:,1]

    xMin, xMax = min(x), max(x)
    yMin, yMax = min(y), max(y)

    xRange = xMax - xMin
    yRange = yMax - yMin

    # Rastojanje najdalje tacke od ivice canvasa
    maxRange = xRange if xRange > yRange else yRange
    padding = maxRange * 0.1 
    
    # Postavljanje granica i razmera osa
    axis.set_xlim([xMin - padding, xMax + padding])
    axis.set_ylim([yMin - padding, yMax + padding])
    axis.set_aspect(aspect, adjustable='box')
#------------------------------------------------------------------------------
def transform_points(points, transform):
    return np.array([transform @ np.transpose(x) for x in points])
#------------------------------------------------------------------------------


def main():
    # Kreiranje plotova
    fig, (axisIn, axisOut) = plt.subplots(1,2)

    # Naslovi
    axisIn.set_title("Input")
    axisOut.set_title("Output")

    
    # Podrazumevane tacke
    inputPoints = np.array([[1, 4, 1], 
                            [1, 3, 1], 
                            [2, 4, 1], 
                            [3, 2, 1]])

    # Matrica preslikavanja
    matrixTransform = np.array([[1, 3, 5],
                                [2, 2, 4],
                                [1, 4, 3]])
    
    # Slike tacaka
    outputPoints = transform_points(inputPoints, matrixTransform)

    pointNum = 4
    pointNames = 'ABCD'

    # Ucitavanje tacaka sa standardnog ulaza
    if len(sys.argv) > 1:
        if sys.argv[1] == '-i':
            print('Unesite 4 tacke u formatu: x y')
            for i in range(pointNum):
                inputPoints[i][0], inputPoints[i][1] = map(
                        float, 
                        input('%s) ' % pointNames[i]).strip().split(' '))


    points = [Point(coord, name) for coord, name in zip(inputPoints, pointNames)]
    
    # Prilagodjavanje granica osa u odnosu na tacke 
    adjust_to_points(axisIn, inputPoints)
    adjust_to_points(axisOut, outputPoints)

    # Iscrtavanje mreze
    density = 1
    plot_grid(0, 6, 0, 6, density, axisIn)
    plot_grid(0, 20, 0, 20, density, axisOut)

    # Iscrtavanje ulaznih tacaka
    axisIn.plot(inputPoints[:,0], inputPoints[:,1], 'ro')

    # Iscrtavanje izlaznih tacaka
    axisOut.plot(outputPoints[:,0], outputPoints[:,1], 'ro')

    for i in range(4):
        # Neuredjene trojke
        k = [k for k in range(4) if k != i]
        if Point.are_colinear(points[k[0]], points[k[1]], points[k[2]]):
            print('Tacke %s su kolinearne' % [points[x].name for x in j])
            # iscrtati liniju

    plt.show()

      
if __name__ == "__main__":
    main()
