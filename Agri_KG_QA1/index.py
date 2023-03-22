#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/22 14:19
# @Author  : yimoru
# @FileName: index.py
# @Software: PyCharm

from django.shortcuts import render
from django.views.decorators import csrf


def index_view(request):  # index页面需要一开始就加载的内容写在这里
    context = {}
    return render(request, 'index.html', context)
