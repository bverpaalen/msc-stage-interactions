import os
import matplotlib.pyplot as plt
import numpy as np
import utilities


def bar_plot(confusion_matrix, subject, save_dir, rounding=2):
    for threshold in confusion_matrix.keys():
        accuracies = []
        precisions = []
        recalls = []
        f1_scores = []
        labels = []

        trajectory_methods = confusion_matrix[threshold]
        for trajectory_method in trajectory_methods.keys():
            labels.append(trajectory_method)
            data = trajectory_methods[trajectory_method]

            accuracy, f1_score, precision, recall = utilities.retrieve_metrics(data, rounding)

            accuracies.append(accuracy)
            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1_score)
        title = subject + "_" + format(threshold, "f")
        plot([accuracies, precisions, recalls, f1_scores], ["Accuracy", "Precision", "Recall", "F1_Score"],
             labels=labels, title=title, save_dir=save_dir)


def plot(data_sets, data_labels, labels, title, save_dir):

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    save_dir += "\\distance_threshold_plots\\"

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    save_dir += title.split("_")[0] + "\\"

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    width = 0.1

    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    i = 0
    for data_set in data_sets:
        difference = i - ((len(data_sets) - 1) / 2)

        rect = plt.bar(x + width * difference, data_set, width=width, label=data_labels[i])
        auto_label(ax, rect)
        i += 1
    ax.set_xticklabels(labels)
    ax.set_xticks(x)
    ax.set_ylabel("Percentage")
    ax.legend()

    ax.set_ylim((0, 1.05))

    fig.tight_layout()
    title.replace(".", ",")
    file_path = save_dir + title + ".png"
    plt.savefig(file_path)
    plt.close()


# source: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
def auto_label(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()

        if (height % 1) == 0:
            height = int(height)

        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')