# -*- coding: utf-8 -*- 
""" 
@File : serviceTest.py 
@Author: csc
@Date : 2022/8/15
"""
import pytest
from Cryptodome.Cipher import AES

import service
import repository
from Cryptodome.Hash import SHA3_224, BLAKE2b
import utils


database = repository.Database()
key1 = '123456ab'
key2 = 'ab123456'
database.setKey(key1, key2)
database.decode()
repo = repository.Repository(database)


def test_encode_decode():
    database.decode()
    repo.data['1'] = ['1', 'plt1', 'usr1', 'note1', 'psd1']
    repo.data['2'] = ['2', 'plt2', 'usr2', 'note2', 'psd2']
    database.keys, database.values = repo.toDataBase()
    database.encode()


def test_toRepository():
    print(database.toRepository())


def test_getPasswordById():
    print(repo.query(note='b'))


def test_password():
    password = service.Password()
    print(password.gen(strength_level=0b0001))
