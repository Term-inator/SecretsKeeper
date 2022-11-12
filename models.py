# -*- coding: utf-8 -*- 
""" 
@File : models.py 
@Author: csc
@Date : 2022/11/9
"""
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "secrets.db")

from peewee import *

db = SqliteDatabase(db_path, pragmas=[('foreign_keys', 'on')])
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


# 用于登录
class User(BaseModel):
    id = AutoField()
    key = TextField()


class Secret(BaseModel):
    id = AutoField()
    platform = BlobField()
    username = BlobField()
    note = BlobField(null=True)
    password = BlobField()
    create_time = DateTimeField()
    update_time = DateTimeField()


class Encrypt(BaseModel):
    id = AutoField()
    secret_id = IntegerField()
    key = BlobField()
    nonce = BlobField()
    tag = BlobField()


if __name__ == '__main__':
    User.create_table()
    Secret.create_table()
    Encrypt.create_table()
