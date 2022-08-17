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


def test_encode_decode():
    repo = repository.Database()
    repo.decode('123456ab', 'ab123456')
    # repo.getKeys().append('123')
    # repo.getKeys().append('abc')
    # repo.getValues().append('456')
    # repo.getValues().append('efg')
    repo.encode()
