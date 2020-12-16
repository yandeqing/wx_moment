#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''

# from pymongo import MongoClient
from time import sleep

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from common import excel_util, time_util, FilePathUtil
from config.AppConfig import MonitorConfig
from wxfriend.WxConfig import DRIVER_SERVER, \
    TIMEOUT
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.config = MonitorConfig()
        self.wx_content_md5 = self.config.get_value("wx_content", "md5_more")

    def enter(self):
        """
        进入朋友圈
        :return:
        """

    def main(self):
        """
        入口
        :return:
        """
        sleep(5)
        by_id = self.driver.find_element_by_id('com.tencent.mm:id/czl')
        el2 = by_id.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.RelativeLayout[3]')
        el2.click()
        sleep(3)
        el3 = self.driver.find_element_by_id('com.tencent.mm:id/f43')
        el3.click()
        sleep(3)

        while True:
            items = self.find_elements_by_id("com.tencent.mm:id/fn9")
            if items is None:
                continue
            for item in items:
                pass
            print(f"【crawl().item={items}】")
            self.swipe_up()
            sleep(5)


if __name__ == '__main__':
    moments = Moments()
    moments.main()
