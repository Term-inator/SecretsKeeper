# -*- coding: utf-8 -*- 
""" 
@File : service.py 
@Author: csc
@Date : 2022/8/15
"""
import repository
import utils

repo = repository.Repository()
buffer = repository.Buffer(repo)


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
