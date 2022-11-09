# -*- coding: utf-8 -*- 
""" 
@File : models.py 
@Author: csc
@Date : 2022/11/9
"""
from peewee import *

db = SqliteDatabase('secrets.db', pragmas=[('foreign_keys', 'on')])
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Secret(BaseModel):
    id = AutoField()
    platform = TextField()
    username = TextField()
    note = TextField(null=True)
    password = TextField()
    create_time = DateTimeField()
    update_time = DateTimeField()


class Encrypt(BaseModel):
    id = AutoField()
    secret_id = ForeignKeyField(Secret, backref='encrypt')
    key = TextField()
    nounce = TextField()
    tag = TextField()


if __name__ == '__main__':
    Secret.create_table()
    Encrypt.create_table()
