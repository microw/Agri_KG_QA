#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 22:37
# @Author  : yimoru
# @FileName: build_graph.py
# @Software: PyCharm

from py2neo import Graph, Node, Relationship
import pandas as pd
import csv
import os

base_path = os.path.abspath('.')  # 获得当前工作目录
father_path = os.path.abspath('..')  # 获得当前工作目录的父目录
# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph("http://localhost:7474", username="root", password='123456')
graph.delete_all()


def load(f2r):
    for key, value in f2r.items():
        with open(os.path.join(father_path, f'data/{key}.csv'), 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            data = list(reader)
        print(data[1])  # ['果蔬汁', '营养成分', '维生素']

        entity = key.split('2')
        entity1 = entity[0]
        entity2 = entity[1]
        for i in range(1, len(data)):
            node1 = Node(f'{entity1}', entity1=data[i][0])
            node2 = Node(f'{entity2}', entity2=data[i][2])
            # relation = Node('relation', relation=data[i][1])
            graph.create(node1)
            graph.create(node2)
            # graph.create(relation)

            relation = Relationship(node1, f'{value}', node2)

            graph.create(relation)


if __name__ == '__main__':
    file2relation = {'city2weather_': '气候', 'food2nutrition': '营养成分', 'weather2plant': '适合种植'}
    load(file2relation)
