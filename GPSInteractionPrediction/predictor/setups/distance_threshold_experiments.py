import working_with_files
from results_visualiser import performance_difference_visualisation, performance_bar_plot


small_range = list(range(1, 21))
for i in range(len(small_range)):
    small_range[i] = round(small_range[i] * 0.00001, 5)

small_range_v2 = list(range(1,41))
for i in range(len(small_range_v2)):
    small_range_v2[i] = round(small_range_v2[i] * 0.00001, 5)

small_range_v3 = list(range(10, 210, 10))
for i in range(len(small_range_v3)):
    small_range_v3[i] = round(small_range_v3[i] * 0.0000001, 7)

normal_range = list(range(1, 21))
for i in range(len(normal_range)):
    normal_range[i] = round(normal_range[i] * 0.5, 1)

test_distances = {
    "euclidean_distance": small_range,
    "meter_distance": normal_range,
    "frechet_distance": small_range,
    "dynamic_time_warping_distance": small_range_v2,
    #"hausdroff_distance": small_range_v3
}


def main(results_path, save_dir):
    dir_path = results_path + "distance_json\\"

    all_files = working_with_files.get_files(dir_path, extension=".json")
    confusion_matrix = {}

    for file in all_files[:1000]:
        meta_data = working_with_files.get_metadata(file)
        data = working_with_files.get_data(file)

        distances = get_distances(data)
        compare_test_distances(distances, test_distances, meta_data[1], confusion_matrix)

    for distance_method in confusion_matrix.keys():
        performance_bar_plot.bar_plot(confusion_matrix[distance_method], distance_method, save_dir)
        performance_difference_visualisation.difference_in_threshold_graph(confusion_matrix[distance_method], distance_method, directory=save_dir)


def get_distances(data):
    distance_predictions = data["distance_prediction"]
    new_distances_dic = {}

    for trajectory_method in distance_predictions.keys():
        if trajectory_method != "Naive":
            new_distances_dic.update({trajectory_method: {}})
            for distance_method in distance_predictions[trajectory_method].keys():
                distances = distance_predictions[trajectory_method][distance_method]
                new_distances = []
                for point_id in distances.keys():
                    distance = distances[point_id]["distance"]
                    new_distances.append(distance)
                new_distances_dic[trajectory_method].update({distance_method: new_distances})
    return new_distances_dic


def compare_test_distances(distances, test_distances, interaction_label, results):
    for distance_method in test_distances.keys():
        if distance_method not in results.keys():
            results.update({distance_method: {}})
        range_of_distances = test_distances[distance_method]

        for x_distance in range_of_distances:
            if x_distance not in results[distance_method].keys():
                results[distance_method].update({x_distance: {}})

            for trajectory_method in distances.keys():
                if trajectory_method not in results[distance_method][x_distance].keys():
                    results[distance_method][x_distance].update({trajectory_method: {"True Positive": 0,
                                                                                     "False Positive": 0,
                                                                                     "True Negative": 0,
                                                                                     "False Negative": 0}})

                # confusion_matrix.update({trajectory_method: {}})

                interaction_prediction = False
                trajectory_distance = distances[trajectory_method][distance_method]

                for point_distance in trajectory_distance:
                    if point_distance < x_distance:
                        interaction_prediction = True

                methods_were_right = interaction_prediction == interaction_label

                confusion_key = ""
                if methods_were_right:
                    confusion_key += "True "
                elif not methods_were_right:
                    confusion_key += "False "

                if (interaction_label and methods_were_right) or (not methods_were_right and not interaction_label):
                    confusion_key += "Positive"
                else:
                    confusion_key += "Negative"

                results[distance_method][x_distance][trajectory_method][confusion_key] += 1


#main(
#"C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\fake_results\\",
#"C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\fake_graphs\\"
#)


main(
    "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\real_results\\",
    "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\GPSInteractionPrediction\\predictor\\real_graphs\\"
)
