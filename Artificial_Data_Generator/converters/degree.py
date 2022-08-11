import math


def degree_to_xy(degree, circle, rounder=4):
    x = circle.radius * math.sin(math.radians(degree))
    y = circle.radius * math.cos(math.radians(degree))

    x = round(x, rounder)
    y = round(y, rounder)

    return (x,y)