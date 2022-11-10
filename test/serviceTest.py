# -*- coding: utf-8 -*- 
""" 
@File : serviceTest.py 
@Author: csc
@Date : 2022/8/15
"""
import pytest
from Cryptodome.Cipher import AES

import service
from Cryptodome.Hash import SHA3_224, BLAKE2b
from Cryptodome.Random import get_random_bytes

import utils
from models import *


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


def test_encrypt_decrypt():
    key = get_random_bytes(32)
    # key = utils.hashUpdateDigest(BLAKE2b.new(digest_bytes=16), '123').encode()
    # print(len(key), len(key1))
    cipher = AES.new(key, AES.MODE_EAX, nonce=get_random_bytes(32))
    # cipher.update(b'header')
    data = ''
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    print(ciphertext)
    print(eval(str(tag)))

    cipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
    # cipher.update(jv['header'])
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    print("The message was: " + str(plaintext))
