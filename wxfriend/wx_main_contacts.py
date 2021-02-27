#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''
# from pymongo import MongoClient
import threading
from time import sleep

from common import FilePathUtil, time_util, excel_util, Logger
from wxfriend import wx_stop
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        sleep(self.WAIT_TIMEOUT)
        by_id = self.find_element_by_id('com.tencent.mm:id/czl')
        el2 = by_id.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.RelativeLayout[2]')

        el2.click()
        sleep(3)

    def crawl(self):
        self.enter()
        """
        爬取
        :return:
        """
        index = 0
        nickNames = []
        contents = []
        finished = False
        while True:
            if wx_stop.stopFlag:
                break
            if index > 0:
                # 上滑
                self.swipe_up()
                sleep(0.5)
            items = self.find_elements_by_id("com.tencent.mm:id/b36")
            if items is None:
                continue
            if finished:
                break
            for item in items:
                nickName = self.getContentTextById('com.tencent.mm:id/dy5', item)
                if nickName:
                    Logger.println(f"【获取到联系人={nickName}】")
                else:
                    continue
                if nickName in nickNames:
                    Logger.println(f"【已经抓取跳过联系人{nickName}】")
                    continue
                nickNames.append(nickName)
                phone = self.get_phone_from_txt(nickName)
                wx_number = ""
                try:
                    item.click()
                    sleep(0.5)
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
                            sleep(0.5)
                    self.driver.back()
                except  Exception  as e:
                    Logger.println(f"【nick_name_element.click.e={e}】")
                    pass
                contents.append({
                    'nick_name': nickName,
                    'wx_number': wx_number,
                    'phone': phone
                })
                date = time_util.now_to_date('%Y%m%d')
                full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text",
                                                     date + "wx_contacts_moments.xls")
                excel_util.write_excel(filename=full_dir, worksheet_name=date,
                                              items=contents)
                index += 1
            last_flag = self.getContentTextById("com.tencent.mm:id/azb")
            if last_flag:
                date = time_util.now_to_date('%Y%m%d')
                full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text",
                                                     date + "wx_contacts_moments.xls")
                FilePathUtil.startfile(full_dir)
                break

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
