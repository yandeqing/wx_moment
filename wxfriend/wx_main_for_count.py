#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''
# from pymongo import MongoClient
import threading
from time import sleep

from selenium.webdriver.common.by import By

from common import Logger
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
        self.contents = []

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        sleep(5)
        el2 = self.wait_find_element(By.XPATH, "//*[@text='发现']")
        el2.click()
        el3 = self.wait_find_element(By.XPATH, "//*[@text='朋友圈']")
        el3.click()
        sleep(3)
        self.swipe_to_top()
        sleep(5)

    def crawl(self):
        self.enter()
        """
        爬取
        :return:
        """
        index_ = 0
        lastItem = None
        b_e_content = None
        isFirst = True
        while True:
            if wx_stop.stopFlag:
                break
            # 上滑
            if not isFirst:
                self.swipe_up_quick()
            isFirst = False
            top_element = self.wait_find_element(By.XPATH,
                                                 '//android.support.v7.widget.LinearLayoutCompat')
            if lastItem and top_element:
                self.scrollElement(lastItem, top_element)
            sleep(1)
            items = self.wait_find_elements(By.XPATH,
                                            '//android.widget.ListView/android.widget.RelativeLayout')
            if items:
                for index, item in enumerate(items):
                    accessibility_id = self.find_element_by_accessibility_id('头像', item)
                    if accessibility_id:
                        lastItem = accessibility_id
                    message_text_container = self.config.get_value("wx_content_ids",
                                                                   "message_text_container")
                    content_element = self.find_element_by_id(message_text_container, item)
                    if content_element:
                        content_element.click()
                        sleep(1)
                        b_e_content = self.getContentText()
                        if b_e_content:
                            Logger.println(f"【获取到全文内容={b_e_content}】")
                            self.go_back()
                    if b_e_content is None:
                        message_text = self.config.get_value("wx_content_ids",
                                                             "message_text")
                        b_e_content = self.getContentTextById(message_text, item)
                    if b_e_content is None:
                        Logger.println(f"【该条说说没有文本,忽略】")
                        continue
                    Logger.println(f"【{index}.获取到内容={b_e_content}】")
                    if b_e_content in self.contents:
                        Logger.println(f"【该条说说已经抓取过,忽略】")
                        continue
                    index_ = index_ + 1
                    Logger.println(f'=============这是第{index_}条朋友圈==============')
                    self.contents.append(b_e_content)

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
