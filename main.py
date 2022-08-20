# -*- coding: utf-8 -*- 
""" 
@File : main.py 
@Author: csc
@Date : 2022/8/20
"""
from typing import List, Dict

import command

command_list: List[command.Command] = [command.LoginCmd(), command.LogoutCmd(), command.LsCmd()]


class CLI:
    command_map: Dict[str, command.Command] = {}

    def __init__(self):
        for cmd in command_list:
            self.command_map[cmd.name] = cmd
            for alias in cmd.alias:
                self.command_map[alias] = cmd

    def run(self):
        while True:
            cmd_str = input('>>> ')
            tmp = cmd_str.strip().split()
            cmd_name = tmp[0]
            params = None
            if len(tmp) > 1:
                params = tmp[1:]
            print(cmd_name, params)
            if cmd_name in self.command_map:
                cmd = self.command_map[cmd_name]
                cmd.execute(params)
                if isinstance(cmd, command.LogoutCmd):
                    break
            else:
                print('Unknown command')


if __name__ == '__main__':
    cli = CLI()
    cli.run()
