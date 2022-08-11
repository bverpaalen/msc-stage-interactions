import os
from matplotlib import pyplot as plt


def run(trajectories, save_dir, prefix):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    save_dir += "normal_trajectories\\"

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    file_path = save_dir + prefix + "_logged_data.png"
    fig, ax = plt.subplots()

    for trajectory_id in trajectories.keys():
        trajectory = trajectories[trajectory_id]
        add_trajectory_to_map(trajectory, ax)
    ax.ticklabel_format(useOffset=False)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close(fig)


def add_trajectory_to_map(trajectory, ax):
    longitude = trajectory[0]
    latitude = trajectory[1]

    ax.plot(longitude, latitude)