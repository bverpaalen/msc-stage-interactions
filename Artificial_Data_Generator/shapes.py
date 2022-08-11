import random
from scipy.spatial import distance


class Circle:

    # len can be diameter or radius, if r=1 len is radius otherwise len is diameter
    # Calculates the origin point for the circle, x and y given are at the left middle side of the circle often seen as the starting point
    def __init__(self, origin_x=0, origin_y=0, length=1, r=1):
        if r:
            self.radius = length
        else:
            self.radius = length / 2
        self.originY = origin_x
        self.originX = origin_y
        self.degrees = list(range(360))

    def random_point_in_circle(self):
        random_x = self.originX + self.radius + 1
        random_y = self.originY + self.radius + 1

        random_point = (random_x, random_y)
        origin = (self.originX, self.originY)

        while abs(distance.euclidean(random_point, origin)) > abs(self.radius):
            random_x = random.uniform(self.originX - self.radius, self.originX + self.radius)
            random_y = random.uniform(self.originY - self.radius, self.originX + self.radius)
            random_point = (random_x, random_y)

        return random_point
