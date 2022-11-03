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

    def __init__(self, name: str, description: str, default_value,
                 convert_func: Callable[[str], any] = None,
                 check_func: Callable[[str], bool] = (lambda x: True)):
        self.name = name
        self.description = description
        self.convert_func = convert_func
        self.default_value = default_value
        self.check_func = check_func

    def check(self, value: str | List[str] | Dict[str, str] | None):
        if self.check_func is None:
            raise ValueError(f'Check failed. The check_func of param {self.name} is None.')
        return self.check_func(value)

    def convert(self, value: str | List[str] | Dict[str, str] | None):
        if value is None:
            return self.default_value
        if self.convert_func is None:
            return value

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
    description: str

    def __init__(self):
        self.addParams([Parameter('h', 'help', False)])

    def addParams(self, params: List[Parameter]):
        res = []
        for param in self.params:
            res.append(param)
        for param in params:
            res.append(param)
        self.params = res

    def help(self):
        print(f'{self.name}:')
        print(self.description)
        for param in self.params:
            if param.name != 'h':
                print(f'-{param.name}: {param.description}')

    def execute(self, params: Dict[str, str | bool | List[str]]):
        pass


class LoginCmd(Command):
    name = 'login'
    description = '登录'

    def execute(self, params: Dict[str, str | bool | List[str]]) -> bool:
        key1 = input('key1: ')
        key2 = input('key2: ')
        return service.login(key1, key2)


class LogoutCmd(Command):
    name = 'logout'
    description = '登出'

    def execute(self, params: Dict[str, str | bool | List[str]]):
        print('logout...')


class ExitCmd(Command):
    name = 'exit'
    description = '退出程序'

    def execute(self, params: Dict[str, str | bool | List[str]]):
        print('exiting...')


class LsCmd(Command):
    name = 'ls'
    description = '列出 key 文件的内容'

    def execute(self, params: Dict[str, str | bool | List[str]]):
        service.ls()


class GenCmd(Command):
    name = 'generate'
    alias = ['gen']
    description = '生成一个密码'

    def __init__(self):
        super().__init__()

        def checkS(x: str) -> bool:
            if x is None:
                return True
            if utils.getOnes(int(x, 2)) > 0:
                return True
            else:
                raise ValueError('-s at least has one 1.')

        self.addParams([
            Parameter('l', '密码长度', 10, int),
            Parameter('s', '密码强度', 0b1111, lambda x: int(x, 2), check_func=checkS),
            Parameter('b', '指定不使用某些字符', None)
        ])

    def execute(self, params: Dict[str, str | bool | List[str]]):
        _params = {}
        for param in self.params:
            if param.check(params.get(param.name)):
                _params[param.name] = param.convert(params.get(param.name))
        print(service.generatePassword(_params['l'], _params['s'], _params['b']))


class AddCmd(Command):
    name = 'add'
    description = '新建一个 (平台名, 用户名, 备注) -> 密码 的映射'

    def __init__(self):
        super().__init__()

    def execute(self, params: Dict[str, str | bool | List[str]]):
        platform = input('platform: ')
        username = input('username: ')
        note = input('note: ')
        length = int(input('length: '))
        strength_level = int(input('strength_level: '), 2)
        ban_char = input('ban_char: ').split()
        print(ban_char)
        if len(ban_char) == 0:
            ban_char = None
        while True:
            password = service.generatePassword(length, strength_level, ban_char)
            print(password)
            next = input('next password?[y/N]: ')
            if next != 'y':
                break

        print(platform, username, note, password)
