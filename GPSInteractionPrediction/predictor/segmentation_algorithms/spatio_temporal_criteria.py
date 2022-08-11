import geopy.distance
import pandas


def run(trajectories, window_range=(-4, 4), speed_difference_threshold=2):
    per_trajectory_sub_trajectories = {}
    i = 0
    for trajectory in trajectories:
        windows = windows_of_trajectory(trajectory, window_range)
        sub_trajectories = []

        old_distance = None
        sub_trajectory = pandas.DataFrame(columns=trajectory.columns)
        for key in windows.keys():
            window = windows[key]
            distance = sum_distance(window)
            if old_distance:
                if abs(old_distance - distance) >= speed_difference_threshold:
                    old_distance = None
                    sub_trajectories.append(sub_trajectory)
                    sub_trajectory = pandas.DataFrame(columns=trajectory.columns)
                else:
                    old_distance = distance
                sub_trajectory = sub_trajectory.append(trajectory.iloc[key], ignore_index=True)
            else:
                sub_trajectory = sub_trajectory.append(trajectory.iloc[key], ignore_index=True)
                old_distance = distance
        sub_trajectories.append(sub_trajectory)
        per_trajectory_sub_trajectories.update({i: sub_trajectories})
        i += 1
    return per_trajectory_sub_trajectories


def windows_of_trajectory(trajectory, window_range):
    relative_start_window = window_range[0]
    relative_end_window = window_range[1]

    windows = {}
    for i in range(len(trajectory)):
        start_window = i + relative_start_window
        end_window = i + relative_end_window

        if start_window >= 0 and end_window < len(trajectory):
            window = trajectory.iloc[start_window:end_window]
            windows.update({i: window})
    return windows


def sum_distance(trajectory):
    sum_distance = 0
    for i in range(len(trajectory)):
        i_point_point = trajectory.iloc[i]
        i_point_cor = i_point_point.get([" Latitude", " Longitude"])
        if i != 0:
            distance = geopy.distance.distance(last_point_cor, i_point_cor).meters
            sum_distance += distance
        last_point_cor = i_point_cor
    rounded_sum_distance = round(sum_distance, 2)
    return rounded_sum_distance

