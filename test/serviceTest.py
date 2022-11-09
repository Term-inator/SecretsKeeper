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
from models import *

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


def test_sqlite():
    import datetime
    print(datetime.datetime.now())
    secret = Secret.create(platform='1', username='2', password='3', create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
    # for secret in Secret.select().where(Secret.platform == '1'):
    #     secret.delete_instance()
    encrypt = Encrypt.create(secret_id=secret, key='123456ab', nounce='4', tag='3')
