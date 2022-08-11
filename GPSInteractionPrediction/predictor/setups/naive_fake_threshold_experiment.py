import working_with_files as wwf
import utilities
import naive


distance_thresholds = list(range(1, 21))
for i in range(len(distance_thresholds)):
    distance_thresholds[i] = round(distance_thresholds[i] * 0.5, 1)

global_data_dir = "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\Artificial_Data_Generator\\fake_experiments_v2\\"


def main(data_dir):
    #data = load_data(data_dir)
    combinations = create_trajectory_path_combinations(data_dir)

    for distance_threshold in distance_thresholds:
        true_positive = 0
        false_positive = 0
        true_negative = 0
        false_negative = 0
        for combination in combinations:
            meta_data = wwf.get_metadata(combination[0], pos_id=2, pos_bool=1)

            data_paths = [combination[0], combination[1]]
            trajectories = utilities.extract_trajectories(data_paths)
            data = naive.run(trajectories, distance_threshold=distance_threshold)

            if len(data["0,1"]) > 0:
                prediction = True
            else:
                prediction = False
            label = meta_data[1]

            if label and prediction:
                true_positive += 1
            elif not label and prediction:
                false_positive += 1
            elif not label and not prediction:
                true_negative += 1
            elif label and not prediction:
                false_negative += 1

        print(distance_threshold)
        print("True Positive:"+str(true_positive))
        print("False Positive:"+str(false_positive))
        print("True Negative:"+str(true_negative))
        print("False Negative:"+str(false_negative))


def load_data(data_dir):
    files = wwf.get_files(data_dir, ".json")

    all_data = []
    for file in files:
        meta = wwf.get_metadata(file)
        data = wwf.get_data(file)

        naive_data = data["distance_prediction"]["Naive"]

        new_data = {
            "id": meta[0],
            "interaction_bool": meta[1],
            "naive_prediction": naive_data
        }
        all_data.append(new_data)
    return all_data


def create_trajectory_path_combinations(directory):
    combinations = []

    file_name = "trip_"
    for i in range(1000):
        for j in range(2):
            path = directory + file_name
            if j == 0:
                interaction = True
            else:
                interaction = False

            path += str(interaction)+"_"
            path += str(i)+"_"

            path_0 = path + "0.csv"
            path_1 = path + "1.csv"

            combinations.append([path_0, path_1])
    return combinations


def process_data(data_set):
    was_right = 0

    for data in data_set:
        prediction = data["naive_prediction"]["0,1"] != []
        label = data["interaction_bool"]

        if label == prediction:
            was_right += 1
    return was_right


main(global_data_dir)