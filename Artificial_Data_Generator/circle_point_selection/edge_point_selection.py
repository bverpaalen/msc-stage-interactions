import random, copy


def random_points_on_edge(num_points, min_difference=0):


    possible_points = list(range(0, 360))
    point_degrees = []

    for pointToChoose in range(num_points):
        chosen_degree = random.choice(possible_points)
        point_degrees.append(chosen_degree)


# def possiblePointsInDegreeRange(degreeStart, degreeEnd, minDifference=1):
#     if minDifference <= 0:
#         return math.inf
#
#     if degreeStart >= degreeEnd:
#         degreeEnd += 360
#     difference = degreeEnd - degreeStart
#     possiblePoints = difference / minDifference
#     return possiblePoints

# def maxPotentialPoints(possiblePoints, minDifference=0):
#     allChosen = []
#     ranges = allRanges(possiblePoints)
#     for r in ranges:
#         maxPoints = maxPointsInRange(r, minDifference)
#         for iPoint in range(maxPoints):
#
#             chosen = random.choice(r)
#             allChosen.append(copy.deepcopy(chosen))
#
#             newR = removePointBelowDifference(removePointBelowDifference(r,chosen,minDifference))
#             r = copy.deepcopy(newR)
#     print(allChosen)

def x_potential_points(possible_points, min_difference=0, n=2):
    if n * (min_difference * 2 + 1) > 360:
        raise Exception(
            "Number of points and minimal difference are impossible to calculate as sum of minimal distance > degree in circle")

    all_chosen = []

    for i in range(n):
        chosen = random.choice(possible_points)
        all_chosen.append(copy.deepcopy(chosen))
        possible_points = remove_point_below_difference(possible_points, chosen, min_difference)

        if len(possible_points) < 1:
            break
    return all_chosen


def remove_point_below_difference(points, chosen, min_difference):
    new_points = []

    for point in points:
        if not abs(point - chosen) <= min_difference and not abs(360 - (point - chosen)) <= min_difference:
            new_points.append(point)
    return new_points

# def maxPointsInRange(r, minDifference):
#     if minDifference < 1:
#         return len(r)
#
#     pointWidth = 2 * minDifference + 1
#     print(pointWidth)
#
#     points = math.floor(len(r) / pointWidth)
#     return points


# def allRanges(points):
#     start = points[0]
#
#     ranges = []
#     curRange = None
#
#     for i in range(len(points)):
#         point = points[i]
#         if curRange != None:
#             if point == oldPoint + 1:
#                 curRange.append(point)
#                 oldPoint = point
#             elif point == 359 and start == 0:
#                 ranges[0] += curRange
#             else:
#                 ranges.append(copy.deepcopy(curRange))
#                 curRange = [copy.deepcopy(point)]
#                 oldPoint = copy.deepcopy(point)
#         else:
#             oldPoint = points[i]
#             curRange = [oldPoint]
#
#     if len(curRange) > 0:
#         ranges.append(copy.deepcopy(curRange))
#
#     first = None
#     last = None
#
#     index = 0
#     for r in ranges:
#         if 0 in r:
#             first = r
#         elif 359 in r:
#             last = r
#         index += 1
#
#     if first != None and last != None:
#         last += first
#         ranges.remove(first)
#     return ranges
