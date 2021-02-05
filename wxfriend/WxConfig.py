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


def get_add_friend_max_count():
    config = MonitorConfig()
    addFriendMaxCount = config.get_value('appiumConfig', 'addFriendMaxCount')
    Logger.println(f"【addFriendMaxCount={addFriendMaxCount}】")
    return addFriendMaxCount


def set_friend_max_count(addFriendMaxCount):
    config = MonitorConfig()
    config.set_value('appiumConfig', 'addFriendMaxCount', addFriendMaxCount)


def get_addfriend_inte_seconds():
    config = MonitorConfig()
    addfriend_inte_seconds = config.get_value('appiumConfig', 'addfriend_inte_seconds')
    Logger.println(f"【get_addfriend_inte_seconds={addfriend_inte_seconds}】")
    if not addfriend_inte_seconds:
        return '3600'
    return addfriend_inte_seconds


def get_crawl_max_count():
    config = MonitorConfig()
    crawl_max_count = config.get_value('appiumConfig', 'crawl_max_count')
    Logger.println(f"【crawl_max_count={crawl_max_count}】")
    if not crawl_max_count:
        return '100'
    return crawl_max_count


def set_crawl_max_count(crawl_max_count):
    config = MonitorConfig()
    config.set_value('appiumConfig', 'crawl_max_count', crawl_max_count)


def set_get_addfriend_inte_seconds(addfriend_inte_seconds):
    config = MonitorConfig()
    config.set_value('appiumConfig', 'addfriend_inte_seconds', addfriend_inte_seconds)


def getServerUrl():
    config = MonitorConfig()
    driver_server = config.get_value('appiumConfig', 'driver_server')
    Logger.println(f"【服务器地址={driver_server}】")
    return driver_server


def getPhoneExcel():
    config = MonitorConfig()
    phone_excel = config.get_value('appiumConfig', 'phone_excel')
    Logger.println(f"【手机号excel文件={phone_excel}】")
    return phone_excel


def setPhoneExcel(phone_excel):
    config = MonitorConfig()
    phone_excel = config.set_value('appiumConfig', 'phone_excel', phone_excel)
    return phone_excel


def getAppDownloadUrl():
    config = MonitorConfig()
    app_download_url = config.get_value('appiumConfig', 'app_download_url')
    Logger.println(f"【app_download_url={app_download_url}】")
    return app_download_url


def setAppDownloadUrl(app_download_url):
    config = MonitorConfig()
    phone_excel = config.set_value('appiumConfig', 'app_download_url', app_download_url)
    return phone_excel


def getAppexeReplaceDir():
    config = MonitorConfig()
    appexe_replace_dir = config.get_value('appiumConfig', 'appexe_replace_dir')
    Logger.println(f"【appexe_replace_dir={appexe_replace_dir}】")
    return appexe_replace_dir


def setAppexeReplaceDir(appexe_replace_dir):
    config = MonitorConfig()
    appexe_replace_dir = config.set_value('appiumConfig', 'appexe_replace_dir', appexe_replace_dir)
    return appexe_replace_dir


def setServerUrl(server_url):
    config = MonitorConfig()
    config.set_value('appiumConfig', 'driver_server', server_url)


##获取设备多台设备号列表
def getDeviceid():
    str_init = ' '
    all_info = os.popen('adb devices').readlines()
    print('adb devices 输出的内容是：', all_info)
    for i in range(len(all_info)):
        str_init += all_info[i]
    devices_name = re.findall('\n(.+?)\t', str_init, re.S)
    print('所有设备名称：\n', devices_name)
    return devices_name


def getAppiumConfig():
    deviceId = ''
    deviceVersion = ''
    try:
        # 读取设备 id
        # 正则表达式匹配出 id 信息
        deviceId = getDeviceid()[0]
        # readDeviceId = list(os.popen('adb devices').readlines())
        # deviceId = re.findall(r'^\w*\b', readDeviceId[1])[0]
        # 读取设备系统版本号
        deviceAndroidVersion = list(
            os.popen(f'adb -s {deviceId} shell getprop ro.build.version.release').readlines())
        deviceVersion = re.findall(r'^\w*\b', deviceAndroidVersion[0])[0]
    except Exception as e:
        Logger.println(f"get deviceAndroidVersion Exception【e={e}】")

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
    Logger.println(f"【appium_config={appiumConfig}】")
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

TIMEOUT = 30

USERNAME = "10"
PASSWORD = "10"

SCROLL_SLEEP_TIME = 3

if __name__ == '__main__':
    appium_config = getAppiumConfig()
    print(f"【().appium_config={appium_config}】")
