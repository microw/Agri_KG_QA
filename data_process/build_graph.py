#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 22:37
# @Author  : yimoru
# @FileName: build_graph.py
# @Software: PyCharm

from py2neo import Graph, Node, Relationship, Subgraph
import pandas as pd
from tqdm import tqdm
import csv
import os

base_path = os.path.abspath('.')  # 获得当前工作目录
father_path = os.path.abspath('..')  # 获得当前工作目录的父目录
# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph("http://localhost:7474", username="root", password='123456')
graph.delete_all()


def load():
    # 导入city2weather.csv
    with open(os.path.join(father_path, 'data/city2weather.csv'), 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        data = list(reader)
    # print(data[1])  # ['果蔬汁', '营养成分', '维生素']
    print('正在加载city2weather...')

    for i in tqdm(range(1, len(data))):
        node1 = Node(f'city', city=data[i][0])
        node2 = Node(f'weather', weather=data[i][2])
        graph.create(node1)
        graph.create(node2)
        relation = Relationship(node1, f'气候', node2)
        graph.create(relation)

    # 导入food2nutrition.csv
    with open(os.path.join(father_path, 'data/food2nutrition.csv'), 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        data = list(reader)
    # print(data[1])  # ['果蔬汁', '营养成分', '维生素']
    print('\n正在加载food2nutrition...')

    for i in tqdm(range(1, len(data))):
        node1 = Node(f'food', food=data[i][0])
        node2 = Node(f'nutrition', nutrition=data[i][2])
        graph.create(node1)
        graph.create(node2)
        relation = Relationship(node1, f'营养元素', node2)
        graph.create(relation)

    # 导入weather2plant.csv
    with open(os.path.join(father_path, 'data/weather_plant.csv'), 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        data = list(reader)
    # print(data[1])  # ['果蔬汁', '营养成分', '维生素']
    print('\n正在加载weather2plant...')
    for i in tqdm(range(1, len(data))):
        node1 = graph.nodes.match(f'weather', weather=data[i][0]).first()
        node2 = Node(f'plant', plant=data[i][2])

        graph.create(node2)
        if node1 is None:
            node1 = Node(f'weather', weather=data[i][0])
        relation = Relationship(node1, f'适合种植', node2)
        graph.create(relation)


if __name__ == '__main__':
    load()
