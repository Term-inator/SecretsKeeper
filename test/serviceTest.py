# -*- coding: utf-8 -*- 
""" 
@File : serviceTest.py 
@Author: csc
@Date : 2022/8/15
"""
import pytest
import service
from Cryptodome.Hash import SHA3_224
import utils


def test_hash():
    key = utils.hashUpdateDigest(SHA3_224, '123456ab')
    print(key)
