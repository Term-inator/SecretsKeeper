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
    # repo.getKeys().append(['123', 'adc', 'asd'])
    # repo.getKeys().append(['2', 'abc', 'fgh'])
    # repo.getValues().append(['2', 'jkl'])
    # repo.getValues().append(['123', 'efg'])
    database.encode()


def test_toRepository():
    print(database.toRepository())


def test_getPasswordById():
    print(repo.query(note='b'))


def test_password():
    password = service.Password()
    print(password.gen(strength_level=0b0001))
