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
        i = 0
        contents = []
        md5_contents = []
        while True:
            if wx_stop.stopFlag:
                break
            if i > 0:
                # 上滑
                self.swipe_up()
                sleep(3)
            items = self.find_elements_by_id("com.tencent.mm:id/fn9")
            if items is None:
                continue
            for item in items:
                b_e_content = self.getContentTextById("com.tencent.mm:id/b_e", item)
                if b_e_content is None:
                    continue
                nickName = self.getNickName(item)
                md5_ = self.MD5(b_e_content)
                phone = self.get_phone(b_e_content)
                data = {
                    'content_md5': md5_,
                    'nick_name': nickName,
                    'content': b_e_content,
                    'phone': phone,
                    'file_ids': '',
                }
                if md5_ in self.wx_content_md5:
                    Logger.println(f"【crawl{i}已经抓取到上一次位置({md5_}).data={data}】")
                    if len(md5_contents) > 1:
                        md5 = ','.join(md5_contents[0:2])
                    else:
                        md5 = md5_contents[0]
                    self.config.set_value("wx_content", "md5", md5)
                    break
                if md5_ in md5_contents:
                    continue
                else:
                    md5_contents.append(md5_)
                    Logger.println(f"【crawl({i}).data={data}】")
                    contents.append(data)
                    i = i + 1
                if i % 5 == 0:
                    date = time_util.now_to_date('%Y%m%d_%H')
                    full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text",
                                                         date + "wx_moments.xls")
                    excel_util.write_excel(filename=full_dir, worksheet_name=date, items=contents)
                    if len(md5_contents) > 1:
                        md5 = ','.join(md5_contents[0:2])
                    else:
                        md5 = md5_contents[0]
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
