import glob
import json


def get_files(dir_path, extension):
    files = glob.glob(dir_path + "*" + extension)
    return files


def get_dirs(dir_path):
    dirs = glob.glob(dir_path + "\\*\\")
    return dirs


def get_metadata(path, pos_id = 0, pos_bool = 1):
    file_name = path.split("\\")[-1]

    split_file_name = file_name.split("_")

    file_id = int(split_file_name[pos_id])
    has_interaction = split_file_name[pos_bool] == "True" or split_file_name[pos_bool] == 1
    meta_data = (file_id, has_interaction)

    return meta_data


def get_data(path):
    read_file = open(path)
    data = json.load(read_file)
    read_file.close()
    return data
