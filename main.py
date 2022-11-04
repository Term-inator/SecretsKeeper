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

command_list: List[command.Command] = [
    command.LoginCmd(),
    command.LogoutCmd(),
    command.ExitCmd(),
    command.LsCmd(),
    command.GenCmd(),
    command.AddCmd()
]


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

    def _parseParams(self, params: List[str]) -> Dict[str, str | bool | List[str]]:
        res = {}
        n = len(params)
        current_param = ''
        for i in range(n):
            if params[i][0] == '-':
                current_param = params[i][1:]
                print(current_param)
                res[current_param] = True
            else:
                if current_param != '':
                    if type(res[current_param]) is bool:
                        res[current_param] = params[i]
                    elif type(res[current_param]) is list:
                        res[current_param].append(params[i])
                    else:
                        res[current_param] = [res[current_param], params[i]]
                else:
                    raise RuntimeError("Invalid param style.")
        return res

    def logout(self):
        self.is_login = False
        service.logout()

    def run(self) -> None:
        while True:
            try:
                self.console.print('>>> ', style='blue', end='')
                cmd_str = input()
                tmp = cmd_str.strip().split()
                cmd_name = tmp[0]
                params = {}
                if len(tmp) > 1:
                    params = self._parseParams(tmp[1:])
                print(cmd_name, params)
                if cmd_name in self.command_map:
                    print(self.is_login, self.time_checker.inactive)
                    cmd = self.command_map[cmd_name]

                    # 帮助
                    if params.get('h') is not None:
                        cmd.help()
                        continue

                    # 退出
                    if isinstance(cmd, command.ExitCmd):
                        cmd.execute(params)
                        break
                    # 未登录 或 一段时间无操作
                    if not self.is_login or self.time_checker.inactive:
                        # 是登录命令
                        if isinstance(cmd, command.LoginCmd):
                            res = cmd.execute(params)
                            # 登陆成功
                            if res:
                                self.is_login = True
                                self.time_checker.initTimer()
                                self.time_checker.startTimer()
                            else:
                                self.logout()
                        else:
                            print('Please login')
                    else:
                        # 已登录情景，过滤登录命令
                        if not isinstance(cmd, command.LoginCmd):
                            self.time_checker.clearTimer()
                            cmd.execute(params)
                            # 登出命令
                            if isinstance(cmd, command.LogoutCmd):
                                self.logout()
                else:
                    print('Unknown command')
            except Exception as e:
                self.console.print(e, style='red')


if __name__ == '__main__':
    time_checker = TimeChecker("timer", 60, 1)
    time_checker.start()
    cli = CLI(time_checker)
    cli.run()
    time_checker.join()
