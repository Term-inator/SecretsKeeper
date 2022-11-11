# -*- coding: utf-8 -*- 
""" 
@File : service.py 
@Author: csc
@Date : 2022/8/15
"""
import random
from functools import reduce
from typing import Dict, Set, List
from Cryptodome.Hash import BLAKE2b
from Cryptodome.Random import get_random_bytes
import datetime

from models import User, Secret, Encrypt
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
    key: bytes = b''
    password_generator: Password = Password()

    def logout(self):
        self.key = b''

    def login(self, password: str, key: str):
        print('login')
        password = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), password).encode()
        if not User.select().exists():
            User.create(password=password)
        else:
            if not User.select().where(User.password == password).exists():
                return False
        self.key = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), key).encode()
        return True

    def generatePassword(self, length: int = 10, strength_level: int = 0b1111, ban_char: List[str] = None):
        password = self.password_generator.gen(length, strength_level, ban_char)
        return password

    def addPassword(self, platform: str, username: str, password: str, note=''):
        key = get_random_bytes(32)

        secret_data = [platform, username, password, note]
        n = len(secret_data)
        nonces = [get_random_bytes(32) for i in range(n)]
        tags = [b'' for i in range(n)]
        for i in range(n):
            secret_data[i], _, tags[i] = utils.encrypt(key, secret_data[i], nonce=nonces[i])
            secret_data[i] = str(secret_data[i])

        # TODO 时间
        secret = Secret.create(platform=secret_data[0], username=secret_data[1], password=secret_data[2], note=secret_data[3],
                               create_time=datetime.datetime.now(), update_time=datetime.datetime.now())

        # TODO 加密 key nonce tag
        nonce = reduce(lambda x, y: x + y, nonces)
        tag = reduce(lambda x, y: x + y, tags)
        encrypt = Encrypt.create(secret_id=secret.id, key=key, nonce=nonce, tag=tag)
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
        query = (Secret.select(Secret, Encrypt).join(Encrypt, on=(Secret.id == Encrypt.secret_id)))
        print(query.sql())
        for item in query:
            # TODO 解密
            print(item.platform, item.username, item.password, item.encrypt.key)


service = Service()
