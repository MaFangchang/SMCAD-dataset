import os
import random


def obtain_files_list():
    for root, dirs, files in os.walk(training_set_path):
        return files


def rename_step_files(rename_list):
    for i, file_name in enumerate(rename_list):
        old_file = training_set_path + "\\" + file_name
        new_file = training_set_path + "\\" + str(i + 59500) + ".step"
        os.rename(old_file, new_file)
        print("已经重命名：", old_file)


if __name__ == '__main__':
    training_set_path = "D:\\Users Files\\Data\\Filtered_data_lean_version\\test"
    step_file_list = obtain_files_list()
    if "0_inc" in step_file_list:
        print("您已经重命名过一次训练集，请勿再次命名")
    else:
        rename_step_files(step_file_list)
