import os
import random
import shutil


def obtain_files_list():
    for root, dirs, files in os.walk(test_set_path):
        return files


def move_step_files(move_list):
    for file_name in move_list:
        move_file = test_set_path + "\\" + file_name
        new_path = val_set_path + "\\" + file_name
        shutil.copyfile(move_file, new_path)
        os.remove(move_file)
        print("已经删除：", move_file)


if __name__ == '__main__':
    val_set_path = "D:\\Users Files\\Data\\Incremental_dataset\\val_inc"
    test_set_path = "D:\\Users Files\\Data\\Incremental_dataset\\test_inc"
    step_file_list = obtain_files_list()
    if len(step_file_list) > 3000:
        n = int(len(step_file_list) - 3000)
        print(n)
        print(step_file_list)
        move_file_list = random.sample(step_file_list, n)
        move_step_files(move_file_list)
    else:
        print("您已经转移过一次训练集，请勿再次筛选")
