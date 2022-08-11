import copy, math
from scipy.spatial import distance


def simulate_walks(point_a, point_b, meeting_point, walking_steps):
    point_a_to_meeting = abs(distance.euclidean(point_a, meeting_point))
    point_b_to_meeting = abs(distance.euclidean(point_b, meeting_point))
    steps_a_to_meeting, steps_b_to_meeting = calculate_steps(point_a_to_meeting, point_b_to_meeting, walking_steps)

    walk_a = create_walk(point_a, meeting_point, int(steps_a_to_meeting))
    walk_b = create_walk(point_b, meeting_point, int(steps_b_to_meeting))

    walk = merge_walks(walk_a, walk_b)

    first_walk = copy.deepcopy(walk)
    walk.reverse()
    second_walk = walk

    return [first_walk, second_walk]


def calculate_steps(point_a_to_meeting, point_b_to_meeting, walking_steps):
    total = point_a_to_meeting + point_b_to_meeting

    per_a_to_meeting = point_a_to_meeting / total
    per_b_to_meeting = point_b_to_meeting / total

    steps_a_to_meeting = round(per_a_to_meeting * walking_steps)
    steps_b_to_meeting = round(per_b_to_meeting * walking_steps)

    if steps_a_to_meeting + steps_b_to_meeting > walking_steps:
        steps_b_to_meeting -= 1

    return steps_a_to_meeting, steps_b_to_meeting


def create_walk(point, meeting, steps):
    walk = []
    delta_x = meeting[0] - point[0]
    delta_y = meeting[1] - point[1]

    for i_step in range(steps+1):
        x_step = delta_x / steps * i_step + point[0]
        y_step = delta_y / steps * i_step + point[1]
        walk.append((x_step, y_step))
    return walk


def merge_walks(walk_a, walk_b):
    walk_b.reverse()
    walk = walk_a + walk_b[1:]
    return walk


def simulate_meeting(walks, length=1):
    meeting_point, i_before_meeting = middle_point(walks)
    for i in range(len(walks)):
        walk = walks[i]

        if i == 1:
            walk.reverse()
        meeting = [meeting_point] * length

        new_walk = walk[:i_before_meeting]
        new_walk.extend(meeting)
        new_walk.extend(walk[i_before_meeting:])

        if i == 1:
            new_walk.reverse()

        walks[i] = new_walk
    return walks


def middle_point(walks):
    walk_a = walks[0]
    walk_b = walks[1]

    if len(walk_a) % 2 != 0:
        i_before_meeting = math.ceil(len(walk_a) / 2)
        return walk_a[i_before_meeting], i_before_meeting

    else:
        i_before_meeting = int(len(walk_a) / 2)

        point_left = walk_a[i_before_meeting]
        point_right = walk_b[i_before_meeting]

        x_left = point_left[0]
        x_right = point_right[0]
        y_left = point_left[1]
        y_right = point_right[1]

        x_meeting = (x_left + x_right) / 2
        y_meeting = (y_left + y_right) / 2

        return (x_meeting, y_meeting), i_before_meeting
