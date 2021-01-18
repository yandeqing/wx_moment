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
        self.wx_content_md5 = self.config.get_value("wx_content", "md5_pic")
        self.md5_contents = []
        self.today_md5_contents = []
        full_dir = FilePathUtil.get_lastmodify_file(
            FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
        array = excel_util.excel2array(full_dir)
        if array:
            for item in array:
                self.today_md5_contents.append(item['content_md5'])

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        by_id = self.wait_find_element(By.ID, 'com.tencent.mm:id/czl')
        el2 = by_id.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.RelativeLayout[3]')
        el2.click()
        el3 = self.wait_find_element(By.ID, 'com.tencent.mm:id/f43')
        el3.click()
        sleep(3)
        # el = self.driver.find_element_by_id('com.tencent.mm:id/bn')
        self.swipe_down(800)
        # sleep(3)

    def crawl(self):
        self.md5_contents = []
        self.enter()
        """
        爬取
        :return:
        """
        index = 0

        contents = []
        finished = False
        lastItem = None
        while True:
            if wx_stop.stopFlag:
                break
            # 上滑
            self.swipe_up_slow()
            top_element = self.find_element_by_id('com.tencent.mm:id/bp')
            if lastItem and top_element:
                self.scrollElement(lastItem, top_element)
            sleep(3)
            items = self.find_elements_by_id("com.tencent.mm:id/fn9")
            if items is None:
                continue
            if finished:
                break
            for item in items:
                accessibility_id = self.find_element_by_accessibility_id('头像', item)
                if accessibility_id:
                    lastItem = accessibility_id
                b_e_content = None
                last_pic_md5 = None
                last_md5_ = None
                advise = self.find_element_by_xpath(
                    "//android.widget.TextView[contains(@text,'广告')]", item)
                if advise:
                    Logger.println(f"【============检测到广告忽略进入下一条================】")
                    continue
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
                    Logger.println(f"【============该条说说没有文本,忽略===========】")
                    continue
                nickName = self.getNickName(item)
                phone = self.get_phone_from_txt(b_e_content)
                md5_ = self.MD5(b_e_content)
                if len(b_e_content) > 3 and b_e_content[-3:] == '...':
                    elment_datas = self.scan_all_text_elment(item)
                    LogUtil.info_jsonformat(elment_datas)
                contition = (last_md5_ in self.wx_content_md5) and (
                        md5_ in self.wx_content_md5) if last_md5_ else md5_ in self.wx_content_md5
                if contition:
                    Logger.println(f"【crawl{index}已经抓取到上一次位置md5_=({md5_},last_md5_={last_md5_}).data={b_e_content}】")
                    md5 = None
                    if len(self.md5_contents) > 1:
                        md5 = ','.join(self.md5_contents[0:2])
                    elif len(self.md5_contents) > 0:
                        md5 = self.md5_contents[0]
                    if md5:
                        self.config.set_value("wx_content", "md5_pic", md5)
                    finished = True
                    self.driver.back()
                    # 延迟一段时间
                    start_time = int(time())
                    sleeptime = int(WxConfig.get_addfriend_inte_seconds())
                    Logger.println(f"【main(暂时停止任务开启休闲模式).{sleeptime}秒后执行第={index}个任务】")
                    while True:
                        rdsleep = self.get_sleep(5, 6)
                        if rdsleep == 5:
                            self.scan_all_text_elment()
                        sleep(rdsleep)
                        if int(time()) - start_time > sleeptime:
                            break
                    self.crawl()
                    break
                if md5_ in self.today_md5_contents:
                    last_md5_ = md5_
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
                                    self.today_md5_contents.append(md5_)
                                    last_md5_ = md5_
                                sleep(1.5)
                                self.driver.back()
                                break
                            try:
                                action1 = TouchAction(self.driver)
                                action1.long_press(el=image_detail, duration=500).perform()
                                sleep(2)
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
                                    self.today_md5_contents.append(md5_)
                                    last_md5_ = md5_
                                sleep(1.5)
                                self.driver.back()
                                break
                            sleep(1.5)
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
                md5 = None
                if len(self.md5_contents) > 1:
                    md5 = ','.join(self.md5_contents[0:2])
                elif len(self.md5_contents) > 0:
                    md5 = self.md5_contents[0]
                if md5:
                    self.config.set_value("wx_content", "md5_pic", md5)

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
