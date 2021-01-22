#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/3 10:25
'''
# from pymongo import MongoClient
import threading
from time import sleep, time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from common import time_util, time_util, excel_util, Logger, FilePathUtil
from common.LogUtil import LogUtil
from config.AppConfig import MonitorConfig
from wxfriend import wx_stop, WxUploader, WxConfig
from wxfriend.wx_swipe_base import MomentsBase


class Moments(MomentsBase):
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        super().__init__()
        self.config = MonitorConfig()
        self.md5_contents = []
        full_dir = FilePathUtil.get_lastmodify_file(
            FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
        array = excel_util.excel2array(full_dir)
        if array:
            for item in array:
                self.md5_contents.append(item['content_md5'])

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
        sleep(3)
        # sleep(3)

    def crawl(self):
        self.enter()
        """
        爬取
        :return:
        """
        index = 0
        isFirst=True
        contents = []
        finished = False
        lastItem = None
        while True:
            if wx_stop.stopFlag:
                break
                # 上滑
            if not isFirst:
                self.swipe_up_slow()
            isFirst = False
            top_element = self.wait_find_element(By.XPATH,
                                                 '//android.support.v7.widget.LinearLayoutCompat')
            if lastItem and top_element:
                self.scrollElement(lastItem, top_element)
            sleep(3)
            items = self.wait_find_elements(By.XPATH,
                                            '//android.widget.ListView/android.widget.RelativeLayout')
            if items is None:
                continue
            if finished:
                break
            for item in items:
                accessibility_id = self.find_element_by_accessibility_id('头像', item)
                if accessibility_id:
                    lastItem = accessibility_id
                b_e_content = None
                last_b_e_content = ""
                last_pic_md5 = None
                advise = self.find_element_by_xpath(
                    "//android.widget.TextView[contains(@text,'广告')]", item)
                if advise:
                    Logger.println(f"【============检测到广告忽略进入下一条================】")
                    continue
                message_text_container = self.config.get_value("wx_content_ids",
                                                               "message_text_container")
                content_element = self.find_element_by_id(message_text_container, item)
                if content_element:
                    content_element.click()
                    sleep(2)
                    b_e_content = self.getContentTextById('com.tencent.mm:id/fpu')
                    if b_e_content:
                        Logger.println(f"【获取到全文内容={b_e_content}】")
                        self.driver.back()
                if b_e_content is None:
                    message_text = self.config.get_value("wx_content_ids",
                                                         "message_text")
                    b_e_content = self.getContentTextById(message_text, item)
                if b_e_content is None:
                    Logger.println(f"【============该条说说没有文本,忽略===========】")
                    continue
                nickName = self.getNickName(item)
                phone = self.get_phone_from_txt(b_e_content)
                md5_ = self.MD5(b_e_content)
                if len(b_e_content) > 3 and b_e_content[-3:] == '...':
                    elment_datas = self.scan_all_text_elment(item)
                    LogUtil.info_jsonformat(elment_datas)
                if md5_ in self.md5_contents:
                    Logger.println(f"【============该条说说已经抓取过,忽略===========】")
                    continue
                image0 = self.find_element_by_xpath(
                    "//*[@content-desc='图片']", item)
                if image0:
                    Logger.println(
                        f"【crawl({index}).开始点击图片】")
                    image0.click()
                    sleep(1)
                    start = '0'
                    end = '0'
                    for index_img in range(9):
                        image_detail = self.find_element_by_id('com.tencent.mm:id/c9h')
                        if image_detail:
                            text_content = ""
                            text_contents = self.scan_all_text_elment()
                            for item in text_contents:
                                text_content += item['text']
                            Logger.println(f"【crawl.{index} text_content ={text_content}】")
                            pic_md5 = self.MD5(text_content)
                            if last_pic_md5 == pic_md5:
                                Logger.println(f"【crawl({index}.{index_img}).前后图片一致退出】")
                                if not end:
                                    sleep(2)
                                    end = time_util.get_time()
                                data = {
                                    'content_md5': md5_,
                                    'nick_name': nickName,
                                    'wx_number': "",
                                    'content': b_e_content,
                                    'phone': phone,
                                    'start': start,
                                    'end': end,
                                    'crawl_time': time_util.now_to_date(),
                                    'count': str(index_img)
                                }
                                if start != '0':
                                    contents.append(data)
                                    self.md5_contents.append(md5_)
                                    last_b_e_content = b_e_content
                                sleep(1.5)
                                self.driver.back()
                                break
                            try:
                                action1 = TouchAction(self.driver)
                                action1.long_press(el=image_detail, duration=500).perform()
                                saveBtn = self.wait_find_element(By.XPATH,
                                                                 "//*[contains(@text,'保存图片')]")
                                if saveBtn:
                                    saveBtn.click()
                                    element = self.wait_find_element(By.XPATH,
                                                                     "//*[contains(@text,'图片已保存')]")
                                    attribute = element.get_attribute('text')
                                    Logger.println(f"【crawl.{index} text_content ={attribute}】")
                                    if index_img == 0:
                                        if attribute:
                                            start = get_time_from_text(attribute)
                                    end = get_time_from_text(attribute)
                                else:
                                    Logger.dingdingException(f"找不到保存按钮,保存图片失败")
                            except Exception as e:
                                Logger.println(f'TouchAction Exception{e}')
                                Logger.dingdingException(f"保存图片失败{e}")
                                self.driver.back()
                                continue
                                pass
                            last_pic_md5 = pic_md5
                            if index_img == 8:
                                if not end:
                                    sleep(2)
                                    end = time_util.get_time()
                                data = {
                                    'content_md5': md5_,
                                    'nick_name': nickName,
                                    'wx_number': "",
                                    'content': b_e_content,
                                    'phone': phone,
                                    'start': start,
                                    'end': end,
                                    'crawl_time': time_util.now_to_date(),
                                    'count': str(index_img + 1)
                                }
                                if start != '0':
                                    Logger.println(
                                        f"【crawl({index}.{index_img}).已保存图片=mmexport{end}.jpg】")
                                    contents.append(data)
                                    self.md5_contents.append(md5_)
                                    last_b_e_content = b_e_content
                                sleep(1)
                                self.driver.back()
                                break
                            self.swipeLeft()
                else:
                    # 纯文本
                    data = {
                        'content_md5': md5_,
                        'nick_name': nickName,
                        'wx_number': "",
                        'content': b_e_content,
                        'phone': phone,
                        'start': "0",
                        'end': "0",
                        'crawl_time': time_util.now_to_date(),
                        'count': "0"
                    }
                    contents.append(data)
                if len(contents) > 0:
                    value = self.config.get_value("wx_content", "select")
                    if value == 'True':
                        Logger.println(f"开始上传第{index}条数据")
                        res = WxUploader.uploadItems(contents)
                        # 有房源刷新的列表
                        if '20003' == res:
                            contents[0]['content'] = ""
                            date = time_util.now_to_date('%Y%m%d')
                            full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text",
                                                                 date + "wx_pic_update_moments.xls")
                            excel_util.write_excel_append(filename=full_dir, worksheet_name=date,
                                                          items=contents)
                            contents.clear()
                    # 新房源列表
                    if len(contents) > 0:
                        contents[0]['content'] = ""
                        date = time_util.now_to_date('%Y%m%d')
                        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "pic",
                                                             date + "wx_pic_moments.xls")
                        excel_util.write_excel_append(filename=full_dir, worksheet_name=date,
                                                      items=contents)
                        contents.clear()
                        index += 1
                else:
                    Logger.println(f"【没有数据不处理】")

    def main(self):
        """
        入口
        :return:
        """
        # 爬取
        date = time_util.now_to_date('%Y-%m-%d')
        Logger.println(f"【============开始抓取{date}遗漏数据================】")
        self.crawl()

    def main_backgroud(self):
        thread = threading.Thread(target=self.main)
        thread.start()


def get_time_from_text(text: str):
    if text:
        splits = text.split("/")
        name = splits[-1]
        if name:
            name_prefix = name.split(".")
            prefix_ = name_prefix[0]
            if prefix_:
                replace = prefix_.replace("mmexport", '')
                return replace
    return None


if __name__ == '__main__':
    moments = Moments()
    moments.main()
    # get_time_from_text('图片已保存至/storage/emulated/0/Pictures/WeiXin/mmexport1610952572472.jpg 文件夹')
