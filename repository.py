# -*- coding: utf-8 -*- 
""" 
@File : repository.py 
@Author: csc
@Date : 2022/8/15
"""
from typing import Dict, List, Tuple

import yaml
import os
from copy import deepcopy

from exception import RecoverException

os.chdir(os.path.split(os.path.realpath(__file__))[0])

from Cryptodome.Hash import BLAKE2b
from Cryptodome.Cipher import AES
from copy import deepcopy
from threading import Thread
import utils

config = {}


def readConfig():
    global config
    with open('config.yml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    print(123)
    print(config)


readConfig()


def writeConfig():
    with open('config.yml', 'w') as f:
        yaml.dump(config, f)


class Repository:
    # id, [id, platform, username, note, password]
    data: Dict[str, List[str]]
    identifier: int

    def __init__(self, database):
        self.data, self.identifier = database.toRepository()
        self.identifier += 1

    def _getRecordById(self, identifier: str):
        return self.data[identifier]

    def getAllRecords(self):
        return self.data

    def insertPassword(self, platform: str, username: str, password: str, note: str = ''):
        # 检查冲突
        if self.data.get(str(self.identifier)) is not None:
            self.fixIdentifier()

        self.data[str(self.identifier)] = [str(self.identifier), platform, username, note, password]
        self.identifier += 1

    def _getPasswordById(self, identifier: str) -> str:
        return self.data[identifier][utils.indexMap['password']]

    def _getIdBy(self, key: str, value: str):
        if key not in utils.indexMap:
            raise KeyError(f'{key} is not in indexMap.')
        res = []
        for identifier in self.data:
            if self.data[identifier][utils.indexMap[key]].find(value) != -1:
                res.append(identifier)
        return res

    def query(self, identifier: str = None, platform: str = None, username: str = None, note: str = None):
        ids = set()
        if identifier:
            ids.add(identifier)
        if platform:
            _ids = self._getIdBy('platform', platform)
            for i in _ids:
                ids.add(i)
        if username:
            _ids = self._getIdBy('username', username)
            for i in _ids:
                ids.add(i)
        if note:
            _ids = self._getIdBy('note', note)
            for i in _ids:
                ids.add(i)
        res = []
        for identifier in ids:
            res.append(self._getRecordById(identifier))
        print(res)
        res.sort(key=lambda x: int(x[utils.indexMap['id']]))
        return deepcopy(res)

    def fixIdentifier(self) -> None:
        """
        修复潜在的 identifier 冲突问题
        :return:
        """
        pre_identifier = self.identifier

        res = 0
        for identifier in self.data:
            res = max(res, identifier)
        self.identifier = res + 1

        raise RecoverException(f'Duplicate identifier {pre_identifier}. Change to {self.identifier}')

    def toDataBase(self) -> Tuple[List[List[str]], List[List[str]]]:
        keys = []
        values = []
        for _key in self.data:
            data = self.data[_key]
            key = [_key, data[utils.indexMap['platform']], data[utils.indexMap['username']], data[utils.indexMap['note']]]
            value = [_key, data[utils.indexMap['password']]]
            keys.append(key)
            values.append(value)

        return keys, values


class Database:
    keys: List[List[str]]
    values: List[List[str]]
    plaintext1: str = ''
    plaintext2: str = ''
    ciphertext1: bytes = b''
    ciphertext2: bytes = b''
    key1: bytes = b''
    key2: bytes = b''

    def __init__(self):
        self.keys = []
        self.values = []
        self.backup()

    def setKey(self, key1: str, key2: str):
        self.key1 = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), key1).encode()
        self.key2 = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), key2).encode()
        self.decode()

    def read(self) -> None:
        def readKeys():
            with open(config['key_filename'], 'rb') as f:
                self.ciphertext1 = f.read()

        def readValues():
            with open(config['value_filename'], 'rb') as f:
                self.ciphertext2 = f.read()

        t1 = Thread(target=readKeys)
        t2 = Thread(target=readValues)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def write(self) -> None:
        def writeKeys():
            with open(config['key_filename'], 'wb') as f:
                f.write(self.ciphertext1)

        def writeValues():
            with open(config['value_filename'], 'wb') as f:
                f.write(self.ciphertext2)

        if self.check():
            t1 = Thread(target=writeKeys)
            t2 = Thread(target=writeValues())
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            self.removeBackup()
        else:
            pass

    def check(self):
        return True

    def backup(self) -> None:
        pass

    def removeBackup(self):
        pass

    def encode(self):
        def encodeKeys():
            data1 = list2dToStr(self.keys).encode(encoding='utf-8')
            self.ciphertext1, nonce1, tag1 = encode(self.key1, data1)
            config['nonce1'] = nonce1
            config['tag1'] = tag1

        def encodeValues():
            data2 = list2dToStr(self.values).encode(encoding='utf-8')
            self.ciphertext2, nonce2, tag2 = encode(self.key2, data2)
            config['nonce2'] = nonce2
            config['tag2'] = tag2

        t1 = Thread(target=encodeKeys)
        t2 = Thread(target=encodeValues)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        writeConfig()
        self.write()

    def decode(self):
        def decodeKeys():
            plaintext1 = decode(self.key1, self.ciphertext1, config['nonce1'], config['tag1'])
            self.plaintext1 = plaintext1.decode()
            print(plaintext1)
            for key in self.plaintext1.split('\n'):
                self.keys.append(key.split(','))

        def decodeValues():
            plaintext2 = decode(self.key2, self.ciphertext2, config['nonce2'], config['tag2'])
            self.plaintext2 = plaintext2.decode()
            print(plaintext2)
            for val in self.plaintext2.split('\n'):
                self.values.append(val.split(','))

        self.read()
        if len(self.ciphertext1) == 0 or len(self.ciphertext2) == 0:
            return

        t1 = Thread(target=decodeKeys)
        t2 = Thread(target=decodeValues)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        if len(self.keys) != len(self.values):
            raise ValueError
        print(self.keys)
        print(self.values)

    def toRepository(self) -> Tuple[Dict[str, List[str]], int]:
        res = {}
        val_map = {}
        largest_id = 0
        for val in self.values:
            val_map[val[0]] = val
            largest_id = max(largest_id, int(val[0]))
        for key in self.keys:
            tmp = deepcopy(key)
            tmp.extend(val_map[key[0]][1:])
            res[key[0]] = tmp
        return res, largest_id

    def getKeys(self):
        return self.keys

    def getValues(self):
        return self.values


def list2dToStr(lst: List[List[str]]) -> str:
    list1d = []
    for item in lst:
        list1d.append(','.join(item))
    return '\n'.join(list1d)


def encode(key: bytes, plaintext: bytes) -> Tuple:
    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    return ciphertext, nonce, tag


def decode(key: bytes, ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes | None:
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        print('The message is authentic.')
        return plaintext
    except ValueError:
        raise ValueError('Key incorrect or message corrupted.')
