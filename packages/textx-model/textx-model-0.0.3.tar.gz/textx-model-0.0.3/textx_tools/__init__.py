# -*- coding: UTF-8 -*-
# @Time : 2022/5/16 01:20 
# @Author : 刘洪波


def dict_to_str(data: dict):
    def deal(key, value):
        if isinstance(value, str):
            return key + " = " + "'" + value + "'"
        elif isinstance(value, int) or isinstance(value, bool):
            return key + " = " + str(value)
        elif isinstance(value, list):
            return key + " = '[" + ','.join(str(v) for v in value) + "]'"
        elif isinstance(value, dict) or isinstance(value, set) or isinstance(value, tuple):
            raise ValueError('data type is not in (str, int, bool, list)')
    return ';'.join([deal(k, v) for k, v in data.items()]) + ';'
