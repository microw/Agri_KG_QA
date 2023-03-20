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

    cw.main()
    pn.main()

    father_path = os.path.abspath('..')
    shutil.copy('csv\weather_plant.csv', os.path.join(father_path, 'data'))
    os.renames(os.path.join(father_path, 'data\weather_plant.csv'),
               os.path.join(father_path, 'data\weather2plant.csv'))

    build_graph.main()

