#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''

import os
import threading

from common import FilePathUtil, excel_util, Logger
from common.FilePathUtil import startfile
from wxfriend import WxConfig


def exec_shell(command, deviceId='98882048434756494f'):
    shell = f'adb -s {deviceId}  {command}'
    exe_shell(shell)


def exe_shell(shell):
    Logger.println(f"【exec_shell().shell={shell}】")
    linesStr = list(os.popen(shell).readlines())
    for line in linesStr:
        Logger.println(f"{line}")


def stop_server():
    shell = f'adb kill-server'
    Logger.println(f"【exec_shell().shell={shell}】")
    exe_shell(shell)


def export():
    full_dir = FilePathUtil.get_full_dir('wxfriend', 'pic')
    deviceId = WxConfig.getAppiumConfig()["deviceName"]
    if deviceId:
        exec_shell(f'pull /sdcard/Pictures/WeiXin/ {full_dir}', deviceId=deviceId)
    else:
        Logger.println(f"【().未找到设备】")


def main():
    # 1.手机导出微信相册
    export()
    # 2.excel获取朋友圈所有说说的md5以及图片的保存起始时间值
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
    sheetname = os.path.basename(full_dir)[0:8]
    Logger.println(f"【().full_dir={full_dir}】")
    Logger.println(f"【().file={sheetname}】")
    array = excel_util.excel2array(full_dir, sheetname)
    count = 0
    for index, item in enumerate(array):
        content_md5 = item['content_md5']
        start = int(item['start'])
        end = int(item['end'])
        Logger.println(f"【().item={item}】")
        # 3.根据起始时间值以及md5值分类好图片
        full_dir = FilePathUtil.get_full_dir('wxfriend', 'pic', 'WeiXin')
        des_dir = FilePathUtil.get_full_dir('wxfriend', 'pic', 'WeiXinCopy', content_md5)
        Logger.println(FilePathUtil.move_files_by_time(full_dir, des_dir, start, end))
    startfile(FilePathUtil.get_full_dir('wxfriend', 'pic'))


if __name__ == '__main__':
    main()
