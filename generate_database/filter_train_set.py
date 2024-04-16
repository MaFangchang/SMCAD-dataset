import os
import random


def obtain_files_list():
    for root, dirs, files in os.walk(training_set_path):
        return files


def remove_step_files(remove_list):
    for file_name in remove_list:
        del_file = training_set_path + "\\" + file_name
        os.remove(del_file)
        print("已经删除：", del_file)


if __name__ == '__main__':
    training_set_path = "D:\\Users Files\\Data\\Incremental_dataset\\test_inc"
    step_file_list = obtain_files_list()
    if len(step_file_list) > 6000:
        n = int(len(step_file_list) - 6000)
        print(n)
        print(step_file_list)
        remove_file_list = random.sample(step_file_list, n)
        remove_step_files(remove_file_list)
    else:
        print("您已经筛选过一次训练集，请勿再次筛选")
