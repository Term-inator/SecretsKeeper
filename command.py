# -*- coding: utf-8 -*- 
""" 
@File : command.py 
@Author: csc
@Date : 2022/8/20
"""
from typing import List

from service import service


class Command:
    name: str
    alias: List[str] = []

    def execute(self, params: List[str] = None):
        pass


class LoginCmd(Command):
    name = 'login'

    def execute(self, params: List[str] = None) -> bool:
        key1 = input('key1: ')
        key2 = input('key2: ')
        return service.login(key1, key2)


class LogoutCmd(Command):
    name = 'logout'

    def execute(self, params: List[str] = None):
        print('logout...')


class ExitCmd(Command):
    name = 'exit'

    def execute(self, params: List[str] = None):
        print('exiting...')


class LsCmd(Command):
    name = 'ls'

    def execute(self, params: List[str] = None):
        service.ls()
