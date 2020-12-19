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
        index = 0
        contents = []
        finished=False
        md5_contents = []
        while True:
            if wx_stop.stopFlag:
                break
            if index > 0:
                # 上滑
                self.swipe_up()
                sleep(3)
            items = self.find_elements_by_id("com.tencent.mm:id/fn9")
            if items is None:
                continue
            if finished:
                break
            for item in items:
                b_e_content = None
                content_element = self.find_element_by_id("com.tencent.mm:id/b_m", item)
                if content_element:
                    content_element.click()
                    sleep(2)
                    b_e_content = self.getContentTextById('com.tencent.mm:id/fpu')
                    if  b_e_content:
                        Logger.println(f"【获取到全文内容={b_e_content}】")
                        self.driver.back()
                if b_e_content is None:
                    b_e_content = self.getContentTextById("com.tencent.mm:id/b_e", item)
                if b_e_content is None:
                    if index == 0:
                        index = +1
                    Logger.println(f"【该条说说没有文本,忽略】")
                    continue
                nickName = self.getNickName(item)
                md5_ = self.MD5(b_e_content)
                phone = self.get_phone_from_txt(b_e_content)
                data = {
                    'content_md5': md5_,
                    'nick_name': nickName,
                    'content': b_e_content,
                    'phone': phone,
                    'file_ids': '',
                }
                if md5_ in self.wx_content_md5:
                    Logger.println(f"【crawl{index}已经抓取到上一次位置({md5_}).data={data}】")
                    md5 = None
                    if len(md5_contents) > 1:
                        md5 = ','.join(md5_contents[0:2])
                    elif len(md5_contents) > 0:
                        md5 = md5_contents[0]
                    if md5:
                        self.config.set_value("wx_content", "md5", md5)
                    finished=True
                    break
                if md5_ in md5_contents:
                    continue
                else:
                    md5_contents.append(md5_)
                    Logger.println(f"【crawl({index}).data={data}】")
                    contents.append(data)
                    index = index + 1
                if index % 5 == 0:
                    date = time_util.now_to_date('%Y%m%d_%H')
                    full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text",
                                                         date + "wx_moments.xls")
                    excel_util.write_excel(filename=full_dir, worksheet_name=date, items=contents)
                    md5 = None
                    if len(md5_contents) > 1:
                        md5 = ','.join(md5_contents[0:2])
                    elif len(md5_contents) > 0:
                        md5 = md5_contents[0]
                    if md5:
                        self.config.set_value("wx_content", "md5", md5)

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
