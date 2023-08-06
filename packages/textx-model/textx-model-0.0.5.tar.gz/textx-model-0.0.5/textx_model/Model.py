# -*- coding: UTF-8 -*-
# @Time : 2021/11/18 上午11:29 
# @Author : 刘洪波
from __future__ import unicode_literals
from textx import metamodel_from_file
import os

namespace = {}


def str_to_list(str_data: str):
    str_data = str_data
    return str_data


class Model(object):
    def __init__(self, **kwargs):
        self.assignments = kwargs.pop('assignments')
        self.expression = kwargs.pop('expression')

    @property
    def value(self):
        # Evaluate variables in the order of definition
        for a in self.assignments:
            namespace[a.variable] = a.expression.value
        return self.expression.value


class ExpressionElement(object):
    def __init__(self, **kwargs):
        # textX will pass in parent attribute used for parent-child
        # relationships. We can use it if we want to.
        self.parent = kwargs.get('parent', None)
        # We have 'op' attribute in all grammar rules
        self.op = kwargs['op']

        super(ExpressionElement, self).__init__()


class Expression(ExpressionElement):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == 'in':
                tag = True
                if ret[0] == '[':
                    ret = ret.lstrip('[')
                    if ret[-1] == ']':
                        ret = ret.rstrip(']').split(',')
                        for r in ret:
                            if r not in operand.value:
                                tag = False
                                break
                        ret = tag
                    else:
                        ret = ret in operand.value
                else:
                    ret = ret in operand.value
            elif operation == 'and':
                ret = ret and operand.value
            elif operation == 'or':
                ret = ret or operand.value
            elif operation == 'not':
                ret = not operand.value
        return ret


class Compare(ExpressionElement):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '<':
                ret = ret < operand.value
            elif operation == '>':
                ret = ret > operand.value
            elif operation == '=':
                ret = ret == operand.value
            elif operation == '>=':
                ret = ret >= operand.value
            elif operation == '<=':
                ret = ret <= operand.value
            elif operation == '!=':
                ret = ret != operand.value
        return ret


class Not(ExpressionElement):
    def __init__(self, **kwargs):
        self._not = kwargs.pop('_not')
        super(Not, self).__init__(**kwargs)

    @property
    def value(self):
        ret = self.op.value
        return not ret if self._not else ret


class AddSub(ExpressionElement):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '+':
                ret += operand.value
            else:
                ret -= operand.value
        return ret


class Term(ExpressionElement):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '*':
                ret *= operand.value
            else:
                ret /= operand.value
        return ret


class Factor(ExpressionElement):
    def __init__(self, **kwargs):
        self.sign = kwargs.pop('sign', '+')
        super(Factor, self).__init__(**kwargs)

    @property
    def value(self):
        value = self.op.value
        return -value if self.sign == '-' else value


class Operand(ExpressionElement):
    @property
    def value(self):
        op = self.op
        if op in namespace:
            return namespace[op]
        elif type(op) in {int, float, bool, str}:
            return op
        elif isinstance(op, ExpressionElement):
            return op.value
        else:
            raise Exception('Unknown variable "{}" at position {}'
                            .format(op, self._tx_position))


this_file_path = os.path.realpath(__file__)
meta = metamodel_from_file(this_file_path[:-8] + 'Meta.tx',
                           classes=[Model, Expression, Not, Compare, AddSub, Term, Factor, Operand])
