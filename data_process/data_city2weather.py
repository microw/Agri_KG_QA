#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/15 15:15
# @Author  : yimoru
# @FileName: data_city.py
# @Software: PyCharm

import os
import csv
import pandas as pd

base_path = os.path.abspath('.')  # 获得当前工作目录
father_path = os.path.abspath('..')  # 获得当前工作目录的父目录


def get_city(files):
    """
    获取互动百科中包含城市气候信息的条目
    :param files: 文件列表，
    :return: city.csv
    """
    data = []

    for filename in files:
        with open(filename, encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)  # 使用csv.reader读取csv_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:  # 将csv 文件中的数据保存到data中
                if '气候条件' in row[5]:
                    data.append(row)  # 选择某一列加入到data数组中

    name = ["title", "url", "image", "openTypeList", "detail", "baseInfoKeyList", "baseInfoValueList"]
    test = pd.DataFrame(columns=name, data=data)
    # print(test)
    test.to_csv(os.path.join(base_path, f'city.csv'), encoding='utf8', index=False)


def get_city_weather(files):
    """
    获取三元组《city，气候，weather_》;
    获得city字典
    :param files: 文件列表，
    :return: city2weather_.csv dict/city.txt
    """
    city2weather = {}

    for filename in files:
        with open(filename, encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)  # 使用csv.reader读取csv_file中的文件
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:  # 将csv 文件中的数据保存到data中
                list1 = row[6].split("##")
                city2weather[row[0]] = list1

    for key, value in city2weather.items():
        for i in value:
            if '气候' in i:
                city2weather[key] = i
            elif '温带' in i:
                city2weather[key] = i
            elif '热带' in i:
                city2weather[key] = i
            elif '大陆' in i:
                city2weather[key] = i
            elif '荒漠' in i:
                city2weather[key] = i
            elif '高原' in i:
                city2weather[key] = i
        city2weather[key] = "".join(city2weather[key])
    data = {}
    for key, value in city2weather.items():
        if len(value) <= 20:
            data[key] = value

    # for i in data.items():
    #     print(i)
    with open(os.path.join(father_path, 'data/city2weather_.csv'), 'w', encoding='utf8') as f:
        [f.write('{0},气候,{1}\n'.format(key, value)) for key, value in data.items()]

    with open(os.path.join(father_path, 'dict/city.txt'), 'w', encoding='utf8') as f:
        [f.write(f'{key}\n') for key, value in data.items()]


def main():
    entity_file1 = [os.path.join(base_path, 'csv/hudong_pedia.csv'),
                    os.path.join(base_path, 'csv/hudong_pedia2.csv')]  # 文件列表
    get_city(entity_file1)

    entity_file2 = [os.path.join(base_path, 'city.csv')]
    get_city_weather(entity_file2)


if __name__ == '__main__':
    main()
