#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import json
import os
import threading
import time
from urllib import request

import requests
from PyQt5.QtCore import pyqtSignal
from qiniu import put_file

from common import FilePathUtil, excel_util, time_util, Logger
from wxfriend import wx_stop, WxConfig


def files_token(type='file', count=1):
    res = requests.get(f"http://internal.zuker.im/files/token?type={type}&count={count}")
    res_json = res.json()
    jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
    Logger.println(f"【files_token().jsonstr={jsonstr}】")
    if res_json['code'] == 0:
        return res_json['result']
    else:
        return None


def upload_file(token, file):
    # 要上传文件的本地路径
    ret, info = put_file(token, None, file)
    return ret


def download(signals: pyqtSignal = None):
    url = WxConfig.getAppDownloadUrl()
    download_address = FilePathUtil.get_full_dir('dist', 'window_main.exe')
    if os.path.exists(download_address):
        os.remove(download_address)
    downloadFile(download_address, url, signals)
    return FilePathUtil.get_full_dir('dist')


def download_resources():
    url = WxConfig.getAppDownloadUrl()
    download_address = FilePathUtil.get_full_dir('dist', 'window_main_resources.zip')
    if os.path.exists(download_address):
        os.remove(download_address)
    downloadFile(download_address, url)
    return FilePathUtil.get_full_dir('dist')


def downloadFile(name, url, signals: pyqtSignal = None):
    headers = {'Proxy-Connection': 'keep-alive'}
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    f = open(name, 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 >1:
                p = count / length * 100
                speed = (count - count_tmp) / 1024 / 1024 / 2
                count_tmp = count
                Logger.println(f'已下载 {formatFloat(p)}% (下载速度:{formatFloat(speed)}M/s)')
                time1 = time.time()
                if signals:
                    signals.emit(f'已下载 {formatFloat(p)}% (下载速度:{formatFloat(speed)}M/s)')
    signals.emit(f'已下载 {formatFloat(100)}%')
    f.close()


def formatFloat(num):
    return '{:.2f}'.format(num)


# 打开文件夹
def startfile(filename):
    try:
        os.startfile(filename)
    except:
        os.subprocess.Popen(['xdg-open', filename])


def upload():
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("dist"))
    token = files_token()
    filepath = upload_file(token[0], full_dir)
    print(f"【().filepath={filepath}】")


if __name__ == '__main__':
    upload()
    # download()
