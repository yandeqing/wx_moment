#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''

# from pymongo import MongoClient
import threading
from time import sleep

from PyQt5.QtCore import QBasicTimer, QTimer

from common import excel_util, FilePathUtil, Logger
from config.AppConfig import MonitorConfig
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.config = MonitorConfig()
        self.last_record_phone = self.config.get_value("wx_content", "last_phone")

    def add(self, phone):
        sleep(get_sleep(6, 8))
        # 输入电话号码
        try:
            self.find_element_by_id('com.tencent.mm:id/bhn').send_keys(phone)
        except:
            pass
        sleep(get_sleep(5, 8))
        try:
            self.find_element_by_id('com.tencent.mm:id/f8g').click()
            sleep(get_sleep(4, 6))
        except:
            pass

        try:
            xpath = self.find_element_by_xpath(
                "//android.widget.TextView[contains(@text,'用户不存在')]")
            if xpath:
                Logger.println(f"【main(用户不存在={phone}】")
                self.find_element_by_xpath(
                    "//android.widget.Button[contains(@text,'确定')]").click()
                self.config.set_value("wx_content", "last_phone", phone)
                sleep(get_sleep(1, 2))
                return False
            xpath = self.find_element_by_xpath(
                "//android.widget.TextView[contains(@text,'被搜账号状态异常')]")
            if xpath:
                Logger.println(f"【main(被搜账号异常无法显示={phone}】")
                self.find_element_by_xpath(
                    "//android.widget.Button[contains(@text,'确定')]").click()
                self.config.set_value("wx_content", "last_phone", phone)
                sleep(get_sleep(1, 2))
                return False
            else:
                xpath = self.find_element_by_xpath(
                    "//android.widget.TextView[contains(@text,'操作过于频繁，请稍后再试')]")
                if xpath:
                    Logger.println(f"【main(操作过于频繁,请稍后再试={phone}】")
                    self.find_element_by_xpath(
                        "//android.widget.Button[contains(@text,'确定')]").click()
                    return True
        except Exception as e:
            Logger.println(f"【add().e={e}】")
            pass
        # 点击设置标签备注
        # self.find_element_by_id('com.tencent.mm:id/f43').click()
        try:
            self.find_element_by_xpath(
                "//android.widget.TextView[contains(@text,'设置备注和标签')]").click()
        except:
            try:
                self.find_element_by_xpath(
                    "//android.widget.TextView[contains(@text,'标签')]").click()
            except:
                pass
            pass
        sleep(get_sleep(2, 3))
        try:
            self.find_element_by_id('com.tencent.mm:id/b0a').send_keys(phone)
            sleep(get_sleep(1, 2))
            # 点击保存
            by_xpath = self.find_element_by_xpath("//*[contains(@text,'保存')]")
            if by_xpath:
                by_xpath.click()
                Logger.println(f"【add().phone={phone}】")
                self.config.set_value("wx_content", "last_phone", phone)
            else:
                self.find_element_by_xpath("//*[contains(@text,'完成')]").click()
                self.config.set_value("wx_content", "last_phone", phone)
        except Exception as e:
            Logger.println(f"【add().e={e}】")
            sleep(get_sleep(1, 2))
            self.driver.back()
            sleep(get_sleep(1, 2))
        sleep(get_sleep(1, 2))
        self.driver.back()
        # 点击添加好友
        # .find_element_by_xpath('
        # self.driver.find_element_by_xpath(
        #     "//android.widget.TextView[contains(@text,'添加到通讯录')]").click()
        # sleep(3)
        # send_btn = self.driver.find_element_by_xpath(
        #     "//android.widget.Button[contains(@text,'发送')]")
        # if send_btn:
        #     send_btn.click()
        # self.driver.back()

    def main(self):
        sleep(get_sleep(6, 10))
        # 点击搜索按钮
        self.find_element_by_id('com.tencent.mm:id/f8y').click()
        sleep(get_sleep(3, 5))
        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "手机号列表.xls")
        array = excel_util.excel2array(full_dir, "手机号列表")
        # array = [{'手机': '17602876095'}]
        # array = [{'手机': '13301616272'}, {'手机': '15821902923'}]
        start_index =-1
        count = 0
        for index, item in enumerate(array):
            phone = str(int(item['手机']))
            if self.last_record_phone == phone:
                Logger.println(f"【main({index}).上次添加的手机={phone}】")
                start_index = index
            if index > start_index:
                Logger.println(f"【main({index}).开始添加手机={phone}】")
                Logger.println(f"【main开始执行第{count}个任务】")
                if count > 44:
                    sleeptime = get_sleep(3600, 4800)
                    Logger.println(f"【main(暂时停止任务).{sleeptime}秒后执行第={count}个任务】")
                    sleep(sleeptime)
                if self.add(phone):
                    break
                count += 1
                Logger.println(f"【main(花费时间).total_count={total_count}s】")
        # self.add('13120749104')

    def main_backgroud(self):
        thread = threading.Thread(target=self.main)
        thread.start()


total_count = 0


def get_sleep(start: int = 1, end: int = 9):
    global total_count
    import random
    randint = random.randint(start, end)
    total_count += randint
    return randint


if __name__ == '__main__':
    moments = Moments()
    moments.main_backgroud()
