import pandas as pd
import datetime
import json
import os


def extract_trajectories(paths, time_in_epoch=False):
    trajectories = []
    for path in paths:
        trajectory = pd.read_csv(path)
        # trajectory = trajectory.loc[:, ["time", "latitude", "longitude"]]
        trajectory = trajectory.rename(columns={'time': ' Time','latitude': ' Latitude', 'longitude': ' Longitude'})

        if time_in_epoch:
            trajectory[' Time'] = trajectory[' Time'].map(lambda a: pd.to_datetime(a).strftime('%H:%M:%S'))

        trajectories.append(trajectory)
    return trajectories


def match_point(point_a, trajectory):
    time = point_a.get(" Time")

    index = trajectory.index[trajectory[" Time"] == time].tolist()

    if len(index) > 0:
        index = index[0]
    else:
        return pd.DataFrame()
    
    point_b = trajectory.iloc[index]

    if time in list(trajectory[" Time"]):
        index = trajectory.index[trajectory[" Time"] == time].tolist()[0]
        point_b = trajectory.iloc[index]
        return point_b
    else:
        return pd.DataFrame()


def get_sec(t):
    h, m, s = t.split(":")
    seconds = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(float(s))).total_seconds())
    return seconds


def replace_time_for_seconds(df):
    time_df = df[[" Time"]]
    new_df = pd.Series()
    for index, time in time_df.iterrows():
        timestamp = time.values[0]
        # timestamp = datetime.datetime.fromtimestamp(timestamp / 1000000000)
        # seconds = get_sec(str(timestamp).split(' ')[1])
        seconds = get_sec(timestamp)
        new_df._set_value(index, seconds)
    return new_df


def pandas_df_to_coordinates_list(trajectory):
    coordinates_trajectory = trajectory[[" Latitude", " Longitude"]]
    list_coordinates_trajectory = list(coordinates_trajectory.values)
    return list_coordinates_trajectory


def pandas_df_to_long_lat_list(trajectory):
    latitude = list(trajectory[" Latitude"])
    longitude = list(trajectory[" Longitude"])

    return longitude, latitude


def save_dict(dictionary, prefix_name, trip_id="", directory=".\\results_v2\\"):
    trip_id = str(trip_id)

    json_data = json.dumps(dictionary)
    name_file = ""

    if len(trip_id) > 0:
        name_file = trip_id+"_"
    if not os.path.isdir(directory):
        os.mkdir(directory)

    name_file += prefix_name

    f = open(directory + name_file, "w")
    f.write(json_data)
    f.close()


def results_to_json(dictionary):
    for method in dictionary.keys():
        for distance_method in dictionary[method].keys():
            if method != "Naive":
                data = dictionary[method][distance_method]
                for item_i in data.keys():
                    item = data[item_i]
                    trajectory_set = data[item_i]["trajectory_set"]
                    new_trajectory_set = []
                    for i in range(len(trajectory_set)):
                        new_trajectory_set.append(item["trajectory_set"][i].to_json())
                    data[item_i]["trajectory_set"] = new_trajectory_set
            else:
                trajectories = dictionary[method][distance_method]
                for trajectory_set_i in range(len(trajectories)):
                    trajectory_set = trajectories[trajectory_set_i]
                    for i in range(len(trajectory_set)):
                        new_trajectory_set = []
                        for j in range(len(trajectory_set[i])):
                            new_trajectory_set.append(trajectory_set[i][j].to_json())
                        trajectories[trajectory_set_i][i] = new_trajectory_set
    return dictionary


def merge_dics(head_dic, to_merge_dic):
    for merge_key in head_dic:
        head_dic[merge_key] += to_merge_dic[merge_key]


def retrieve_metrics(data, rounding):
    TP = data["True Positive"]
    FP = data["False Positive"]
    TN = data["True Negative"]
    FN = data["False Negative"]

    accuracy = round((TP + TN) / (TP + FP + FN + TN), rounding)

    if (TP + FP) > 0:
        precision = round(TP / (TP + FP), rounding)
    else:
        precision = 0

    if (TP + FN) > 0:
        recall = round(TP / (TP + FN), rounding)
    else:
        recall = 0

    if recall + precision > 0:
        f1_score = round(2 * (recall * precision) / (recall + precision), rounding)
    else:
        f1_score=0

    return accuracy, f1_score, precision, recall
