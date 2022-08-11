import shapes
from converters import degree

from circle_point_selection import edge_point_selection as eps

testCircle = shapes.Circle()
points = list(range(0, 360))

for i in range(1,50):
    print(i)
    results = eps.x_potential_points(points, i)
    print(results)
    for result in results:
        print(degree.degree_to_xy(result, testCircle))
    print()