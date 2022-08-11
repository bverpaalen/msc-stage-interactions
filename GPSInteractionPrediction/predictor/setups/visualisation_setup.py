import working_with_files
import copy
import json
import utilities
from results_visualiser import time_space_figure, segmentation_visualization, distribution
import os

number_sub_trajectory_distribution_per_method = {
    #"sliding_window": [],
    "spatio_temporal_criteria": [],
    "clustering": []
}

number_sub_trajectory_distribution_per_bool_interaction = {
    True: copy.deepcopy(number_sub_trajectory_distribution_per_method),
    False: copy.deepcopy(number_sub_trajectory_distribution_per_method)
}

colors = ["r", "b"]


def main(dir_path, save_dir, max_trajectory_in_files):
    files = working_with_files.get_files(dir_path, ".json")

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    for file in files:
        meta_data = working_with_files.get_metadata(file)
        file_id = meta_data[0]
        has_interaction = meta_data[1]

        data = working_with_files.get_data(file)

        number_sub_trajectory_distribution_per_method, sub_trajectories_per_method = extract_number_of_sub_trajectories_and_sub_trajectories(data)

        utilities.merge_dics(number_sub_trajectory_distribution_per_bool_interaction[has_interaction], number_sub_trajectory_distribution_per_method)
        for method in sub_trajectories_per_method.keys():
            prefix_file = method+str(file_id)+str(has_interaction)
            sub_trajectories = sub_trajectories_per_method[method]
            segmentation_visualization.multi_trajectory_sub_trajectory_segmentation_visualisation(sub_trajectories, save_dir +"multi_segmentation\\", prefix=prefix_file)

            time_space_figure.time_space_figure(sub_trajectories, save_dir, prefix_file)
        color = colors[has_interaction]
        #segmentation_visualization.single_trajectory_sub_trajectory_segmentation_visualisation(sub_trajectories_per_method, str(meta_data[0]) + "_" + str(meta_data[1]), method, color, save_dir)


    distribution.visualize_sub_trajectory_count(number_sub_trajectory_distribution_per_bool_interaction, save_dir, max_trajectory_in_files)


def extract_number_of_sub_trajectories_and_sub_trajectories(data):
    number_sub_trajectory_distribution_per_bool_interaction = {}
    sub_trajectories = {}

    for method in data.keys():
        if method != "sliding_window":
            sub_trajectories.update({method: {}})

        number_sub_trajectories_of_trajectory = []
        for trajectory_id in data[method].keys():
            sub_trajectories_for_trajectory = data[method][trajectory_id]

            amount_of_trajectories = len(sub_trajectories_for_trajectory)
            number_sub_trajectories_of_trajectory.append(amount_of_trajectories)

            if method != "sliding_window":
                all_x = []
                all_y = []

                for sub_trajectory_string in sub_trajectories_for_trajectory:
                    sub_trajectory_dic = json.loads(sub_trajectory_string)

                    all_x.append(list(sub_trajectory_dic[" Longitude"].values()))
                    all_y.append(list(sub_trajectory_dic[" Latitude"].values()))

                sub_trajectories[method].update({trajectory_id: (all_x, all_y)})
        number_sub_trajectory_distribution_per_bool_interaction.update({method: number_sub_trajectories_of_trajectory})
    return number_sub_trajectory_distribution_per_bool_interaction, sub_trajectories


main(
    "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\real_results\\sub_trajectories\\",
    "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\real_graphs\\",
    12
)

#main(
#    "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\fake_results\\sub_trajectories\\",
#    "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\fake_graphs\\",
#    2000
#)
