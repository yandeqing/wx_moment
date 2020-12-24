#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''
# from pymongo import MongoClient
import threading
from time import sleep

from appium.webdriver.common.touch_action import TouchAction

from common import FilePathUtil, time_util, excel_util, Logger
from config.AppConfig import MonitorConfig
from wxfriend import wx_stop, WxUploader
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.config = MonitorConfig()
        self.wx_content_md5 = self.config.get_value("wx_content", "md5_pic")

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        sleep(5)
        by_id = self.find_element_by_id('com.tencent.mm:id/czl')
        el2 = by_id.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.RelativeLayout[3]')

        el2.click()
        sleep(3)
        el3 = self.driver.find_element_by_id('com.tencent.mm:id/f43')
        el3.click()

    def crawl(self):
        self.enter()
        """
        爬取
        :return:
        """
        index = 0
        md5_contents = []
        contents = []
        finished = False
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
                self.scan_all_text_elment(item)
                b_e_content = None
                content_element = self.find_element_by_id("com.tencent.mm:id/b_m", item)
                if content_element:
                    content_element.click()
                    sleep(2)
                    b_e_content = self.getContentTextById('com.tencent.mm:id/fpu')
                    if b_e_content:
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
                if md5_ in self.wx_content_md5:
                    Logger.println(f"【crawl{index}已经抓取到上一次位置({md5_}).data={b_e_content}】")
                    finished = True
                    break
                if md5_ in md5_contents:
                    continue
                wx_number = ""
                phone = self.get_phone_from_txt(b_e_content)
                nick_name_element = self.getNickNameElement(item)
                if nick_name_element:
                    try:
                        nick_name_element.click()
                        sleep(1)
                        by_xpath_nickname = self.find_element_by_xpath("//*[contains(@text,'昵称:')]")
                        if by_xpath_nickname:
                            nickName = by_xpath_nickname.get_attribute("text").replace('昵称:',
                                                                                       '').strip()
                        by_xpath = self.find_element_by_xpath("//*[contains(@text,'微信号:')]")
                        if by_xpath:
                            wx_number = by_xpath.get_attribute("text").replace('微信号:', '').strip()
                            Logger.println(f"【微信号={wx_number}】")
                            xpath = self.find_element_by_xpath("//*[contains(@text,'电话号码')]")
                            if xpath:
                                phone_parent = xpath.parent
                                phone = self.getPhone(phone_parent)
                                Logger.println(f"【phone={phone}】")
                                sleep(1)
                        self.driver.back()
                    except  Exception  as e:
                        Logger.println(f"【nick_name_element.click.e={e}】")
                        pass
                contents.append({
                    'content_md5': md5_,
                    'nick_name': nickName,
                    'wx_number': wx_number,
                    'phone': phone
                })
                md5_contents.append(md5_)
                date = time_util.now_to_date('%Y%m%d')
                full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text",
                                                     date + "wx_user_moments.xls")
                excel_util.write_excel_append(filename=full_dir, worksheet_name=date,
                                              items=contents)
                WxUploader.putItems(contents)
                contents.clear()
                index += 1

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
