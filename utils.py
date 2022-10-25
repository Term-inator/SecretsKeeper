# -*- coding: utf-8 -*- 
""" 
@File : utils.py 
@Author: csc
@Date : 2022/8/15
"""


def hashUpdateDigest(hash_obj, string: str) -> str:
    """
    获取一个字符串的哈希值
    """
    hash_obj.update(string.encode(encoding='utf-8'))
    return hash_obj.hexdigest()


def getOnes(bits: int):
    """
    获取二进制数中 1 的数量
    """
    res = 0
    while bits > 0:
        res += (bits & 1)
        bits >>= 1
    return res
