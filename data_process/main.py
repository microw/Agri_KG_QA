#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/20 21:08
# @Author  : yimoru
# @FileName: main.py
# @Software: PyCharm

import build_graph
import data_process.data_city2weather as cw
import data_process.data_plant2nutrition as pn
import shutil
import os

if __name__ == '__main__':

    print("正在对数据进行处理...")
    cw.main()
    pn.main()
    father_path = os.path.abspath('..')
    shutil.copy('csv\weather_plant.csv', os.path.join(father_path, 'data'))

    print("\n数据处理完成 \n正在构建知识图谱...")

    build_graph.load()

    print('\n知识图谱构建完成...')

