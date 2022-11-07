# -*- coding: utf-8 -*- 
""" 
@File : service.py 
@Author: csc
@Date : 2022/8/15
"""
import random
from typing import Dict, Set, List

import repository
import utils


class Password:
    chars: Dict[int, List[int]] = {
        0b1000: [],
        0b0100: [],
        0b0010: [],
        0b0001: []
    }  # 待选字符集

    def __init__(self, ):
        strength_level = 0b1000
        while strength_level > 0:
            if strength_level == 0b1000:  # 符号
                tmp = [[33, 47], [58, 64], [91, 96], [123, 126]]
                for _range in tmp:
                    for i in range(_range[0], _range[1] + 1):
                        self.chars[strength_level].append(i)
            elif strength_level == 0b0100:  # 数字
                for i in range(48, 58):
                    self.chars[strength_level].append(i)
            elif strength_level == 0b0010:  # 大写字母
                for i in range(65, 91):
                    self.chars[strength_level].append(i)
            elif strength_level == 0b0001:  # 小写字母
                for i in range(97, 123):
                    self.chars[strength_level].append(i)
            strength_level >>= 1

    def checkBanChar(self, ban_char: List[str] = None) -> bool:
        """
        如果某一类字符集是 ban_char 的子集，返回 False
        """
        if ban_char is None:
            return True
        for key in self.chars:
            cnt = 0
            for char in self.chars[key]:
                if chr(char) in ban_char:
                    cnt += 1
            if cnt == len(self.chars[key]):
                return False
        return True

    def gen(self, length: int = 10, strength_level: int = 0b1111, ban_char: List[str] = None):
        """
        生成密码
        :param length: 密码长度
        :param strength_level: 符号，数字，大写字母，小写字母 0b1111
        :param ban_char: 排除一些字符
        :return:
        """
        if not self.checkBanChar(ban_char):
            raise ValueError('Ban too many chars.')

        one = utils.getOnes(strength_level)
        groups = [(strength_level >> i) & 1 for i in range(4)]

        group_map = {}
        index = 0
        for i in range(4):
            if groups[i] != 0:
                group_map[index] = i
                index += 1

        for i in range(length - one):
            tmp = random.randint(0, one * length)
            groups[group_map[tmp % one]] += 1

        char_lst = []
        for i in range(4):
            for j in range(groups[i]):
                level = 2**i
                while True:
                    char = chr(random.choice(self.chars[level]))
                    if ban_char is None or char not in ban_char:
                        break
                char_lst.append(char)
        random.shuffle(char_lst)

        return "".join(char_lst)


class Service:
    database: repository.Database = None
    repo: repository.Repository = None
    password_generator: Password = Password()

    def _reset(self):
        self.database = None
        self.repo = None

    def logout(self):
        if self.database is None and self.repo is None:
            return
        self.database.keys, self.database.values = self.repo.toDataBase()
        self.database.encode()
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

    def generatePassword(self, length: int = 10, strength_level: int = 0b1111, ban_char: List[str] = None):
        password = self.password_generator.gen(length, strength_level, ban_char)
        return password

    def addPassword(self, platform: str, username: str, password: str, note=None):
        self.repo.insertPassword(platform, username, password, note)
        print(f'platform: {platform}, username: {username}, password: {password}, note: {note}')

    def removePassword(self, identifier):
        pass

    def searchRecord(self, platform: str = None, username: str = None, note: str = None):
        """
        查找记录，不包含密码
        :param platform: 平台名
        :param username: 用户名
        :param note: 备注
        :return: 记录
        """
        records = self.repo.query(platform=platform, username=username, note=note)
        for i in range(len(records)):
            records[i].pop(utils.indexMap['password'])
        return records

    def getPassword(self, identifier: str):
        return self.repo.query(identifier=identifier)

    def ls(self):
        data = self.repo.getAllRecords()
        for identifier in data:
            print('\t'.join(data[identifier][:4]))


service = Service()
