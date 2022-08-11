import sklearn.cluster
from utilities import replace_time_for_seconds
import pandas


def run(trajectories):
    per_trajectory_sub_trajectories = {}
    i = 0
    for trajectory in trajectories:
        seconds_df = replace_time_for_seconds(trajectory)
        trajectory[" Seconds"] = seconds_df

        to_cluster_data = trajectory[[" Latitude", " Longitude"]]

        #cluster_data = sklearn.cluster.OPTICS(min_samples=2, algorithm="brute").fit(to_cluster_data)
        #cluster_data = sklearn.cluster.DBSCAN(eps=3, min_samples=3).fit(to_cluster_data)
        cluster_data = sklearn.cluster.k_means(to_cluster_data, n_clusters=5)

        clusters = labeled_cluster_prediction_to_sub_trajectories(trajectory, cluster_data)
        #clusters = cluster_prediction_to_sub_Trajectories(trajectory, cluster_data)
        sub_trajectories = extract_sub_trajectories(clusters)

        per_trajectory_sub_trajectories.update({i: sub_trajectories})
        i += 1
    return per_trajectory_sub_trajectories


def labeled_cluster_prediction_to_sub_trajectories(trajectory, cluster_data):
    cluster = {}
    #cluster_mask = cluster_data.labels_

    cluster_mask = cluster_data[1]
    for i in range(len(cluster_mask)):
        coordinate = trajectory.iloc[i]
        label = cluster_mask[i]
        if label not in cluster:
            cluster.update({label: pandas.DataFrame(columns=trajectory.columns)})
        cluster[label] = cluster[label].append(coordinate, ignore_index=True)
    return cluster


def extract_sub_trajectories(clusters):
    sub_trajectories = []
    for key in clusters.keys():
        if key != -1:
            sub_trajectories.append(clusters[key])
    return sub_trajectories
