# -*- coding: UTF-8 -*-
# @Time : 2022/5/15 22:19
# @Author : 刘洪波


def general_model(input_data, input_rule):
    from textx_model.General import GeneralModel
    return GeneralModel(input_data, input_rule)


def cs_model(input_data, input_rule):
    from textx_model.CaseWhen import CaseWhenModel
    return CaseWhenModel(input_data, input_rule)
