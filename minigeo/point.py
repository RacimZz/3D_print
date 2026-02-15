from math import sqrt, cos, sin, atan2, pi
from random import random


def point_aleatoire():
    return (random(), random())


def distance_carree(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    xdiff = x2 - x1
    ydiff = y2 - y1
    return xdiff * xdiff + ydiff * ydiff


def code_svg(point):
    x, y = point
    return f"<circle cx='{x}' cy='{y}' r='1%'/>"


def angle(self, autre):
    angle_brut = -atan2(*reversed(moins(autre, self)))
    if angle_brut <= 0.0:
        angle_brut += 2 * pi
    return angle_brut


def mise_a_jour_dimensions(dimensions, point):
    xmin, xmax, ymin, ymax = dimensions
    x, y = point
    return (min(xmin, x), max(xmax, x), min(ymin, y), max(ymax, y))


def distance(p1, p2):
    return sqrt(distance_carree(p1, p2))


def rotation(point, angle):
    x, y = point
    cosinus = cos(-angle)
    sinus = sin(-angle)
    return (cosinus * x - sinus * y, sinus * x + cosinus * y)


def moins(u, v):
    return tuple(cu - cv for cu, cv in zip(u, v))


def plus(u, v):
    return tuple(cu + cv for cu, cv in zip(u, v))


def fois(u, f):
    return tuple(cu * f for cu in u)
