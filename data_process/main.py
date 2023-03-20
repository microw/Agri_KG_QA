#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/20 21:08
# @Author  : yimoru
# @FileName: main.py
# @Software: PyCharm

# import build_graph
import data_process.data_city2weather as cw
import data_process.data_plant2nutrition as pn

if __name__ == '__main__':
    cw.main()
    pn.main()
    build_graph.main()

