# -*- coding: UTF-8 -*-
# @Time : 2022/5/16 00:01 
# @Author : 刘洪波
from textx_model.Model import meta


class CaseWhenModel(object):
    def __init__(self, input_data: str, input_rule: str):
        self.input_data = input_data
        self.input_rule = input_rule
        if input_data and input_rule:
            pass
        else:
            raise ValueError('Both input_data and input_rule need values')

    def run(self):
        _when, tips = self.deal_case_when_rule(self.input_rule)
        model = meta.model_from_str(self.input_data + _when)
        result = tips.get(str(model.value).lower())
        return result

    @staticmethod
    def deal_case_when_rule(rule):
        _, _when = rule.split('when')
        _when, _then = _when.split('then')
        _when = _when.strip()
        _then, _else = _then.split('else')
        _then = _then.strip().strip("'")
        _else = _else.strip().strip("'")
        tips = {
            'true': _then,
            'false': _else
        }
        return _when, tips
