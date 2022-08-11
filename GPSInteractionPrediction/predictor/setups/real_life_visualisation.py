from results_visualiser import map_visualisation, segmentation_visualization
import utilities
import working_with_files as wwf
from results_visualiser import time_space_figure
from glob import glob
import copy

path = "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\data_real_life\\2_2\\"
save_dir = "..\\real_graphs\\"

path2 = "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\Artificial_Data_Generator\\fake_experiments_v2\\"
save_dir2 = "..\\fake_graphs\\"

def main(data_dir):
    for experiment_dir_path in wwf.get_dirs(data_dir):
        for interaction_dir_path in wwf.get_dirs(experiment_dir_path):
            trajectory_paths = wwf.get_files(interaction_dir_path, "csv")
            path_to_data_split = interaction_dir_path.split("\\")
            prefix = path_to_data_split[-3] + "_" + path_to_data_split[-2]

            trajectories = utilities.extract_trajectories(trajectory_paths)

            list_trajectories = {}
            trajectory_id = 0
            for trajectory in trajectories:
                list_trajectory = utilities.pandas_df_to_long_lat_list(trajectory)
                list_trajectories.update({trajectory_id: list_trajectory})
                trajectory_id += 1
            map_visualisation.run(list_trajectories, save_dir, prefix)
            time_space_figure.time_space_figure(list_trajectories, save_dir, prefix, has_subs=False)



def main2(data_dir):
    trip_path = "trip_{bool}_{id}_{id_trajec}.csv"
    bools = [False, True]
    ids = list(range(1000))
    ids_trajec = [0, 1]

    for bool in bools:
        trip_path1 = copy.deepcopy(trip_path.replace("{bool}", str(bool)))
        for id in ids:
            trip_path2 = copy.deepcopy(trip_path1.replace("{id}", str(id)))

            trajectory_paths = []
            for id_trajec in ids_trajec:
                trip_path_trajec = data_dir + copy.deepcopy(trip_path2.replace("{id_trajec}", str(id_trajec)))
                trajectory_paths.append(trip_path_trajec)

            trajectories = utilities.extract_trajectories(trajectory_paths)

            list_trajectories = {}
            trajectory_id = 0
            for trajectory in trajectories:
                list_trajectory = utilities.pandas_df_to_long_lat_list(trajectory)
                list_trajectories.update({trajectory_id: list_trajectory})
                trajectory_id += 1
            prefix = trip_path2.split("_{id_trajec}")[0]
            map_visualisation.run(list_trajectories, save_dir2, prefix)
            time_space_figure.time_space_figure(list_trajectories, save_dir2, prefix, has_subs=False)

main(path)
#main2(path2)