# -*- coding: utf-8 -*- 
""" 
@File : utils.py 
@Author: csc
@Date : 2022/8/15
"""


def hashUpdateDigest(hash_obj, string: str) -> str:
    """
    get a hashcode of a string
    :param hash_obj:
    :param string: source
    :return: a hashcode
    """
    hash_obj.update(string.encode(encoding='utf-8'))
    return hash_obj.hexdigest()
