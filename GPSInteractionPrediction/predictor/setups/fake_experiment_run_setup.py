import predictor
from results_visualiser import confusion_matrix

directory = "C:\\Users\\user\\Desktop\\Leiden\\Research_Project\\msc-stage-interactions\\Artificial_Data_Generator\\fake_experiments_v2\\"
save_dir = ".\\fake_results\\"


def main():
    file_name = "trip_"
    for i in range(1000):
        for j in range(2):
            path = directory + file_name
            if j == 0:
                interaction = True
            else:
                interaction = False
            print("Running id: "+str(i) + " "+str(interaction))

            path += str(interaction)+"_"
            path += str(i)+"_"

            path_0 = path + "0.csv"
            path_1 = path + "1.csv"

            was_right = predictor.run([path_0, path_1], interaction, i, save_dir, create_distance_plot=False)

            #if i == 0 and j == 0:
            #    confusion_matrix_dic = confusion_matrix.create_confusion_matrix(was_right)
            #confusion_matrix.add_to_confusion_matrix(was_right, confusion_matrix_dic, interaction)
    #confusion_matrix.visualize_confusion_matrix(confusion_matrix_dic, save_dir=save_dir)


main()
