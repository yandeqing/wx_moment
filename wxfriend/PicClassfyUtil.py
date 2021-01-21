#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''

import os
import shutil

from common import FilePathUtil, excel_util, Logger
from wxfriend import WxConfig


def execute_adb_shell(command, deviceId='98882048434756494f'):
    shell = f'adb -s {deviceId}  {command}'
    exe_shell(shell)


def getImiDefault():
    shell = f' adb shell ime list -a'
    Logger.println(f"【exec_shell().shell={shell}】")
    linesStr = list(os.popen(shell).readlines())
    for line in linesStr:
        Logger.println(f"{line}")
        if 'IME' in line:
            replace = line.replace(':', '')
            Logger.println(f"【().找到默认输入法:{replace}】")
            return replace


def setImiDefault():
    default = getImiDefault()
    shell = f' adb shell ime set {default}'
    Logger.println(f"【exec_shell().shell={shell}】")
    linesStr = list(os.popen(shell).readlines())
    for line in linesStr:
        Logger.println(f"{line}")
        if 'IME' in line:
            replace = line.replace(':', '')
            Logger.println(f"【().已经恢复默认输入法:{replace}】")
            return replace


def exe_shell(shell):
    Logger.println(f"【exec_shell().shell={shell}】")
    linesStr = list(os.popen(shell).readlines())
    for line in linesStr:
        Logger.println(f"{line}")


def stop_server():
    shell = f'adb kill-server'
    Logger.println(f"【exec_shell().shell={shell}】")
    exe_shell(shell)


def start_server():
    shell = f'adb start-server '
    Logger.println(f"【exec_shell().shell={shell}】")
    exe_shell(shell)


def export():
    full_dir = FilePathUtil.get_full_dir('wxfriend', 'pic')
    weixinPath = FilePathUtil.get_full_dir('wxfriend', 'pic', 'WeiXin')
    if os.path.exists(weixinPath):
        try:
            shutil.rmtree(weixinPath)
        except:
            pass
    deviceId = WxConfig.getAppiumConfig()["deviceName"]
    if deviceId:
        execute_adb_shell(f'pull /sdcard/Pictures/WeiXin/ {full_dir}', deviceId=deviceId)
    else:
        Logger.println(f"【().未找到设备】")


def classify(full_dir):
    # 2.excel获取朋友圈所有说说的md5以及图片的保存起始时间值
    Logger.println(f"【().full_dir={full_dir}】")
    array = excel_util.excel2array(full_dir)
    count = 0
    for index, item in enumerate(array):
        content_md5 = item['content_md5']
        start = int(item['start'])
        end = int(item['end'])
        count = int(item['count'])
        if count > 0:
            # Logger.println(f"【classify().item={item}】")
            # 3.根据起始时间值以及md5值分类好图片
            full_dir = FilePathUtil.get_full_dir('wxfriend', 'pic', 'WeiXin')
            des_dir = FilePathUtil.get_full_dir('wxfriend', 'pic', 'WeiXinCopy', content_md5)
            files = FilePathUtil.move_files_by_time(full_dir, des_dir, start, end)
            # Logger.println(f"【{content_md5}(图片数量={count},实际图片数量={len(files)}】")
    # startfile(FilePathUtil.get_full_dir('wxfriend', 'pic'))


def main():
    # 1.手机导出微信相册
    export()
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
    classify(full_dir)


def deletePictures():
    Logger.println(f"【deletePictures===========开始删除手机图片缓存========================】")
    deviceId = WxConfig.getAppiumConfig()["deviceName"]
    if deviceId:
        execute_adb_shell('shell rm -r /sdcard/Pictures/WeiXin',deviceId=deviceId)
    Logger.println(f"【deletePictures===========删除图片缓存执行完成=================】")


if __name__ == '__main__':
    # setImiDefault()
    # if __name__ == '__main__':
    # main()
    # execute_adb_shell('rm -r /sdcard/Pictures/WeiXin')
    export()
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
    classify(full_dir)
