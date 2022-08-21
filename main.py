# -*- coding: utf-8 -*- 
""" 
@File : main.py 
@Author: csc
@Date : 2022/8/20
"""
from typing import List, Dict
from rich.console import Console

import command

command_list: List[command.Command] = [command.LoginCmd(), command.LogoutCmd(), command.LsCmd()]


class CLI:
    console = Console()
    command_map: Dict[str, command.Command] = {}

    def __init__(self):
        for cmd in command_list:
            self.command_map[cmd.name] = cmd
            for alias in cmd.alias:
                self.command_map[alias] = cmd

    def _parseParams(self, params: List[str]) -> Dict[str, str | bool]:
        res = {}
        n = len(params)
        for i in range(n):
            if params[i][0] == '-':
                param_name = params[i][1:]
                print(param_name)
                res[param_name] = True
                if i + 1 < n and params[i + 1][0] != '-':
                    res[param_name] = params[i + 1]
                    i += 2
        return res

    def run(self):
        while True:
            self.console.print('>>> ', style='blue', end='')
            cmd_str = input()
            tmp = cmd_str.strip().split()
            cmd_name = tmp[0]
            params = None
            if len(tmp) > 1:
                params = self._parseParams(tmp[1:])
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
