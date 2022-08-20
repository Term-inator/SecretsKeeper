# -*- coding: utf-8 -*- 
""" 
@File : service.py 
@Author: csc
@Date : 2022/8/15
"""
import repository
import utils


class Service:
    database = None
    repo = None

    def login(self, key1, key2):
        print('login')
        self.database = repository.Database()
        self.database.setKey(key1, key2)
        self.repo = repository.Repository(self.database)

    def generatePassword(self, length=10, char_type=4):
        pass

    def addPassword(self, identifier, password, note=None):
        pass

    def removePassword(self, identifier):
        pass

    def searchPassword(self, identifier: str = None, url: str = None, note: str = None):
        return self.repo.query(identifier=identifier)

    def recallId(self, note):
        pass

    def ls(self):
        for identifier in self.repo.data:
            print('\t'.join(self.repo.data[identifier][:3]))


service = Service()
