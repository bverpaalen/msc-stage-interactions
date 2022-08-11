import os
import matplotlib.pyplot as plt
import seaborn as sn


def visualize_confusion_matrix(confusion_matrix_dic, save_dir=".\\results\\", confusion_dir="confusion_matrix"):
    print("Creating confusion matrix plot")

    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    if not os.path.isdir(save_dir + confusion_dir + "\\"):
        os.mkdir(save_dir + confusion_dir + "\\")

    for sub_trajectory_method in confusion_matrix_dic.keys():
        for distance_method in confusion_matrix_dic[sub_trajectory_method].keys():
            results = confusion_matrix_dic[sub_trajectory_method][distance_method]
            confusion_matrix = [
                                    [results["True Positive"], results["False Positive"]],
                                    [results["False Negative"], results["True Negative"]]
                                ]
            max_value = max((results["True Positive"]+results["False Negative"]),(results["True Negative"]+results["False Positive"]))
            fig = plt.figure()
            ax = sn.heatmap(confusion_matrix, vmin=0, vmax=max_value, annot=True, fmt="d", annot_kws={"size": 20}, linewidths=0.3)
            ax.set_xlabel("Actual")
            ax.set_ylabel("Prediction")
            #ax.set_title(str(sub_trajectory_method)+" "+str(distance_method))
            ax.set_xticklabels(["Interaction", "No Interaction"])
            ax.set_yticklabels(["Interaction", "No Interaction"])
            fig.savefig(save_dir + confusion_dir + "\\" + str(sub_trajectory_method)+"_"+distance_method+"_confusion_matrix.png")
            plt.close(fig)


def create_confusion_matrix(was_right):
    confusion_matrix_dic = {}

    for sub_trajectory_method in was_right.keys():
        confusion_matrix_dic.update({sub_trajectory_method: {}})
        for distance_method in was_right[sub_trajectory_method].keys():
            confusion_matrix_dic[sub_trajectory_method].update({distance_method: {}})
            confusion_matrix = confusion_matrix_dic[sub_trajectory_method][distance_method]
            confusion_matrix.update({"True Positive": 0, "False Positive": 0, "True Negative": 0, "False Negative": 0})
    return confusion_matrix_dic


def add_to_confusion_matrix(was_right, confusion_matrix_dic, interaction):
    for sub_trajectory_method in was_right.keys():
        for distance_method in was_right[sub_trajectory_method].keys():
            confusion_key = ""
            methods_were_right = was_right[sub_trajectory_method][distance_method]

            if methods_were_right:
                confusion_key += "True "
            elif not methods_were_right:
                confusion_key += "False "

            if (interaction and methods_were_right) or (not methods_were_right and not interaction):
                confusion_key += "Positive"
            else:
                confusion_key += "Negative"
            confusion_matrix_dic[sub_trajectory_method][distance_method][confusion_key] += 1