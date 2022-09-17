# -*- coding: utf-8 -*- 
""" 
@File : service.py 
@Author: csc
@Date : 2022/8/15
"""
from typing import Dict

import repository
import utils


class Password:
    length: int
    strength_level: int  # 小写字母，大写字母，数字，符号 0b1111
    ban_char: Dict[str]

    def __init__(self, length: int = 10, strength_level: int = 0b1111, ban_char: Dict[str] = None):
        self.length = length
        self.strength_level = strength_level
        self.ban_char = ban_char




class Service:
    database = None
    repo = None

    def _reset(self):
        self.database = None
        self.repo = None

    def logout(self):
        # TODO encode & write
        self._reset()

    def login(self, key1, key2):
        print('login')
        try:
            self.database = repository.Database()
            self.database.setKey(key1, key2)
            self.repo = repository.Repository(self.database)
            return True
        except ValueError:
            return False

    def generatePassword(self, length: int = 10, strength_level: int = 0b1111, ban_char: Dict[str] = None):
        pass

    def addPassword(self, identifier, password, note=None):
        pass

    def removePassword(self, identifier):
        pass

    def searchPassword(self, identifier: str = None, url: str = None, note: str = None):
        return self.repo.query(identifier=identifier)

    def recallId(self, note):
        pass

    def ls(self):
        for identifier in self.repo.data:
            print('\t'.join(self.repo.data[identifier][:3]))


service = Service()
