# -*- coding: utf-8 -*-
from __future__ import division
import redis
import operator


class Classifier(object):

    def __init__(self):
        self.__persister = redis.StrictRedis(host="192.168.6.151", port=6379, db=0)
        self._default_term_frequency = 0.001
        self.__category_namespace = "demo_home_trained_category"
        self.__text_category_namespace = "demo_home_trained_text_category"

    def __tokenize(self, txt):
        return txt.split(" ")

    def train(self,txt,category):
        tokens = self.__tokenize(txt)
        # incr train data category count
        self.__incr_train_category_count(category,len(tokens))
        # incr train token_category count
        self.__incr_train_text_count(tokens,category)

    def __incr_train_category_count(self, train_category, token_count):
        self.__persister.hincrby(self.__category_namespace, train_category, token_count)

    def __incr_train_text_count(self,tokens, category):
        for token in tokens:
            self.__persister.hincrby(self.__text_category_namespace, token.upper() + '_' + category, 1)

    def __get_trained_categories_count(self):
        trained_categories = self.__persister.hkeys(self.__category_namespace)
        trained_categories_count = {}
        for category in trained_categories:
            trained_categories_count[category] = int(self.__persister.hmget(self.__category_namespace, category)[0])
        return trained_categories_count

    def __get_token_count_in_trained_category(self, tokens):
        trained_categories = self.__persister.hkeys(self.__category_namespace)
        trained_categories_count = self.__get_trained_categories_count()
        data = {}
        result = {}
        for category in trained_categories:
            data[category] = []
            for token in tokens:

                if self.__persister.hexists(self.__text_category_namespace, token.upper() + '_' + category):
                    token_in_category = int(self.__persister.hmget(self.__text_category_namespace, token.upper()+'_'+category)[0])
                    category_count = int(trained_categories_count[category])
                    prob = token_in_category / category_count
                    data[category].append(prob)
                else:
                    data[category].append(0)
            result[category] = sum(data[category]) / len(data[category])
        return result

    def classify(self, txt):
        tokens = self.__tokenize(txt)
        token_cnt = self.__get_token_count_in_trained_category(tokens)
        return max(token_cnt.iteritems(), key=operator.itemgetter(1))[0]