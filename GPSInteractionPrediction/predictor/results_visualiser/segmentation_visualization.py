import os
import matplotlib.pyplot as plt


def single_trajectory_sub_trajectory_segmentation_visualisation(sub_trajectories, file_id, save_dir, method, dir_name="segmentation"):
    for trajectory_id in sub_trajectories.keys():
        new_file_id = file_id + "_" + trajectory_id

        trajectory = sub_trajectories[trajectory_id]
        print(save_dir)
        file_path = save_dir + dir_name + "\\" + method + "\\"
        print(file_path)
        plot_single_trajectory(trajectory, new_file_id, file_path)


def multi_trajectory_sub_trajectory_segmentation_visualisation(trajectories, save_dir, prefix= "", colors = ["r", "b"]):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    fig, ax = plt.subplots()
    for trajectory_id in trajectories.keys():
        trajectory_id = trajectory_id
        color = colors[int(trajectory_id)]
        sub_trajectories = trajectories[trajectory_id]
        add_sub_trajectories_to_segmentation_plot(sub_trajectories, color, fig, ax)

    save_file_path = save_dir + prefix + "_trajectories_segmentation"

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.ticklabel_format(useOffset=False)
    plt.tight_layout()
    plt.savefig(save_file_path)
    plt.close()


def plot_single_trajectory(trajectory, file_id, save_dir, postfix="segmentation_plot"):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    fig, ax = plt.subplots()

    all_x = trajectory['0']
    all_y = trajectory['1']

    for i in range(len(all_x)):
        xs_sub_trajectory = all_x[i]
        ys_sub_trajectory = all_y[i]
        ax.plot(ys_sub_trajectory, xs_sub_trajectory)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.ticklabel_format(useOffset=False)
    plt.tight_layout()
    plt.savefig(save_dir+file_id+"_"+postfix)
    plt.close(fig)


def add_sub_trajectories_to_segmentation_plot(sub_trajectories, color, fig, ax):
    all_x = sub_trajectories[0]
    all_y = sub_trajectories[1]
    for sub_trajectory_id in range(len(all_x)):
        ys_sub_trajectory = all_x[sub_trajectory_id]
        xs_sub_trajectory = all_y[sub_trajectory_id]

        ax.plot(ys_sub_trajectory, xs_sub_trajectory, color)