# -*- coding: utf-8 -*- 
""" 
@File : command.py 
@Author: csc
@Date : 2022/8/20
"""
from typing import List, Dict, Callable

import utils
from service import service


class Parameter:
    name: str
    description: str
    convert_func: Callable[[str], any]
    default_value: any
    check_func: Callable[[str], bool]

    def __init__(self, name: str, description: str, convert_func: Callable[[str], any], default_value,
                 check_func: Callable[[str], bool] = (lambda x: True)):
        self.name = name
        self.description = description
        self.convert_func = convert_func
        self.default_value = default_value
        self.check_func = check_func

    def check(self, value: str | List[str] | Dict[str, str] | None):
        return self.check_func(value)

    def convert(self, value: str | List[str] | Dict[str, str] | None):
        if value is None:
            return self.default_value

        if type(value) == str:
            return self.convert_func(value)
        elif type(value) == list:
            for i in range(len(value)):
                value[i] = self.convert_func(value[i])
            return value
        elif type(value) == dict:
            for key in value:
                value[key] = self.convert_func(value[key])
            return value


class Command:
    name: str
    alias: List[str] = []
    params: List[Parameter] = []

    def execute(self, params: Dict[str, str | bool | List[str]] = None):
        pass


class LoginCmd(Command):
    name = 'login'

    def execute(self, params: Dict[str, str | bool | List[str]] = None) -> bool:
        key1 = input('key1: ')
        key2 = input('key2: ')
        return service.login(key1, key2)


class LogoutCmd(Command):
    name = 'logout'

    def execute(self, params: Dict[str, str | bool | List[str]] = None):
        print('logout...')


class ExitCmd(Command):
    name = 'exit'

    def execute(self, params: Dict[str, str | bool | List[str]] = None):
        print('exiting...')


class LsCmd(Command):
    name = 'ls'

    def execute(self, params: Dict[str, str | bool | List[str]] = None):
        service.ls()


class GenCmd(Command):
    name = 'generate'
    alias = ['gen']

    def __init__(self):
        def checkS(x: str) -> bool:
            if x is None:
                return True
            if utils.getOnes(int(x, 2)) > 0:
                return True
            else:
                raise ValueError('-s at least has one 1.')

        self.params = [
            Parameter('l', 'length', int, 10),
            Parameter('s', 'strength level', lambda x: int(x, 2), 0b1111, check_func=checkS),
            Parameter('b', 'ban chars', str, None)
        ]

    def execute(self, params: Dict[str, str | bool | List[str]] = None):
        _params = {}
        for param in self.params:
            if param.check(params.get(param.name)):
                _params[param.name] = param.convert(params.get(param.name))
        print(service.generatePassword(_params['l'], _params['s'], _params['b']))
