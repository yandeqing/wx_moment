#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/1/14 9:49
'''
import sys
import time

from common import Logger
from common.LogUtil import LogUtil


def m():
    return 1 / 0


def n():
    m()


def p():
    n()


def myExcepthook(ttype, tvalue, ttraceback):
    msg = f"【myExcepthook(异常内容).ttype={ttype}:{tvalue}】"
    Logger.dingdingException(f"应用出现闪退{msg}")
    LogUtil.info(msg)
    i = 1
    while ttraceback:
        tracebackCode = ttraceback.tb_frame.f_code
        LogUtil.info(
            f"第{i}层堆栈信息文件名：\n{tracebackCode.co_filename}\n函数或者模块名:{tracebackCode.co_name}")
        ttraceback = ttraceback.tb_next
        i += 1


def main():
    sys.excepthook = myExcepthook


if __name__ == '__main__':
    main()
    p()
    time.sleep(3)
    print("继续执行")
