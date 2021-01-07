#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''
import hashlib
import re
# from pymongo import MongoClient
import threading
from time import sleep

from common import excel_util, time_util, FilePathUtil, Logger
from config.AppConfig import MonitorConfig
from wxfriend import PicClassfyUtil
from wxfriend.PicClassfyUtil import stop_server, start_server
from wxfriend.wx_swipe_base import MomentsBase

stopFlag = False


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.config = MonitorConfig()

    def main(self):
        """
        入口
        :return:
        """
        # 执行adb断开
        stop_server()
        start_server()
        self.stop()

    def main_backgroud(self):
        thread = threading.Thread(target=self.main)
        thread.start()


if __name__ == '__main__':
    moments = Moments()
    moments.main()
