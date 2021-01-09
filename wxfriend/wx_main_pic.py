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

from common import FilePathUtil, time_util, excel_util, Logger
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
        self.addfriend_inte_seconds = int(WxConfig.get_addfriend_inte_seconds())
        self.wx_content_md5 = self.config.get_value("wx_content", "md5_pic")

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        sleep(8)
        by_id = self.find_element_by_id('com.tencent.mm:id/czl')
        el2 = by_id.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.RelativeLayout[3]')
        el2.click()
        sleep(3)
        el3 = self.driver.find_element_by_id('com.tencent.mm:id/f43')
        el3.click()
        sleep(3)
        # el = self.driver.find_element_by_id('com.tencent.mm:id/bn')
        # self.double_click(el)
        # sleep(3)

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
            # timestr = time_util.now_to_date('%Y-%m-%d') + " 01:00:00"
            # des_timestamp = time_util.date_to_timestamp(timestr)
            # now_timestamp = time_util.now_to_timestamp()
            # if now_timestamp > des_timestamp:
            #     Logger.println(f"【到达休息时间点:{time_util.now_to_date()}】")
            #     break
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
                last_pic_md5 = None
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
                    if index == 0:
                        index = +1
                    Logger.println(f"【该条说说没有文本,忽略】")
                    continue
                nickName = self.getNickName(item)
                phone = self.get_phone_from_txt(b_e_content)
                md5_ = self.MD5(b_e_content)
                if md5_ in self.wx_content_md5:
                    Logger.println(f"【crawl{index}已经抓取到上一次位置({md5_}).data={b_e_content}】")
                    md5 = None
                    if len(md5_contents) > 1:
                        md5 = ','.join(md5_contents[0:2])
                    elif len(md5_contents) > 0:
                        md5 = md5_contents[0]
                    if md5:
                        self.config.set_value("wx_content", "md5_pic", md5)
                    finished = True
                    self.driver.back()
                    # 延迟一段时间
                    start_time = int(time())
                    sleeptime = self.addfriend_inte_seconds
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
                if md5_ in md5_contents:
                    continue
                wx_number = ""
                # phone = self.get_phone(b_e_content)
                # nick_name_element = self.getNickNameElement(item)
                # if nick_name_element:
                #     try:
                #         nick_name_element.click()
                #         sleep(1)
                #         by_xpath_nickname = self.find_element_by_xpath("//*[contains(@text,'昵称:')]")
                #         if by_xpath_nickname:
                #             nickName = by_xpath_nickname.get_attribute("text").replace('昵称:',
                #                                                                        '').strip()
                #         by_xpath = self.find_element_by_xpath("//*[contains(@text,'微信号:')]")
                #         if by_xpath:
                #             wx_number = by_xpath.get_attribute("text").replace('微信号:', '').strip()
                #             Logger.println(f"【微信号={wx_number}】")
                #             xpath = self.find_element_by_xpath("//*[contains(@text,'电话号码')]")
                #             if xpath:
                #                 phone_parent = xpath.parent
                #                 phone = self.getPhone(phone_parent)
                #                 Logger.println(f"【phone={phone}】")
                #                 sleep(1)
                #             self.driver.back()
                #     except  Exception  as e:
                #         Logger.println(f"【nick_name_element.click.e={e}】")
                #         pass
                image0 = self.find_element_by_xpath(
                    "//*[@content-desc='图片']", item)
                if image0:
                    Logger.println(
                        f"【crawl({index}).开始点击图片】")
                    image0.click()
                    sleep(1)
                    start = '0'
                    for index_img in range(9):
                        image_detail = self.find_element_by_id('com.tencent.mm:id/c9h')
                        if image_detail:
                            if index_img == 0:
                                start = FilePathUtil.get_time()
                            sleep(1)
                            text_content = self.scan_all_text_elment()
                            Logger.println(f"【crawl.{index} text_content ={text_content}】")
                            pic_md5 = self.MD5(text_content)
                            if last_pic_md5 == pic_md5:
                                Logger.println(f"【crawl({index}.{index_img}).前后图片一致退出】")
                                end = FilePathUtil.get_time()
                                data = {
                                    'content_md5': md5_,
                                    'nick_name': nickName,
                                    'wx_number': wx_number,
                                    'content': b_e_content,
                                    'phone': phone,
                                    'start': start,
                                    'end': end,
                                    'crawl_time': time_util.now_to_date(),
                                    'count': str(index_img)
                                }
                                if start != '0':
                                    contents.append(data)
                                self.driver.back()
                                break
                            # name = f"{i}_{base_md5}.png"
                            # if self.save_screenshot(image_detail, md5_, name):
                            try:
                                action1 = TouchAction(self.driver)
                                action1.long_press(el=image_detail, duration=500).perform()
                                sleep(1.5)
                                saveBtn = self.find_element_by_xpath("//*[contains(@text,'保存图片')]")
                                if saveBtn:
                                    saveBtn.click()
                                else:
                                    Logger.dingdingException(f"找不到保存按钮,保存图片失败")
                            except Exception as e:
                                Logger.println(f'TouchAction Exception{e}')
                                Logger.dingdingException(f"保存图片失败{e}")
                                self.driver.back()
                                continue
                                pass
                            Logger.println(
                                f"【crawl({index}.{index_img}).已保存图片=mmexport{FilePathUtil.get_time()}.jpg】")
                            last_pic_md5 = pic_md5
                            # is_oppo = self.desired_caps['deviceName'] == '5e8caad5'
                            if index_img == 8:
                                # if index_img == 8 or is_oppo:
                                sleep(1)
                                end = FilePathUtil.get_time()
                                data = {
                                    'content_md5': md5_,
                                    'nick_name': nickName,
                                    'wx_number': wx_number,
                                    'content': b_e_content,
                                    'phone': phone,
                                    'start': start,
                                    'end': end,
                                    'crawl_time': time_util.now_to_date(),
                                    'count': str(index_img + 1)
                                }
                                if start != '0':
                                    contents.append(data)
                                self.driver.back()
                                break
                            sleep(1)
                            self.swipeLeft()
                    md5_contents.append(md5_)
                if len(contents) > 0:
                    value = self.config.get_value("wx_content", "select")
                    if value == 'True':
                        Logger.println(f"开始上传第{index}条数据")
                        res = WxUploader.uploadItems(contents)
                        # 有房源刷新的列表
                        if '20003' == res:
                            contents[0]['content']=''
                            date = time_util.now_to_date('%Y%m%d')
                            full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text",
                                                                 date + "wx_pic_update_moments.xls")
                            excel_util.write_excel_append(filename=full_dir, worksheet_name=date,
                                                          items=contents)
                            contents.clear()
                    # 新房源列表
                    if len(contents) > 0:
                        contents[0]['content'] = ''
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
                if len(md5_contents) > 1:
                    md5 = ','.join(md5_contents[0:2])
                elif len(md5_contents) > 0:
                    md5 = md5_contents[0]
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


if __name__ == '__main__':
    moments = Moments()
    moments.main()
