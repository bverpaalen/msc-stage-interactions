import sys

sys.path.append(r'D:\School\Leiden\ResearchProject\code\msc-stage-interactions\GPSInteractionPrediction\predictor')

from results_visualiser import performance_difference_visualisation, performance_bar_plot
from glob import glob
import working_with_files as wwf
import utilities
import naive

distance_thresholds = list(range(1, 21))
for i in range(len(distance_thresholds)):
    distance_thresholds[i] = round(distance_thresholds[i] * 0.5, 1)

data_dir_path = r"D:\School\Leiden\ResearchProject\code\msc-stage-interactions\data\real_life_data\\"


def main(data_dir):

    print(data_dir)

    combinations = []
    for experiment_dir_path in glob(data_dir+"\\*\\"):
        print(experiment_dir_path)
        for interaction_dir_path in glob(experiment_dir_path+"\\*\\"):
            print(interaction_dir_path)
            trajectory_paths = glob(interaction_dir_path+"\\*.csv")

            dirs_in_trajectory_path = interaction_dir_path.split("\\")
            experiment_dir = dirs_in_trajectory_path[-3]
            interaction_dir = dirs_in_trajectory_path[-2]

            has_interaction = extract_interaction(interaction_dir)

            trajectory_paths.append(has_interaction)
            combinations.append(trajectory_paths)

    confusion_matrix = {}

    for distance_threshold in distance_thresholds:
        true_positive = 0
        false_positive = 0
        true_negative = 0
        false_negative = 0
        for combination in combinations:
            label = combination[2]

            data_paths = [combination[0], combination[1]]
            trajectories = utilities.extract_trajectories(data_paths, True)
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

        confusion_matrix.update({distance_threshold: { "naive": {
        "True Positive": true_positive,
        "False Positive": false_positive,
        "True Negative": true_negative,
        "False Negative": false_negative,            
            }}
        })

        print(distance_threshold)
        print("True Positive:" + str(true_positive))
        print("False Positive:" + str(false_positive))
        print("True Negative:" + str(true_negative))
        print("False Negative:" + str(false_negative))

    performance_bar_plot.bar_plot(confusion_matrix, 'Naive', save_dir=r"D:\School\Leiden\ResearchProject\code\msc-stage-interactions\GPSInteractionPrediction\predictor\setups\real_graphs\\")
    performance_difference_visualisation.difference_in_threshold_graph(confusion_matrix, 'Naive', directory=r"D:\School\Leiden\ResearchProject\code\msc-stage-interactions\GPSInteractionPrediction\predictor\setups\real_graphs\\")

def extract_interaction(interaction_dir):
    if interaction_dir == "interaction":
        return True
    elif interaction_dir == "no_interaction":
        return False
    else:
        raise Exception("Interaction dir error")


main(data_dir_path)