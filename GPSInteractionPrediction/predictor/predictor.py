from utilities import extract_trajectories, save_dict, results_to_json
from segmentation_algorithms import sliding_window, spatio_temporal_criteria, clustering
from results_visualiser import distance_plot
from functools import partial
import distance_metrics
import naive
import pandas
import sys
import copy
import os

testing = False

if len(sys.argv) < 2:
    if testing:
        data_paths = [
            "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\randomDataCreator\\fake_experiments\\trip_True_0_0.csv",
            "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\randomDataCreator\\fake_experiments\\trip_True_0_1.csv"
        ]
else:
    data_paths = sys.argv[1:]

sub_trajectory_algorithms = {
#    "sliding_window": sliding_window.run,
    "spatio_temporal_criteria": partial(spatio_temporal_criteria.run, speed_difference_threshold=0.75),
    "clustering": clustering.run
}

sub_trajectory_distance_methods = {
    "euclidean_distance": distance_metrics.average_euclidean_distance,
    "meter_distance": distance_metrics.average_meter_distance,
    "frechet_distance": distance_metrics.frechet_distance,
    "dynamic_time_warping_distance": distance_metrics.DTW_distance,
#    "hausdroff_distance": distance_metrics.Hausdroff_distance
}

threshold_per_method = {
    "euclidean_distance": 0.00002,
    "meter_distance": 1.5,
    "frechet_distance": 0.00004,
    "dynamic_time_warping_distance": 0.00005,
    "hausdroff_distance": 0.00004
}


def run(data_paths, interaction_bool, trip_id, trajectory_dir=".\\results\\", create_distance_plot=False, time_in_epoch=False):
    if not os.path.exists(trajectory_dir):
        os.mkdir(trajectory_dir)

    results = {}
    # print(data_paths)
    trajectories = extract_trajectories(data_paths, time_in_epoch)
    # print(trajectories)
    # print(trajectories)
    print("Naive\n")
    naive_interactions = naive.run(trajectories)
    # print(naive_interactions)
    results.update({"Naive": naive_interactions})

    sub_trajectories_per_segmentation_algorithm = sub_trajectory_creation(trajectories, sub_trajectory_algorithms)
    sub_trajectories_to_save = make_sub_trajectories_json_ready(copy.deepcopy(sub_trajectories_per_segmentation_algorithm))

    save_dict(sub_trajectories_to_save, prefix_name="sub_trajectories.json", trip_id=str(trip_id)+"_"+str(interaction_bool), directory=trajectory_dir + "sub_trajectories\\")

    for algorithm_name in sub_trajectories_per_segmentation_algorithm.keys():
        results.update({algorithm_name: {}})
        print(algorithm_name)
        
        sub_trajectories = sub_trajectories_per_segmentation_algorithm[algorithm_name]

        for distance_method_name in sub_trajectory_distance_methods.keys():
            distance_method = sub_trajectory_distance_methods[distance_method_name]
            sub_trajectory_distances = sub_trajectory_distance(sub_trajectories, algorithm_name, distance_method)
            results[algorithm_name].update({distance_method_name: sub_trajectory_distances})

    if create_distance_plot:
        distance_plot.visualize(results, interaction_bool, trip_id)
    #prediction = distance_to_prediction(results)

    # print(trajectory_dir + "distance_json\\")

    save_dict({"distance_prediction": results_to_json(copy.deepcopy(results)), "has_interaction": interaction_bool}, trip_id=str(trip_id) + "_" + str(interaction_bool), prefix_name="distance_prediction_data.json", directory=trajectory_dir + "distance_json\\")
    #was_right = compare_prediction(prediction, interaction_bool)
    #return was_right


def make_sub_trajectories_json_ready(dictionary):
    for method in dictionary.keys():
        for trajectory_id in dictionary[method].keys():
            for i in range(len(dictionary[method][trajectory_id])):
                dictionary[method][trajectory_id][i] = dictionary[method][trajectory_id][i].to_json()
    return dictionary


def sub_trajectory_distance(sub_trajectories, sub_trajectory_method, distance_method):
    sub_trajectory_distances = {}
    i = 0
    while i < len(sub_trajectories):
        trajectory_a = sub_trajectories[i]
        i += 1

        j = i
        while j < len(sub_trajectories):
            trajectory_b = sub_trajectories[j]

            trajectory_distances = compare_trajectories(trajectory_a, trajectory_b, sub_trajectory_method, distance_method)

            sub_trajectory_distances.update({str(i) + "," + str(j): trajectory_distances})
            j += 1
    return trajectory_distances


def compare_trajectories(trajectory_a, trajectory_b, sub_trajectory_method, distance_method):
    i = 0
    trajectory_distances = {}
    trajectory_sets = create_time_sets(trajectory_a, trajectory_b, sub_trajectory_method)
    for trajectory_set in trajectory_sets:
        distance = distance_method(trajectory_set[0], trajectory_set[1])
        trajectory_distances.update({i: {"distance": distance, "trajectory_set": trajectory_set}})
        i += 1

    return trajectory_distances


def create_time_sets(trajectory_a, trajectory_b, sub_trajectory_method):
    sub_trajectory_sets = []
    for sub_trajectory_a in trajectory_a:
        sub_trajectory_a = sub_trajectory_a.drop_duplicates(" Time")
        for sub_trajectory_b in trajectory_b:
            sub_trajectory_b = sub_trajectory_b.drop_duplicates(" Time")
            if sub_trajectory_a[" Time"].equals(sub_trajectory_b[" Time"]):
                sub_trajectory_set = (sub_trajectory_a, sub_trajectory_b)
                sub_trajectory_sets.append(sub_trajectory_set)
            elif sub_trajectory_method != "sliding_window":
                overlapping_time = pandas.merge(sub_trajectory_a, sub_trajectory_b, on=[" Time"])[" Time"]
                if len(overlapping_time) > 0:
                    overlapping_sub_trajectory_a = sub_trajectory_a.loc[
                        sub_trajectory_a[" Time"].isin(overlapping_time)]
                    overlapping_sub_trajectory_b = sub_trajectory_b.loc[
                        sub_trajectory_b[" Time"].isin(overlapping_time)]
                    sub_trajectory_set = (overlapping_sub_trajectory_a, overlapping_sub_trajectory_b)
                    sub_trajectory_sets.append(sub_trajectory_set)
    return sub_trajectory_sets


def sub_trajectory_creation(trajectories, sub_trajectory_methods):
    per_method_sub_trajectories = {}

    for method_name in sub_trajectory_methods.keys():
        method = sub_trajectory_methods[method_name]

        sub_trajectories = method(trajectories)
        per_method_sub_trajectories.update({method_name: sub_trajectories})
    return per_method_sub_trajectories


def distance_to_prediction(results):
    predictions = {}

    for method in results.keys():
        if method != "Naive":
            predictions.update({method: {}})
            for distance_method in results[method].keys():
                interaction_found = False
                data = results[method][distance_method]
                for item_i in data.keys():
                    distance = data[item_i]["distance"]
                    if distance < threshold_per_method[distance_method]:
                        interaction_found = True
                predictions[method].update({distance_method: interaction_found})
        else:
            if len(results["Naive"]["0,1"]) > 0:
                interaction_found = True
            else:
                interaction_found = False
            predictions.update({"Naive": {"Meter": interaction_found}})
    return predictions


def compare_prediction(predictions, interaction_bool):
    predictions_results = {}
    for method in predictions.keys():
        predictions_results.update({method: {}})
        for distance_method in predictions[method].keys():
            prediction = predictions[method][distance_method]
            if prediction == interaction_bool:
                is_right = True
            else:
                is_right = False
            predictions_results[method].update({distance_method: is_right})
    return predictions_results


if __name__ == "__main__" and testing:
    data_path = data_paths[0]
    trip_id = int(data_path.split("\\")[-1].split("_")[2])
    interaction_bool = bool(data_path.split("\\")[-1].split("_")[1])

    run(data_paths, interaction_bool, trip_id)
