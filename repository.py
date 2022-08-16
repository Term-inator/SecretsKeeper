# -*- coding: utf-8 -*- 
""" 
@File : repository.py 
@Author: csc
@Date : 2022/8/15
"""
import yaml
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

from Cryptodome.Hash import SHA3_512
from Cryptodome.Cipher import AES

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


class Buffer:
    data: list

    def __init__(self, repository):
        self.data = repository.toBuffer()

    def insertPassword(self, identifier, password, note=''):
        print(1)
        pass

    def getPasswordById(self, identifier):
        pass

    def getIdByNote(self, identifier):
        pass


class Repository:
    keys: list
    values: list

    def __init__(self):
        self.backup()
        self.read()

    def read(self) -> None:
        with open(config['key_filename'], 'r', encoding='utf-8') as f:
            self.keys = f.readlines()
        with open(config['value_filename'], 'r', encoding='utf-8') as f:
            self.values = f.readlines()

    def write(self) -> None:
        if self.check():
            with open(config['key_filename'], 'w', encoding='utf-8') as f:
                f.write(self.keys.join('\n'))
            with open(config['value_filename'], 'w', encoding='utf-8') as f:
                f.write(self.keys.join('\n'))
            self.removeBackup()
        else:
            pass

    def check(self):
        pass

    def backup(self) -> None:
        pass

    def removeBackup(self):
        pass

    def encode(self):
        key = b'Sixteen byte key'
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

    def decode(self):
        pass

    def toBuffer(self):
        pass
