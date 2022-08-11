import math, copy
from scipy.spatial import distance


def best_n_point_selection(circle, compare_point_a, compare_point_b, n=5):
    best_distance = -math.inf
    furthest_point = None
    points = []

    for i in range(n):
        points.append(circle.random_point_in_circle())

    for point in points:
        cur_distance_a = distance.euclidean(point, compare_point_a)
        cur_distance_b = distance.euclidean(point, compare_point_b)

        abs_avg_cur_distance = (abs(cur_distance_a) + abs(cur_distance_b)) / 2

        if abs_avg_cur_distance > best_distance:
            best_distance = copy.deepcopy(abs_avg_cur_distance)
            furthest_point = point
    return furthest_point
