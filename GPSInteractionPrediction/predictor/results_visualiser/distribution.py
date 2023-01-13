import os
import matplotlib.pyplot as plt
import numpy as np


def visualize_sub_trajectory_count(number_sub_trajectory_distribution_per_bool_interaction, save_dir, y_max):
    print(save_dir)
    for interaction_bool in number_sub_trajectory_distribution_per_bool_interaction.keys():
        number_sub_trajectory_distribution_per_segmentation_method = number_sub_trajectory_distribution_per_bool_interaction[interaction_bool]
        print(number_sub_trajectory_distribution_per_segmentation_method)
        for method in number_sub_trajectory_distribution_per_segmentation_method.keys():
            distribution = number_sub_trajectory_distribution_per_segmentation_method[method]
            filename = str(interaction_bool) + "_" + str(method)
            plot_distribution(distribution, y_max, filename, save_dir)


def plot_distribution(distribution, y_max, filename, directory=".\\temp\\distribution\\"):
    directory += "distribution\\"
    if not os.path.exists(directory):
        os.mkdir(directory)

    fig, ax = plt.subplots()

    print(distribution)

    min_number_dist = min(distribution)
    max_numb_dist = max(distribution)

    tick_list = np.arange(start=min_number_dist, stop=max_numb_dist+3)

    ax.hist(distribution, bins=tick_list)

    plt.xticks(ticks=tick_list-0.5, labels=tick_list-1)
    ax.set_ylabel("Occurences")
    ax.set_xlabel("Number of subtrajectories")
    ax.set_ylim(top=y_max)
    plt.savefig(directory + filename)
    plt.close(fig)
