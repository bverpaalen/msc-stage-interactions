from glob import glob
import working_with_files as wwf
import utilities
import naive

distance_thresholds = list(range(1, 21))
for i in range(len(distance_thresholds)):
    distance_thresholds[i] = round(distance_thresholds[i] * 0.5, 1)

data_dir_path = "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\data_real_life\\2_2\\"


def main(data_dir):

    combinations = []
    for experiment_dir_path in glob(data_dir+"\\*\\"):
        for interaction_dir_path in glob(experiment_dir_path+"\\*\\"):
            trajectory_paths = glob(interaction_dir_path+"\\*.csv")

            dirs_in_trajectory_path = interaction_dir_path.split("\\")
            experiment_dir = dirs_in_trajectory_path[-3]
            interaction_dir = dirs_in_trajectory_path[-2]

            has_interaction = extract_interaction(interaction_dir)

            trajectory_paths.append(has_interaction)
            combinations.append(trajectory_paths)

    for distance_threshold in distance_thresholds:
        true_positive = 0
        false_positive = 0
        true_negative = 0
        false_negative = 0
        for combination in combinations:
            label = combination[2]

            data_paths = [combination[0], combination[1]]
            trajectories = utilities.extract_trajectories(data_paths)
            data = naive.run(trajectories, distance_threshold=distance_threshold)

            if len(data["0,1"]) > 0:
                prediction = True
            else:
                prediction = False

            if label and prediction:
                true_positive += 1
            elif not label and prediction:
                false_positive += 1
            elif not label and not prediction:
                true_negative += 1
            elif label and not prediction:
                false_negative += 1

        print(distance_threshold)
        print("True Positive:" + str(true_positive))
        print("False Positive:" + str(false_positive))
        print("True Negative:" + str(true_negative))
        print("False Negative:" + str(false_negative))

def extract_interaction(interaction_dir):
    if interaction_dir == "interaction":
        return True
    elif interaction_dir == "no_interaction":
        return False
    else:
        raise Exception("Interaction dir error")


main(data_dir_path)