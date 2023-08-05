# -*- coding: UTF-8 -*-
# @Time : 2022/5/15 22:19 
# @Author : 刘洪波
from textx_model.Model import meta


class GeneralModel(object):
    def __init__(self, input_data: str, input_rule: str):
        self.input_data = input_data
        self.input_rule = input_rule
        if input_data and input_rule:
            pass
        else:
            raise ValueError('Both input_data and input_rule need values')

    def run(self):
        return meta.model_from_str(self.input_data + self.input_rule).value
