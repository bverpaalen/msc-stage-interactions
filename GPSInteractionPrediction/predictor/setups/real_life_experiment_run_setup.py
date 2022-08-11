from glob import glob
import predictor

data_dir_path = "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\data_real_life\\2_2\\"
save_dir = ".\\real_results\\"


def main(data_dir):
    cur_id = 0
    for experiment_dir_path in glob(data_dir+"\\*\\"):
        for interaction_dir_path in glob(experiment_dir_path+"\\*\\"):
            trajectory_paths = glob(interaction_dir_path+"\\*.csv")

            dirs_in_trajectory_path = interaction_dir_path.split("\\")
            experiment_dir = dirs_in_trajectory_path[-3]
            interaction_dir = dirs_in_trajectory_path[-2]

            has_interaction = extract_interaction(interaction_dir)

            predictor.run(trajectory_paths, has_interaction, cur_id, trajectory_dir=save_dir)
            cur_id += 1


def extract_interaction(interaction_dir):
    if interaction_dir == "interaction":
        return True
    elif interaction_dir == "no_interaction":
        return False
    else:
        raise Exception("Interaction dir error")


main(data_dir_path)