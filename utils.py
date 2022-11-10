# -*- coding: utf-8 -*- 
""" 
@File : utils.py 
@Author: csc
@Date : 2022/8/15
"""
from typing import Dict, Tuple

from Cryptodome.Cipher import AES


def hashUpdateDigest(hash_obj, string: str) -> str:
    """
    获取一个字符串的哈希值
    """
    hash_obj.update(string.encode(encoding='utf-8'))
    return hash_obj.hexdigest()


def encrypt(key: bytes, plaintext: str, nonce: bytes = None) -> Tuple[bytes, bytes, bytes]:
    plaintext = plaintext.encode()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    return ciphertext, nonce, tag


def decrypt(key: bytes, ciphertext: bytes, nonce: bytes, tag: bytes) -> str | None:
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        print('The message is authentic.')
        plaintext = plaintext.decode(encoding='utf-8')
        return plaintext
    except ValueError:
        raise ValueError('Key incorrect or message corrupted.')


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
