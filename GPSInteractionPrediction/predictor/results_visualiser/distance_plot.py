import matplotlib.pyplot as plt
import os


def visualize(results, interaction_bool, trip_id, save_dir=".\\results\\"):
    fig, ax = plt.subplots()

    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    distance_plot_dir = save_dir + "distance_plots\\"

    if not os.path.isdir(distance_plot_dir):
        os.mkdir(distance_plot_dir)

    for method in results.keys():
        if method is not "Naive":
            for distance_method in results[method].keys():
                distances = []
                data = results[method][distance_method]

                for item_i in data:
                    item = data[item_i]
                    distances.append(item["distance"])

                plt.plot(distances)

                if not os.path.exists(distance_plot_dir+str(trip_id)):
                    os.mkdir(distance_plot_dir+str(trip_id))
                ax.set_xlabel("Time")
                ax.set_ylabel("Distance")

                plt.tight_layout()
                plt.savefig(distance_plot_dir+str(trip_id)+"\\distance_plot_"+str(trip_id)+"_"+str(interaction_bool)+"_"+str(method)+"_"+str(distance_method)+".png")
                plt.close()
