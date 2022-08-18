# -*- coding: utf-8 -*- 
""" 
@File : repository.py 
@Author: csc
@Date : 2022/8/15
"""
from typing import Dict, List, Tuple

import yaml
import os

os.chdir(os.path.split(os.path.realpath(__file__))[0])

from Cryptodome.Hash import BLAKE2b
from Cryptodome.Cipher import AES
from copy import deepcopy
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
    data: Dict[str, List[str]]
    identifier: int

    def __init__(self, database):
        self.data, self.identifier = database.toRepository()
        self.identifier += 1

    def insertPassword(self, url: str, password: str, note: str = ''):
        # TODO check existence
        self.data[str(self.identifier)] = [str(self.identifier), url, note, password]
        self.identifier += 1

    def _getPasswordById(self, identifier: str) -> str:
        return self.data[identifier][-1]

    def _getIdByUrl(self, url: str) -> List[str]:
        res = []
        for identifier in self.data:
            if self.data[identifier][1].find(url) != -1:
                res.append(identifier)
        return res

    def _getIdByNote(self, note: str) -> List[str]:
        res = []
        for identifier in self.data:
            if self.data[identifier][2].find(note) != -1:
                res.append(identifier)
        return res

    def query(self, identifier: str = None, url: str = None, note: str = None):
        ids = set()
        if identifier:
            ids.add(identifier)
        if url:
            _ids = self._getIdByUrl(url)
            for i in _ids:
                ids.add(i)
        if note:
            _ids = self._getIdByNote(note)
            for i in _ids:
                ids.add(i)
        res = []
        for identifier in ids:
            res.append(self._getPasswordById(identifier))
        return res


class Database:
    keys: List[List[str]] = []
    values: List[List[str]] = []
    plaintext1: str = ''
    plaintext2: str = ''
    ciphertext1: bytes = b''
    ciphertext2: bytes = b''
    key1: bytes = b''
    key2: bytes = b''

    def __init__(self):
        self.backup()

    def setKey(self, key1: str, key2: str):
        self.key1 = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), key1).encode()
        self.key2 = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), key2).encode()

    def read(self) -> None:
        with open(config['key_filename'], 'rb') as f:
            self.ciphertext1 = f.read()
        with open(config['value_filename'], 'rb') as f:
            self.ciphertext2 = f.read()

    def write(self) -> None:
        if self.check():
            print(self.ciphertext1)
            with open(config['key_filename'], 'wb') as f:
                f.write(self.ciphertext1)
            with open(config['value_filename'], 'wb') as f:
                f.write(self.ciphertext2)
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
        data1 = list2dToStr(self.keys).encode(encoding='utf-8')
        data2 = list2dToStr(self.values).encode(encoding='utf-8')

        self.ciphertext1, nonce1, tag1 = encode(self.key1, data1)
        self.ciphertext2, nonce2, tag2 = encode(self.key2, data2)

        config['nonce1'] = nonce1
        config['nonce2'] = nonce2
        config['tag1'] = tag1
        config['tag2'] = tag2
        writeConfig()
        self.write()

    def decode(self):
        self.read()
        if len(self.ciphertext1) == 0 or len(self.ciphertext2) == 0:
            return
        plaintext1 = decode(self.key1, self.ciphertext1, config['nonce1'], config['tag1'])
        plaintext2 = decode(self.key2, self.ciphertext2, config['nonce2'], config['tag2'])
        self.plaintext1 = plaintext1.decode()
        self.plaintext2 = plaintext2.decode()
        print(plaintext1)
        print(plaintext2)
        for key in self.plaintext1.split('\n'):
            self.keys.append(key.split(','))
        for val in self.plaintext2.split('\n'):
            self.values.append(val.split(','))
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
        print("The message is authentic")
        return plaintext
    except ValueError:
        print("Key incorrect or message corrupted")
        return None
