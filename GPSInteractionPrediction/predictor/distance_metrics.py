import geopy.distance
import similaritymeasures
import utilities
import scipy.spatial


def average_euclidean_distance(trajectory_a, trajectory_b):
    average_distance = average_function_distance(trajectory_a, trajectory_b, scipy.spatial.distance.euclidean)
    return average_distance


def average_meter_distance(trajectory_a, trajectory_b):
    def distance_in_meters(cor_a, cor_b):
        return geopy.distance.distance(cor_a, cor_b).meters

    average_distance = average_function_distance(trajectory_a, trajectory_b, distance_in_meters)
    rounded_average_distance = round(average_distance, 1)
    return rounded_average_distance


def average_function_distance(trajectory_a, trajectory_b, metric_function):

    if trajectory_a[" Time"].reset_index(drop=True).equals(trajectory_b[" Time"].reset_index(drop=True)):
        sum_distance = 0
        for index, point_a in trajectory_a.iterrows():
            point_a_time = point_a.get(" Time")
            point_b = trajectory_b[trajectory_b[" Time"] == point_a_time].squeeze()
            cor_a = point_a.get([" Latitude", " Longitude"])
            cor_b = point_b.get([" Latitude", " Longitude"])

            distance = metric_function(cor_a, cor_b)
            sum_distance += distance
        average_distance = sum_distance / len(trajectory_a)

        return average_distance
    else:
        #print(trajectory_a)
        #print(trajectory_b)
        raise Exception("Different timestamps in trajectories")


def frechet_distance(trajectory_a, trajectory_b):
    list_coordinates_trajectory_a = utilities.pandas_df_to_coordinates_list(trajectory_a)
    list_coordinates_trajectory_b = utilities.pandas_df_to_coordinates_list(trajectory_b)

    distance = similaritymeasures.frechet_dist(list_coordinates_trajectory_a, list_coordinates_trajectory_b)
    return distance


def DTW_distance(trajectory_a, trajectory_b):
    list_coordinates_trajectory_a = utilities.pandas_df_to_coordinates_list(trajectory_a)
    list_coordinates_trajectory_b = utilities.pandas_df_to_coordinates_list(trajectory_b)

    distances = similaritymeasures.dtw(list_coordinates_trajectory_a, list_coordinates_trajectory_b)
    return distances[0]


def Hausdroff_distance(trajectory_a, trajectory_b):
    list_coordinates_trajectory_a = utilities.pandas_df_to_coordinates_list(trajectory_a)
    list_coordinates_trajectory_b = utilities.pandas_df_to_coordinates_list(trajectory_b)

    distances = scipy.spatial.distance.directed_hausdorff(list_coordinates_trajectory_a, list_coordinates_trajectory_b)
    return distances[0]

