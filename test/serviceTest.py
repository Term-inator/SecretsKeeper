# -*- coding: utf-8 -*- 
""" 
@File : serviceTest.py 
@Author: csc
@Date : 2022/8/15
"""
import pytest
import service


def test_register():
    key = '123456ab'
    service.register(key)


def test_authenticate():
    key = '123456ab'
    assert service.authenticate(key)
    assert not service.authenticate(key + '1')
