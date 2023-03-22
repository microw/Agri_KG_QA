#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/15 10:53
# @Author  : yimoru
# @FileName: QA.py
# @Software: PyCharm


import os
import ahocorasick
from py2neo import Graph, Node, Relationship
from django.shortcuts import render


class QuestionClassifier:
    def __init__(self):
        # cur_dir = os.path.abspath('.')  # 获得当前工作目录的父目录
        cur_dir = os.path.abspath('..')  # 获得当前工作目录的父目录
        # 特征值路径
        self.city_path = os.path.join(cur_dir, 'dict/city.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        self.plant_path = os.path.join(cur_dir, 'dict/plant.txt')

        # 加载特征值
        self.city_wds = [i.strip() for i in open(self.city_path, encoding='utf8') if i.strip()]
        self.food_wds = [i.strip() for i in open(self.food_path, encoding='utf8') if i.strip()]
        self.plant_wds = [i.strip() for i in open(self.plant_path, encoding='utf8') if i.strip()]
        self.region_words = set(self.city_wds + self.food_wds + self.plant_wds)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构造词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.city_qwds = ['气候']
        self.food_qwds = ['营养元素', '营养成分']
        self.cityplant_qwds = ['适合种植', '可以种植', '应该种植']
        self.plant_qwds = ['详细信息', '简介', '基本信息', '']

        print('model init finished ......')
        return

    # 构造词对应类型
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.city_wds:
                wd_dict[wd].append('city')
                wd_dict[wd].append('city2plant')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.plant_wds:
                wd_dict[wd].append('plant2detail')

        return wd_dict

    # 构造actree，加速过滤
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()  # 创建自动机
        for index, word in enumerate(wordlist):  # 构造trie树
            actree.add_word(word, (index, word))
        actree.make_automaton()  #
        return actree

    # 问句过滤
    def check_question(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        # print(f"stop_wds:{stop_wds}")
        # print(f"final_wds:{final_wds}")
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        # print(final_dict)

        return final_dict

    # 基于特征词进行分类
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    # 分类主函数
    def classify(self, question):
        data = {}
        question_dict = self.check_question(question)
        if not question_dict:
            return {}
        data['args'] = question_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in question_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # city
        if self.check_words(self.city_qwds, question) and ('city' in types):
            question_type = 'city'
            question_types.append(question_type)

        # plant
        if self.check_words(self.food_qwds, question) and ('food' in types):
            question_type = 'food'
            question_types.append(question_type)

        # city2plant
        if self.check_words(self.cityplant_qwds, question) and ('city2plant' in types):
            question_type = 'city2plant'
            question_types.append(question_type)

        # plant2detail
        if self.check_words(self.plant_qwds, question) and ('plant2detail' in types):
            question_type = 'plant2detail'
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data


class QuestionPaser:
    # 构建实体节点
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    # 解析主函数
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {'question_type': question_type}
            sql = []
            if question_type == 'city':
                sql = self.sql_transfer(question_type, entity_dict.get('city'))
            elif question_type == 'food':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))
            elif question_type == 'city2plant':
                sql = self.sql_transfer(question_type, entity_dict.get('city2plant'))
            elif question_type == 'plant2detail':
                sql = self.sql_transfer(question_type, entity_dict.get('plant2detail'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    # 针对不同的问题，分开进行处理

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询城市气候
        if question_type == 'city':
            sql = ["MATCH (m:city)-[relation:气候]->(n:weather) where m.city = '{0}'" \
                   " return n.weather, m.city".format(i) for i in entities]
        # 查询food营养成分
        elif question_type == 'food':
            sql = ["MATCH (m:food)-[r:营养元素]->(n:nutrition) where m.food = '{0}' " \
                   "return n.nutrition, m.food".format(i) for i in entities]
        # 查询city2plant营养成分
        elif question_type == 'city2plant':
            sql = ["MATCH (m:city)-[*2]->(n) where m.city = '{0}'" \
                   " return n.plant, m.city".format(i) for i
                   in entities]
        # 查询plant2detail
        elif question_type == 'plant2detail':
            sql = ["MATCH (m:plant)-[relation:简介]->(n:detail) where m.plant = '{0}'" \
                   " return n.detail, m.plant".format(i) for i in entities]

        return sql


class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'city':
            desc = [i['m.city'] for i in answers]
            subject = answers[0]['n.weather']
            final_answer = '{1}的气候类型是：{0}'.format(subject, ''.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'food':
            desc = [i['m.food'] for i in answers]
            subject = answers[0]['n.nutrition']
            final_answer = '{1}的营养成分包括：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'city2plant':
            desc = [i['m.city'] for i in answers]
            subject = []
            for i in range(len(answers)):
                # subject = answers[0]['n.plant']
                subject.append(answers[i]['n.plant'])
            final_answer = '{1}适合种植的植物包括：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'plant2detail':
            desc = [i['m.plant'] for i in answers]
            subject = answers[0]['n.detail']
            final_answer = '{1}的基本介绍：{0}'.format(subject, ''.join(list(set(desc))[:self.num_limit]))
        return final_answer


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是智能助理，希望可以帮到您。如果没答上来，祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        print(f'res_classify: {res_classify}')
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        print(f'res_sql:{res_sql}')
        final_answers = self.searcher.search_main(res_sql)
        print(f'final_answers: {final_answers}')

        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


def question_answering(request):  # index页面需要一开始就加载的内容写在这里
    context = {'ctx': ''}
    if request.GET:
        question = request.GET['question']
        handler = ChatBotGraph()
        # question = input('input an question:')
        d = handler.chat_main(question)
        # print(type(data))
        data = [d]
        ret_dict = {'answer': data}
        print(ret_dict)
        # context = {'ctx': data}
        if len(ret_dict) != 0 and ret_dict != 0:
            return render(request, 'question_answering.html', {'ret': ret_dict})
        print(context)
        return render(request, 'question_answering.html', {'ctx': '暂未找到答案'})
    return render(request, 'question_answering.html', context)


if __name__ == '__main__':
    handler = ChatBotGraph()
    # question = '伦敦的气候？'
    question = '崇明县适合种植什么？'
    # question = '豆腐乳的营养成分？'
    # question = '茄子的基本信息？'
    # question = '植物'

    data = handler.chat_main(question)
    print(data)
