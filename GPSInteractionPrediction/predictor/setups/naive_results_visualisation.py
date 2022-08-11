from results_visualiser import performance_difference_visualisation

file_path = "..\\fake_results\\naive_results\\threshold_experiment.txt"
#file_path = "..\\real_results\\naive_results\\threshold_experiment.txt"


def main(file_path):
    f = open(file_path, "r")
    data = load_data(f)
    print(data)

    performance_difference_visualisation.difference_in_threshold_graph(data, "naive_fake")


def load_data(f):
    data = {}
    for counter, line in enumerate(f):
        if counter % 5 == 0:
            threshold = float(line)
            data.update({threshold: {"naive":{}}})
        else:
            split_line = line.split(":")
            data_key = split_line[0]
            data_value = int(split_line[1])
            data[threshold]["naive"].update({data_key: data_value})
    return data


main(file_path)