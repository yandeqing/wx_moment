#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''
import hashlib
import json
import re
# from pymongo import MongoClient
import threading
from time import sleep

from common import excel_util, time_util, FilePathUtil, Logger
from config.AppConfig import MonitorConfig
from wxfriend import wx_stop
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.config = MonitorConfig()
        self.wx_content_md5 = self.config.get_value("wx_content", "md5")

    def enter(self):
        """
        进入朋友圈
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

    def crawl(self):
        """
        爬取
        :return:
        """
        lastItem = None
        while True:
            if wx_stop.stopFlag:
                break
            top_element = self.find_element_by_id('com.tencent.mm:id/bp')
            if lastItem and top_element:
                self.scrollElement(lastItem, top_element)
            items = self.find_elements_by_id("com.tencent.mm:id/fn9")
            if items:
                for item in items:
                    accessibility_id = self.find_element_by_accessibility_id('头像', item)
                    if accessibility_id:
                        lastItem = accessibility_id
                    advise = self.scan_all_text_elment(driver=item)
                    dumps = json.dumps(advise, indent=4,ensure_ascii=False)
                    print(f"【crawl().dumps={dumps}】")


    def main(self):
        """
        入口
        :return:
        """
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()

    def main_backgroud(self):
        thread = threading.Thread(target=self.main)
        thread.start()


if __name__ == '__main__':
    moments = Moments()
    moments.main()
