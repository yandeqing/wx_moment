import json
import logging
import os
import threading
from datetime import datetime

from PyQt5.QtCore import pyqtSignal

# 开关
from common import DingDingSdk

debug = True
mSignal: pyqtSignal = None


def println(msg):
    import time
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not debug:
        return
    global mSignal
    if mSignal is None:
        print(f"{strftime} {msg}")
    else:
        mSignal.emit(strftime + str(msg))
    pass


def dingdingException(msg):
    DingDingSdk.send_message(f"朋友圈数据抓取出现异常:{msg}")


def init(signal: pyqtSignal = None):
    global mSignal
    mSignal = signal


if __name__ == "__main__":
    println("test")
