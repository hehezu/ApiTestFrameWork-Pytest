#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：ApiTestFrameWork-Pytest 
@File    ：wechat_auto_send.py 自动打开桌面微信的一个程序
@Author  ：hehezu
@Date    ：2022/2/15 11:00 
'''
import pyautogui
import time
import pyperclip
from date import countdown


def openWechat():
    pyautogui.hotkey("ctrl", "alt", "w")
    time.sleep(1)


# TODO 定义一个查询联系人的函数，参数为name
def chatWho(name):
    # TODO 使用hotkey函数，操作按钮“command”，“f”，打开搜索
    pyautogui.hotkey("ctrl", "f")
    # TODO 使用pyperclip模块的copy函数，复制微信号name到剪贴板
    pyperclip.copy(name)
    # TODO 使用hotkey函数，操作按钮“command”，“v”，粘贴微信号
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    # TODO 使用hotkey函数，操作按钮“enter”，确认搜索
    pyautogui.hotkey("enter")
    time.sleep(2)

def sentMsg(msg):
    pyperclip.copy(msg)
    pyautogui.hotkey("ctrl","v")
    pyautogui.hotkey("enter")

# 调用OpenWechat()函数打开桌面微信
openWechat()
# TODO 调用chatWho(name)函数查找联系人
chatWho("文件传输助手")
sentMsg(f"{countdown()}")

