import numpy as np

class Point:

    def __init__(self, coord = [0, 0, 1], name = 'point'):
        self.name = name
        self.coord = np.array(coord)

    def to(self, point):
        return Point(point.cords - self.cords)

    def __str__(self):
        return '%s: %s' % (self.name, self.coord)

    @staticmethod
    def are_colinear(a, b, c):
        return np.dot(a.coord, np.cross(b.coord, c.coord)) == 0

    @staticmethod
    def averagePoint(points):
        avg = Point('avg', [0., 0., 0.])

        for point in points:
            avg.coord += point.coord
        avg.coord /= len(points)

        return avg

    def set_coord(self, array):
        self.coord = np.array(array)

    def set_name(self, name):
        self.name = name



