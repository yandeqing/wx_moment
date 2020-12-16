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
        """
        爬取
        :return:
        """
        index = 0
        md5_contents = []
        contents = []
        last_base_md5 = None
        while True:
            if index > 0:
                # 上滑
                self.swipe_up()
                sleep(3)
            items = self.find_elements_by_id("com.tencent.mm:id/fn9")
            if items is None:
                continue
            for item in items:
                b_e_content = self.getContentTextById("com.tencent.mm:id/b_e", item)
                if b_e_content is None:
                    if index == 0:
                        index = +1
                    continue
                md5_ = self.MD5(b_e_content)
                if md5_ in md5_contents:
                    continue
                image0 = self.find_element_by_xpath(
                    "//*[@content-desc='图片']", item)
                if image0:
                    image0.click()
                    sleep(1)
                    start = 0
                    for index_img in range(9):
                        image_detail = self.find_element_by_id('com.tencent.mm:id/c9h')
                        if image_detail:
                            base64 = self.get_screenshot_as_base64(image_detail)
                            base_md5 = self.MD5(base64)
                            if last_base_md5 == base_md5:
                                end = FilePathUtil.get_time()
                                data = {
                                    'content_md5': md5_,
                                    'start': start,
                                    'end': end,
                                    'count': str(index_img)
                                }
                                contents.append(data)
                                self.driver.back()
                                break
                            if index_img == 0:
                                start = FilePathUtil.get_time()
                            # name = f"{i}_{base_md5}.png"
                            # if self.save_screenshot(image_detail, md5_, name):
                            try:
                                action1 = TouchAction(self.driver)
                                action1.long_press(el=image_detail, duration=500).perform()
                                sleep(0.5)
                                self.find_element_by_xpath(
                                    "//android.widget.TextView[contains(@text,'保存图片')]").click()
                            except:
                                continue
                                pass
                            time = FilePathUtil.get_time()
                            name = f'mmexport{time}.jpg'
                            Logger.println(f"【crawl({index}.{index_img}).已保存图片={name}】")
                            last_base_md5 = base_md5
                            if index_img == 8:
                                sleep(1)
                                end = FilePathUtil.get_time()
                                data = {
                                    'content_md5': md5_,
                                    'start': start,
                                    'end': end,
                                    'count': str(index_img + 1)
                                }
                                contents.append(data)
                                self.driver.back()
                                break
                            md5_contents.append(md5_)
                            sleep(1)
                            self.swipeLeft()
                date = time_util.now_to_date('%Y%m%d')
                full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "pic",
                                                     date + "wx_pic_moments.xls")
                excel_util.write_excel(filename=full_dir, worksheet_name=date, items=contents)
                index += 1
                if self.wx_content_md5 == md5_:
                    Logger.println(f"【crawl{index}已经抓取到上一次位置({md5_}).data={b_e_content}】")
                    self.config.set_value("wx_content", "md5_pic", md5_contents[0])
                    break


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