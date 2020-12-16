import json
import logging
import os
import threading
from datetime import datetime

from PyQt5.QtCore import pyqtSignal

# 开关
debug = True
mSignal: pyqtSignal = None


def println(msg):
    if not debug:
        return
    global  mSignal
    if mSignal is None:
        print(msg)
    else:
        mSignal.emit(str(msg))
    pass


def init(signal: pyqtSignal = None):
    global mSignal
    mSignal = signal


if __name__ == "__main__":
    println("test")
