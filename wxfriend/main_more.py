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
        sleep(5)
        by_id = self.driver.find_element_by_id('com.tencent.mm:id/czl')
        el2 = by_id.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.RelativeLayout[3]')
        el2.click()
        sleep(3)
        el3 = self.driver.find_element_by_id('com.tencent.mm:id/f43')
        el3.click()

    def crawl(self):
        """
        爬取
        :return:
        """
        self.driver.swipe(300, 400, 300, 300, 1000)
        i = 0
        contents = []
        md5_contents = []
        while True:
            if i > 0:
                # 上滑
                self.swipe_up()
                sleep(3)
            items = self.find_elements_by_id("com.tencent.mm:id/fn9")
            if items is None:
                continue
            for item in items:
                sleep(3)
                content_element = self.find_element_by_id("com.tencent.mm:id/b_m", item)
                if content_element:
                    content_element.click()
                else:
                    if i == 0:
                        self.swipe_up()
                    continue
                sleep(1)
                b_e_content = self.getContentTextById('com.tencent.mm:id/fpu', item)
                if b_e_content is None:
                    continue
                nickName = self.getNickName(item)
                md5_ = self.MD5(b_e_content)
                phone = self.get_phone(b_e_content)
                data = {
                    'content_md5': md5_,
                    'nickName': nickName,
                    'content': b_e_content,
                    'phone': phone
                }
                print(f"【crawl({i}).data={data}】")
                if self.wx_content_md5 == md5_:
                    print(f"【crawl{i}已经抓取到上一次位置({md5_}).data={data}】")
                    self.config.set_value("wx_content", "md5_more", md5_contents[0])
                    break
                if md5_ in md5_contents:
                    continue
                else:
                    i = i + 1
                    md5_contents.append(md5_)
                    contents.append(data)
                if i % 5 == 0:
                    date = time_util.now_to_date('%Y%m%d_%H')
                    full_dir = FilePathUtil.get_full_dir("wxfriend", "excel",
                                                         date + "more_wx_moments.xls")
                    excel_util.write_excel(filename=full_dir, worksheet_name=date, items=contents)

    def main(self):
        """
        入口
        :return:
        """
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()


if __name__ == '__main__':
    moments = Moments()
    moments.main()
