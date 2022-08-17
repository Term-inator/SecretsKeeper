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
    data: list

    def __init__(self, database):
        self.data = database.toRepository()

    def insertPassword(self, identifier, password, note=''):
        print(1)
        pass

    def getPasswordById(self, identifier):
        pass

    def getIdByNote(self, identifier):
        pass


class Database:
    keys: List[str]
    values: List[str]
    plaintext1: str
    plaintext2: str
    ciphertext1: bytes
    ciphertext2: bytes
    key1: bytes
    key2: bytes

    def __init__(self):
        self.backup()
        self.keys = []
        self.values = []
        self.plaintext1 = ''
        self.plaintext2 = ''
        self.ciphertext1 = b''
        self.ciphertext2 = b''
        self.key1 = b''
        self.key2 = b''

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
        data1 = '\n'.join(self.keys).encode(encoding='utf-8')
        data2 = '\n'.join(self.values).encode(encoding='utf-8')

        self.ciphertext1, nonce1, tag1 = encode(self.key1, data1)
        self.ciphertext2, nonce2, tag2 = encode(self.key2, data2)

        config['nonce1'] = nonce1
        config['nonce2'] = nonce2
        config['tag1'] = tag1
        config['tag2'] = tag2
        writeConfig()
        self.write()

    def decode(self, key1: str, key2: str):
        self.read()
        self.key1 = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), key1).encode()
        self.key2 = utils.hashUpdateDigest(BLAKE2b.new(digest_bits=128), key2).encode()
        if len(self.ciphertext1) == 0 or len(self.ciphertext2) == 0:
            return
        plaintext1 = decode(self.key1, self.ciphertext1, config['nonce1'], config['tag1'])
        plaintext2 = decode(self.key2, self.ciphertext2, config['nonce2'], config['tag2'])
        self.plaintext1 = plaintext1.decode()
        self.plaintext2 = plaintext2.decode()
        print(plaintext1)
        print(plaintext2)
        self.keys = self.plaintext1.split('\n')
        self.values = self.plaintext2.split('\n')
        print(self.keys)
        print(self.values)

    def toRepository(self):
        pass

    def getKeys(self):
        return self.keys

    def getValues(self):
        return self.values


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
