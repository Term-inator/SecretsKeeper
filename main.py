# -*- coding: utf-8 -*- 
""" 
@File : main.py 
@Author: csc
@Date : 2022/8/20
"""
import threading
import ctypes
from time import sleep
from typing import List, Dict
from rich.console import Console

import command
from service import service

command_list: List[command.Command] = [command.LoginCmd(), command.LogoutCmd(), command.ExitCmd(), command.LsCmd()]


class TimeChecker(threading.Thread):
    name: str
    time: int
    unit: int
    timer: int = 0
    start_timer: bool = False
    inactive: bool = False

    def __init__(self, name: str, time: int, unit: int):
        threading.Thread.__init__(self)
        self.name = name
        self.time = time
        self.unit = unit

    def initTimer(self):
        self.inactive = False
        self.resetTimer()

    def clearTimer(self):
        self.timer = 0

    def startTimer(self):
        self.start_timer = True

    def resetTimer(self):
        self.start_timer = False
        self.clearTimer()

    def run(self) -> None:
        while True:
            sleep(self.unit)
            if self.start_timer:
                self.timer += self.unit
                if self.timer >= self.time:
                    self.inactive = True
                    self.resetTimer()


class CLI:
    console = Console()
    command_map: Dict[str, command.Command] = {}
    time_checker: TimeChecker
    is_login: bool = False

    def __init__(self, time_checker):
        self.time_checker = time_checker
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

    def logout(self):
        self.is_login = False
        service.logout()

    def run(self) -> None:
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
                print(self.is_login, self.time_checker.inactive)
                cmd = self.command_map[cmd_name]
                if isinstance(cmd, command.ExitCmd):
                    cmd.execute(params)
                    break
                if not self.is_login or self.time_checker.inactive:
                    if isinstance(cmd, command.LoginCmd):
                        res = cmd.execute(params)
                        if res:
                            self.is_login = True
                            self.time_checker.initTimer()
                            self.time_checker.startTimer()
                        else:
                            self.logout()
                    else:
                        print('Please login')
                else:
                    if not isinstance(cmd, command.LoginCmd):
                        self.time_checker.clearTimer()
                        cmd.execute(params)
                        if isinstance(cmd, command.LogoutCmd):
                            self.logout()
            else:
                print('Unknown command')


if __name__ == '__main__':
    time_checker = TimeChecker("timer", 60, 1)
    time_checker.start()
    cli = CLI(time_checker)
    cli.run()
    time_checker.join()
