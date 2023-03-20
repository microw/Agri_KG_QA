#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 16:13
# @Author  : yimoru
# @FileName: data_plant2nutrition.py
# @Software: PyCharm
import os
import csv
import pandas as pd

base_path = os.path.abspath('.')  # 获得当前工作目录
father_path = os.path.abspath('..')  # 获得当前工作目录的父目录


def get_nutrition(files):
    """
    获取互动百科中baseInfoKeyList包含”营养成分“的互动条目
    :param files: 文件列表，
    :return: nutrition.csv
    """

    data = []

    for filename in files:
        with open(filename, encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)  # 使用csv.reader读取csv_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:  # 将csv 文件中的数据保存到data中
                if '营养成分' in row[5]:
                    data.append(row)  # 选择某一列加入到data数组中

    name = ["title", "url", "image", "openTypeList", "detail", "baseInfoKeyList", "baseInfoValueList"]
    test = pd.DataFrame(columns=name, data=data)
    # print(test)
    test.to_csv(os.path.join(father_path, f'data/nutrition.csv'), encoding='utf8', index=False)


def get_plant_nutrition(files):
    """
    获取三元组《food，营养，nutrition》;
    获得city字典
    :param files: 文件列表，
    :return: plant2nutrition.csv dict/food.txt
    """
    plant2nutrition = {}

    for filename in files:
        with open(filename, encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)  # 使用csv.reader读取csv_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:  # 将csv 文件中的数据保存到data中
                info_key = row[5].split("：##")
                info_value = row[6].split("##")
                d = dict(zip(info_key, info_value))
                for key, value in d.items():
                    if "营养成分" == key:
                        plant2nutrition[row[0]] = value

    # for i in plant2nutrition.items():
    #     print(i)

    with open(os.path.join(father_path, 'data/food2nutrition.csv'), 'w', encoding='utf8') as f:
        [f.write(f'{key},营养成分,{value}\n') for key, value in plant2nutrition.items()]

    with open(os.path.join(father_path, 'dict/food.txt'), 'w', encoding='utf8') as f:
        [f.write(f'{key}\n') for key, value in plant2nutrition.items()]


def main():
    entity_file1 = [os.path.join(base_path, 'csv/hudong_pedia.csv'),
                    os.path.join(base_path, 'csv/hudong_pedia2.csv')]  # 实体
    get_nutrition(entity_file1)

    entity_file2 = [os.path.join(father_path, 'data/nutrition.csv')]
    get_plant_nutrition(entity_file2)


if __name__ == '__main__':
    main()
