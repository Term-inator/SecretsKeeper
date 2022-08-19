# -*- coding: utf-8 -*- 
""" 
@File : service.py 
@Author: csc
@Date : 2022/8/15
"""
import click
import repository
import utils

database = repository.Database()
repo = None


@click.group()
@click.command()
def cli():
    print('CLI...')


@click.command()
# @click.argument('--key1')
# @click.argument('--key2')
def login(key1, key2):
    print(123)
    # database.setKey(key1, key2)
    # global repo
    # repo = repository.Repository(database)


def generatePassword(length=10, char_type=4):
    pass


def addPassword(identifier, password, note=None):
    pass


def removePassword(identifier):
    pass


@click.command()
@click.option('--id', default=None)
@click.option('--url', default=None)
@click.option('--note', default=None)
def searchPassword(identifier: str = None, url: str = None, note: str = None):
    return repo.query(identifier=identifier)


def recallId(note):
    pass


cli.add_command(login)


if __name__ == '__main__':
    cli()
