#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''

# from pymongo import MongoClient
import threading
from time import sleep, time

from PyQt5.QtCore import QBasicTimer, QTimer

from common import excel_util, FilePathUtil, Logger
from config.AppConfig import MonitorConfig
from wxfriend import WxConfig, wx_stop
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.max_count = int(WxConfig.get_add_friend_max_count())
        self.addfriend_inte_seconds = int(WxConfig.get_addfriend_inte_seconds())
        self.config = MonitorConfig()
        self.last_record_phone = self.config.get_value("wx_content", "add_friend_last_phone")

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
                self.config.set_value("wx_content", "add_friend_last_phone", phone)
                sleep(get_sleep(1, 2))
                return False
            xpath = self.find_element_by_xpath(
                "//android.widget.TextView[contains(@text,'被搜账号状态异常')]")
            if xpath:
                Logger.println(f"【main(被搜账号异常无法显示={phone}】")
                self.find_element_by_xpath(
                    "//android.widget.Button[contains(@text,'确定')]").click()
                self.config.set_value("wx_content", "add_friend_last_phone", phone)
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
        # 点击添加好友
        try:
            addbtn = self.find_element_by_xpath(
                "//android.widget.TextView[contains(@text,'添加到通讯录')]")
            if addbtn:
                addbtn.click()
                sleep(get_sleep(5, 6))
                send_btn = self.find_element_by_xpath(
                    "//android.widget.Button[contains(@text,'发送')]")
                if send_btn:
                    send_btn.click()
                    self.config.set_value("wx_content", "add_friend_last_phone", phone)
                    sleep(get_sleep(1, 2))
                    send_btn = self.find_element_by_xpath(
                        "//android.widget.Button[contains(@text,'发送')]")
                    if send_btn:
                        self.driver.back()
                        sleep(get_sleep(1, 2))
                    self.driver.back()
                else:
                    Logger.println(f"【main(号码已添加无需添加={phone}】")
                    self.driver.back()
            else:
                Logger.println(f"【main(号码已添加无需添加={phone}】")
                self.driver.back()
        except Exception as e:
            Logger.println(f"【add().e={e}】")
            pass

    def main(self):
        sleep(get_sleep(6, 10))
        # 点击搜索按钮
        self.find_element_by_id('com.tencent.mm:id/f8y').click()
        sleep(get_sleep(3, 5))
        # full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "手机号列表.xls")
        full_dir = WxConfig.getPhoneExcel()
        if not full_dir:
            Logger.println(f"【main(请先配置手机号列表文件】")
            return
        array = excel_util.excel2array(full_dir, "手机号列表")
        length = len(array)
        if not array:
            Logger.println(f"【main(请先配置手机号列表文件的sheet_name为手机号列表】")
            return
        # array = [{'手机': '18612205027'}]
        # array = [{'手机': '18612205027'}, {'手机': '15821902923'}]
        start_index = 0
        for index, element in enumerate(array):
            if str(int(element["手机"])) == self.last_record_phone:
                start_index = index
                Logger.println(f"【main找到上次添加的手机位置={start_index + 1}={self.last_record_phone}】")
                break
        count = 0
        if start_index + 1 > length:
            Logger.println(f"【已经是最后一条了】")
            return
        for index, item in enumerate(array[start_index + 1:length]):
            if wx_stop.stopFlag:
                break
            phone = str(int(item['手机']))
            Logger.println(f"【main({index}).开始添加手机={phone}】")
            Logger.println(f"【main开始执行第{count}个任务】")
            if self.max_count > 1 and count > 1 and (count % self.max_count) == 0:
                start_time = int(time())
                sleeptime = self.addfriend_inte_seconds
                Logger.println(f"【main(暂时停止任务开启休闲模式).{sleeptime}秒后执行第={count}个任务】")
                while True:
                    rdsleep = get_sleep(5, 9)
                    by_id = self.find_element_by_id('com.tencent.mm:id/bhn')
                    if rdsleep == 5:
                        if by_id:
                            by_id.send_keys(f'已经休眠{int(time()) - start_time}s')
                    else:
                        if by_id:
                            by_id.send_keys('')
                    sleep(rdsleep)
                    if int(time()) - start_time > sleeptime:
                        break
                Logger.println(f"【main(退出休闲模式)继续执行第={count}个任务】")
            if wx_stop.stopFlag:
                break
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
    moments.main()
