# -*- coding: utf-8 -*- 
""" 
@File : service.py 
@Author: csc
@Date : 2022/8/15
"""
import repository
import utils


def generatePassword(length=10, char_type=4):
    pass


def addPassword(identifier, password, note=None):
    pass


def removePassword(identifier):
    pass


def searchPassword(identifier):
    pass


def recallId(note):
    pass


def register(key):
    repository.register(utils.hash_sha3_512(key))


def authenticate(key):
    return repository.login(utils.hash_sha3_512(key))
