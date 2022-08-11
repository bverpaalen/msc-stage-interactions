import matplotlib.pyplot as plt
import os

colors = ["red", "blue"]


def time_space_figure(trajectories, save_dir, prefix, has_subs=True):
    save_name = prefix + "_time_space"
    time_space_dir = save_dir + "real_time_space\\"

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    if not os.path.exists(time_space_dir):
        os.mkdir(time_space_dir)

    fig, ax = plt.subplots()
    for trajectory_id in trajectories.keys():
        trajectory = trajectories[trajectory_id]
        space_time_data = sum_longitude_with_latitude(trajectory, has_subs)
        color = colors[int(trajectory_id)]

        add_data_to_plot(space_time_data, ax, color)

    ax.set_ylabel("Location")
    ax.set_xlabel("Time")
    ax.ticklabel_format(useOffset=False)

    plt.tight_layout()
    plt.savefig(time_space_dir+save_name)
    plt.close(fig)


def sum_longitude_with_latitude(trajectory, has_subs):
    latitude = trajectory[0]
    longitude = trajectory[1]

    space = []
    if has_subs:
        for sub_trajectory_id in range(len(latitude)):
            sub_latitude = latitude[sub_trajectory_id]
            sub_longitude = longitude[sub_trajectory_id]

            sub_space = []
            for point_id in range(len(sub_latitude)):
                point_latitude = sub_latitude[point_id]
                point_longitude = sub_longitude[point_id]
                sum_space = point_latitude + point_longitude
                sub_space.append(sum_space)
            space.append(sub_space)
    else:

        sub_space = []
        for point_id in range(len(latitude)):
            point_latitude = latitude[point_id]
            point_longitude = longitude[point_id]
            sum_space = point_latitude + point_longitude
            sub_space.append(sum_space)
        space.append(sub_space)
    return space


def add_data_to_plot(trajectory, ax, color="red"):
    old_x = 0
    for sub_trajectory in trajectory:
        x = old_x + len(sub_trajectory)
        range_x = list(range(old_x,x))
        ax.plot(range_x, sub_trajectory, color)
        old_x = x