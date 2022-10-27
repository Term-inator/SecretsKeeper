# -*- coding: utf-8 -*- 
""" 
@File : command.py 
@Author: csc
@Date : 2022/8/20
"""
from typing import List, Dict, Callable

from service import service


class Parameter:
    name: str
    convert_func: Callable[[str], any]

    def __init__(self, name: str, convert_func: Callable[[str], any], default_value):
        self.name = name
        self.convert_func = convert_func
        self.default_value = default_value

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
    name = 'gen'
    params = [
        Parameter('l', int, 10),
        Parameter('s', lambda x: int(x, 2), 0b1111),
        Parameter('b', str, None)
    ]

    def execute(self, params: Dict[str, str | bool | List[str]] = None):
        _params = {}
        for param in self.params:
            _params[param.name] = param.convert(params.get(param.name))
        print(service.generatePassword(_params['l'], _params['s'], _params['b']))
