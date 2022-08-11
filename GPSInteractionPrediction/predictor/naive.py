import geopy.distance
import utilities


def run(trajectories, distance_threshold=1.5, minimal_length_interaction=5):
    interactions_per_trajectories = {}

    for i in range(len(trajectories)):
        trajectory_a = trajectories[i]
        for j in range(i + 1, len(trajectories)):
            recording = False
            interactions = []
            interaction = []

            trajectory_b = trajectories[j]
            for k in range(len(trajectory_a)):
                point_a = trajectory_a.iloc[k, :]
                point_b = utilities.match_point(point_a, trajectory_b)

                if not point_b.empty:
                    point_a_cor = point_a.get([" Latitude", " Longitude"])
                    point_b_cor = point_b.get([" Latitude", " Longitude"])

                    distance = geopy.distance.distance(point_a_cor, point_b_cor).meters

                    if distance <= distance_threshold:
                        recording = True
                        interaction.append((point_a, point_b))
                    elif recording:
                        recording = False
                        if len(interaction) >= minimal_length_interaction:
                            interactions.append(interaction)
                        interaction = []
                    else:
                        recording = []
            if recording and len(interaction) >= minimal_length_interaction:
                interactions.append(interaction)
            combination = str(i) + "," + str(j)
            interactions_per_trajectories.update({combination: interactions})
    return interactions_per_trajectories
