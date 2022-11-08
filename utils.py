# -*- coding: utf-8 -*- 
""" 
@File : utils.py 
@Author: csc
@Date : 2022/8/15
"""
from typing import Dict

indexMap: Dict[str, int] = {
    'id': 0,
    'platform': 1,
    'username': 2,
    'note': 3,
    'password': 4
}


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


class Choice:
    question: str
    _default: bool

    def __init__(self, question: str, _default: bool = True):
        self.question = question
        self._default = _default

    def ask(self):
        left = 'Y' if self._default else 'y'
        right = 'n' if self._default else 'N'
        while True:
            choice = input(f'{self.question}[{left}/{right}]: ')
            if choice == '':
                return self._default
            elif choice == 'y' or choice == 'Y':
                return True
            elif choice == 'n' or choice == 'N':
                return False
