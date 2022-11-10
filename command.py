# -*- coding: utf-8 -*- 
""" 
@File : command.py 
@Author: csc
@Date : 2022/8/20
"""
from typing import List, Dict, Callable
from enum import Enum
import pyperclip

import utils
from service import service


class Source(Enum):
    CLI = 0
    INPUT = 1


class Parameter:
    name: str
    description: str
    source: Source
    convert_func: Callable[[str], any]
    default_value: any
    check_func: Callable[[str], bool]

    def __init__(self, name: str, description: str, _type, source: Source,
                 default_value: any = None,
                 convert_func: Callable[[str], any] = None,
                 check_func: Callable[[str], bool] = (lambda x: True)):
        self.name = name
        self.description = description
        self.type = _type
        self.source = source
        self.convert_func = convert_func
        self.default_value = default_value
        self.check_func = check_func

    def _getName(self):
        return f'{"-" if self.source is Source.CLI else " "}{self.name}'

    def checkType(self, value: str | List[str] | None):
        if value is None:
            return True
        # 是 list 但 value 是 str 的话会转换成 list(str)
        if self.type is list:
            return True
        if type(value) is str:
            return True
        else:
            raise TypeError(f'{self._getName()} requires a {self.type.__name__}, not a {type(value).__name__}')

    def check(self, value: str | List[str] | None) -> bool:
        return self.checkType(value) and self.check_func(value)

    def convert(self, value: str | List[str] | None) -> any:
        if value is None:
            return self.default_value
        if self.convert_func is None:
            return value

        if type(value) == str:
            if self.type is list:
                value = [value]
            else:
                return self.convert_func(value)
        if type(value) == list:
            for i in range(len(value)):
                value[i] = self.convert_func(value[i])
            return value

    def help(self) -> None:
        if self.name != 'h':
            print(f'{self._getName()}: {self.type.__name__}\t|\t{self.description}')


class Command:
    name: str
    alias: List[str] = []
    params: List[Parameter] = []
    description: str

    def __init__(self):
        self.addParams([Parameter('h', 'help', bool, Source.CLI, False)])

    def addParams(self, params: List[Parameter]) -> None:
        res = []
        for param in self.params:
            res.append(param)
        for param in params:
            res.append(param)
        self.params = res

    def parseParams(self, params: Dict[str, str | bool | List[str]]) -> Dict[str, str | bool | List[str]]:
        _params = {}
        for param in self.params:
            if param.source is Source.CLI:
                value = params.get(param.name)
            else:
                value = input(f'{param.name}: ')
            if param.check(value):
                _params[param.name] = param.convert(value)

        return _params

    def help(self) -> None:
        print(f'{self.name}:')
        print(self.description)
        for param in self.params:
            param.help()

    def execute(self, params: Dict[str, str | bool | List[str]]):
        pass


class LoginCmd(Command):
    name = 'login'
    alias = []
    description = '登录'

    def __init__(self):
        super().__init__()

        self.addParams([
            Parameter('login key', '登录密码', str, Source.INPUT),
            Parameter('key', '秘钥', str, Source.INPUT)
        ])

    def execute(self, params: Dict[str, str | bool | List[str]]) -> bool:
        _params = self.parseParams(params)
        return service.login(_params['key'])


class LogoutCmd(Command):
    name = 'logout'
    alias = []
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
    alias = []
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
            Parameter('l', '密码长度', int, Source.CLI, 10, int),
            Parameter('s', '密码强度', int, Source.CLI, 0b1111, lambda x: int(x, 2), check_func=checkS),
            Parameter('b', '指定不使用某些字符', list, Source.CLI, None)
        ])

    def execute(self, params: Dict[str, str | bool | List[str]]):
        _params = self.parseParams(params)
        print(service.generatePassword(_params['l'], _params['s'], _params['b']))


class AddCmd(GenCmd):
    name = 'add'
    alias = []
    description = '新建一个 (平台名, 用户名, 备注) -> 密码 的映射'

    def __init__(self):
        super().__init__()

        self.addParams([
            Parameter('platform', '平台名', str, Source.INPUT),
            Parameter('username', '用户名', str, Source.INPUT),
            Parameter('note', '备注', str, Source.INPUT, default_value='')
        ])

    def execute(self, params: Dict[str, str | bool | List[str]]):
        _params = self.parseParams(params)
        while True:
            password = service.generatePassword(_params['l'], _params['s'], _params['b'])
            print(password)
            next_psd = utils.Choice('换一个?', False).ask()
            if not next_psd:
                break
        service.addPassword(_params['platform'], _params['username'], password, _params['note'])


class SearchCmd(Command):
    name = 'search'
    alias = []
    description = '搜索'

    def __init__(self):
        super().__init__()

        self.addParams([
            Parameter('p', '平台名', str, Source.CLI, default_value=None),
            Parameter('u', '用户名', str, Source.CLI, default_value=None),
            Parameter('n', '备注', str, Source.CLI, default_value=None)
        ])

    def execute(self, params: Dict[str, str | bool | List[str]]):
        _params = self.parseParams(params)
        records = service.searchRecord(platform=_params['p'], username=_params['u'], note=_params['n'])
        for record in records:
            print('\t'.join(record))
        identifier = input('选择一个 id: ')

        in_records = False
        for record in records:
            if record[utils.indexMap['id']] == identifier:
                in_records = True
                break

        if in_records:
            record = service.getPassword(identifier)[0]

            copy_to_clipboard = utils.Choice('复制到剪贴板?', True).ask()
            if copy_to_clipboard:
                print(record)
                pyperclip.copy(record[utils.indexMap['password']])
                print('\t'.join(record[:utils.indexMap['password']]))
            else:
                print('\t'.join(record))
