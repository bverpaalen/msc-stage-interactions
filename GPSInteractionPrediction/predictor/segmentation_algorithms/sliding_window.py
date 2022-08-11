def run(trajectories, length=5):
    per_trajectory_sub_trajectories = {}
    i = 0
    for trajectory in trajectories:
        sub_trajectories = split_trajectory(trajectory, length)
        per_trajectory_sub_trajectories.update({i: sub_trajectories})
        i += 1
    return per_trajectory_sub_trajectories


def split_trajectory(trajectory, length):
    sub_trajectories = []
    for sub_i in range(len(trajectory)+1-length):
        sub_trajectory = trajectory[sub_i:sub_i+length]
        sub_trajectories.append(sub_trajectory)
    return sub_trajectories
