#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''
# from pymongo import MongoClient
import threading
from time import sleep, time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from common import time_util, time_util, excel_util, Logger, FilePathUtil
from common.LogUtil import LogUtil
from config.AppConfig import MonitorConfig
from wxfriend import wx_stop, WxUploader, WxConfig
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.config = MonitorConfig()
        self.md5_contents = []
        full_dir = FilePathUtil.get_lastmodify_file(
            FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
        array = excel_util.excel2array(full_dir)
        if array:
            for item in array:
                self.md5_contents.append(item['content_md5'])

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        sleep(15)
        el2 = self.wait_find_element(By.XPATH, "//*[@text='发现']")
        el2.click()
        el3 = self.wait_find_element(By.XPATH, "//*[@text='朋友圈']")
        el3.click()
        sleep(3)

    def crawl(self):
        self.enter()
        """
        爬取
        :return:
        """
        index = 0
        lastItem = None
        isFirst = True
        while True:
            if index > 0 and index % 56 == 0:
                self.driver.back()
                self.crawl()
                break
            if wx_stop.stopFlag:
                break
            # 上滑
            if not isFirst:
                self.swipe_up_slow()
            isFirst = False
            top_element = self.wait_find_element(By.XPATH,
                                                 '//android.support.v7.widget.LinearLayoutCompat')
            if lastItem and top_element:
                self.scrollElement(lastItem, top_element)
            sleep(3)
            items = self.wait_find_elements(By.XPATH,
                                            '//android.widget.ListView/android.widget.RelativeLayout')
            if items:
                lastItem = items[-1]
                for item in items:
                    index = index + 1
                    elment_datas = self.scan_all_text_elment(item)
                    LogUtil.info_jsonformat(elment_datas)

    def main(self):
        """
        入口
        :return:
        """
        # 爬取
        self.crawl()

    def main_backgroud(self):
        thread = threading.Thread(target=self.main)
        thread.start()


if __name__ == '__main__':
    moments = Moments()
    moments.main()
