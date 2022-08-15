# -*- coding: utf-8 -*- 
""" 
@File : utils.py 
@Author: csc
@Date : 2022/8/15
"""
import hashlib


def hash_sha3_512(string):
    sha3 = hashlib.sha3_512()
    sha3.update(string.encode(encoding='utf-8'))
    return sha3.hexdigest()
