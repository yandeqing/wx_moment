#!/usr/bin/env python
# coding=utf-8
"""
@author: Zuber
@date:  2020/12/3 11:23
"""
import os
import re

from common import Logger
from config.AppConfig import MonitorConfig

config = MonitorConfig()


def get_add_friend_max_count():
    addFriendMaxCount = config.get_value('appiumConfig', 'addFriendMaxCount')
    Logger.println(f"【addFriendMaxCount={addFriendMaxCount}】")
    return addFriendMaxCount


def set_friend_max_count(addFriendMaxCount):
    return config.set_value('appiumConfig', 'addFriendMaxCount', addFriendMaxCount)


def getServerUrl():
    driver_server = config.get_value('appiumConfig', 'driver_server')
    Logger.println(f"【服务器地址={driver_server}】")
    return driver_server


def getPhoneExcel():
    phone_excel = config.get_value('appiumConfig', 'phone_excel')
    Logger.println(f"【手机号excel文件={phone_excel}】")
    return phone_excel


def setPhoneExcel(phone_excel):
    Logger.println(f"【设置手机号excel文件={phone_excel}】")
    phone_excel = config.set_value('appiumConfig', 'phone_excel', phone_excel)
    return phone_excel


def setServerUrl(server_url):
    return config.set_value('appiumConfig', 'driver_server', server_url)


def getAppiumConfig():
    deviceId = ''
    deviceVersion = ''
    try:
        # 读取设备 id
        readDeviceId = list(os.popen('adb devices').readlines())

        # 正则表达式匹配出 id 信息
        deviceId = re.findall(r'^\w*\b', readDeviceId[1])[0]
        # 读取设备系统版本号
        deviceAndroidVersion = list(
            os.popen('adb shell getprop ro.build.version.release').readlines())
        deviceVersion = re.findall(r'^\w*\b', deviceAndroidVersion[0])[0]
    except:
        pass

    appiumConfig = {
        "platformName": "Android",
        "deviceName": deviceId,
        "udid": deviceId,
        "platformVersion": deviceVersion,
        "appPackage": "com.tencent.mm",
        "appActivity": "com.tencent.mm.ui.LauncherUI",
        "noReset": "True",
        "unicodeKeyboard": "True",
        "resetKeyboard": "True"
    }
    return appiumConfig


# appiumConfig = {
#     "platformName": "Android",
#     "deviceName": "98882048434756494f",
#     "platformVersion": "7",
#     "appPackage": "com.tencent.mm",
#     "appActivity": "com.tencent.mm.ui.LauncherUI",
#     "noReset": "True",
#     "unicodeKeyboard": "True",
#     "resetKeyboard": "True"
# }

TIMEOUT = 10

USERNAME = "10"
PASSWORD = "10"

SCROLL_SLEEP_TIME = 3

if __name__ == '__main__':
    appium_config = getAppiumConfig()
    print(f"【().appium_config={appium_config}】")
