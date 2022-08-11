import os
import matplotlib.pyplot as plt
import utilities


def difference_in_threshold_graph(confusion_matrix, distance_method, directory=".\\temp\\", rounding=2):
    if not os.path.exists(directory):
        os.mkdir(directory)

    directory += "treshold_graph\\"
    metrics_list_per_segmentation_method = transform_metrics_to_lists(confusion_matrix, rounding)
    metrics = change_data_order(metrics_list_per_segmentation_method)
    if not os.path.exists(directory):
        os.mkdir(directory)

    distances = list(confusion_matrix.keys())

    for metric in metrics.keys():
        ax = plt.subplot()
        ax.set_xticklabels(distances)
        ax.set_xlabel("Distance treshold")
        ax.set_ylabel(metric)

        #ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        plt.ylim(0,1.05)

        #plt.title(distance_method)

        results_per_method = metrics[metric]

        for method in results_per_method.keys():
            ax.plot(results_per_method[method], label=method)


        ax.legend(loc=4)
        #plt.show()
        plt.savefig(directory + distance_method+"_"+metric)
        plt.cla()


def change_data_order(metrics_list_per_segmentation_method):
    metrics = {}
    for segmentation_method in metrics_list_per_segmentation_method.keys():
        metric_lists = metrics_list_per_segmentation_method[segmentation_method]

        for metric in metric_lists.keys():
            ordered_results = metric_lists[metric]

            if metric not in metrics.keys():
                metrics.update({metric: {segmentation_method: ordered_results}})
            else:
                metrics[metric].update({segmentation_method: ordered_results})
    return metrics


def transform_metrics_to_lists(confusion_matrix, rounding):
    methods = {}
    for treshold in confusion_matrix.keys():
        metrics_per_segmentation_method = confusion_matrix[treshold]
        for segmentation_method in metrics_per_segmentation_method.keys():
            data = metrics_per_segmentation_method[segmentation_method]

            if segmentation_method not in methods.keys():
                methods.update({segmentation_method:
                    {
                        "accuracy": [],
                        "f1_score": [],
                        "precision": [],
                        "recall": []

                    }
                })
            accuracy, f1_score, precision, recall = utilities.retrieve_metrics(data, rounding)

            methods[segmentation_method]["accuracy"].append(accuracy)
            methods[segmentation_method]["f1_score"].append(f1_score)
            methods[segmentation_method]["precision"].append(precision)
            methods[segmentation_method]["recall"].append(recall)
    return methods
