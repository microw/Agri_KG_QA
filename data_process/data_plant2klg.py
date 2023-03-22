#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/21 15:58
# @Author  : yimoru
# @FileName: data_plant2klg.py
# @Software: PyCharm
import os
import csv
import pandas as pd
from tqdm import tqdm

base_path = os.path.abspath('.')  # 获得当前工作目录
father_path = os.path.abspath('..')  # 获得当前工作目录的父目录


def get_plant_klg(files):
    """
    获取互动百科中类型包含植物的条目
    :param files: 文件列表，
    :return: plant_klg.csv
    """
    data = []

    for filename in files:
        with open(filename, encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)  # 使用csv.reader读取csv_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:  # 将csv 文件中的数据保存到data中
                if '植物' in row[3] and row[0] != '大豆垄三栽培'\
                        and '种' != row[0] and '植物' != row[0]:

                    data.append(row)  # 选择某一列加入到data数组中

    # for i in range(len(data)):
    #     if len(data[i]) == 11:
    #         print(data[i])

    name = ["title", "url", "image", "openTypeList", "detail", "baseInfoKeyList", "baseInfoValueList"]
    test = pd.DataFrame(columns=name, data=data)
    # print(test)
    test.to_csv(os.path.join(base_path, f'plant_klg.csv'), encoding='utf8', index=False)


def get_plant_detail(files):
    """
    获取三元组《plant，气候，detail》;
    获得city字典
    :param files: 文件列表，
    :return: plant2detail.csv dict/plant.txt
    """
    plant2detail = {'plant': 'detail'}

    for filename in files:
        with open(filename, encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)  # 使用csv.reader读取csv_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:  # 将csv 文件中的数据保存到data中
                plant2detail[row[0]] = row[4]

    data = {}

    with open(os.path.join(father_path, 'data/plant2detail.csv'), 'w', encoding='utf8') as f:
        [f.write('{0},简介,{1}\n'.format(key, value)) for key, value in tqdm(plant2detail.items())]

    with open(os.path.join(father_path, 'dict/plant.txt'), 'w', encoding='utf8') as f:
        [f.write(f'{key}\n') for key, value in tqdm(plant2detail.items())]


def main():
    entity_file1 = [os.path.join(base_path, 'csv/hudong_pedia.csv'),
                    os.path.join(base_path, 'csv/hudong_pedia2.csv')]  # 文件列表
    get_plant_klg(entity_file1)

    entity_file2 = [os.path.join(base_path, 'plant_klg.csv')]
    get_plant_detail(entity_file2)


if __name__ == '__main__':
    main()
