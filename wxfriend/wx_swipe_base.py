#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/7 12:07
'''
import hashlib
import os
import re
from time import sleep

from appium.webdriver import WebElement
from appium.webdriver.common import mobileby
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from appium import webdriver

from selenium.webdriver.support import expected_conditions as EC

from common import FilePathUtil, Logger, time_util
from wxfriend import WxConfig
from wxfriend.WxConfig import TIMEOUT


class MomentsBase():

    def stop(self):
        try:
            self.driver.close()
        except:
            pass

    def get_sleep(self, start: int = 1, end: int = 9):
        import random
        randint = random.randint(start, end)
        self.total_count += randint
        return randint

    def __init__(self):
        self.total_count = 0
        self.desired_caps = WxConfig.getAppiumConfig()
        self.driver = webdriver.Remote(WxConfig.getServerUrl(), self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.screen_size = [x, y]
        self.by = mobileby.MobileBy()
        pass

    def getNickName(self, driver=None):
        driver = driver or self.driver
        try:
            nickname = driver.find_element_by_id(
                'com.tencent.mm:id/e3x').get_attribute("text")
            Logger.println(f"【getNickName().nickname={nickname}】")
            return nickname
        except:
            pass

    def getPhone(self, driver=None):
        driver = driver or self.driver
        try:
            xpath = driver.find_element_by_id('com.tencent.mm:id/ec9')
            if xpath:
                phone = xpath.find_element_by_xpath(
                    '//android.widget.TextView').get_attribute("text")
                return phone
        except  Exception  as e:
            Logger.println(f"【getPhone().e={e}】")
            pass

    def getNickNameElement(self, driver=None):
        driver = driver or self.driver
        try:
            nickname_element = driver.find_element_by_id(
                'com.tencent.mm:id/e3x')
            return nickname_element
        except:
            return None
            pass

    def double_click(self, element, driver=None):
        driver = driver or self.driver
        # action = TouchAction(driver)
        # action.tap(element).release().tap(element).release().perform()
        Logger.println(f'double click element({element})')

    def long_press(self, element, driver=None):
        driver = driver or self.driver
        action1 = TouchAction(driver)
        action1.long_press(el=element, duration=500).perform()
        Logger.println(f'long_press element({element})')

    def get_phone_from_txt(self, text):
        phone_reg = re.compile('[0-9]{11}', re.MULTILINE)
        search = phone_reg.search(text)
        if search and search.group:
            return search.group(0).strip()
        else:
            return ''

    def wait_find_element(self, by_type: str, value: str, driver: WebDriver = None):
        """
        获取单个元素, 显式等待
        :param driver: 驱动对象
        :param by_type: 查找元素的操作
        :param value: 查找元素的方法
        :return:
        """
        driver = driver or self.driver
        if not driver:
            return driver
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(locator=(by_type, value)))
        return driver.find_element(by_type, value)

    def wait_find_elements(self, by_type: str, value: str, driver: WebDriver = None):
        """
        获取多个元素, 显式等待
        :param driver:
        :param by_type:
        :param value:
        :return:
        """
        driver = driver or self.driver
        if not driver:
            return driver
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(locator=(by_type, value)))
            return driver.find_elements(by_type, value)
        except:
            return None

    def swipe_up(self, _time: int = 1000):
        """
        向上滑动
        :param driver:
        :param _time:
        :return:
        """
        try:
            size = self.screen_size
            x1 = int(size[0] * 0.5)  # 起始x坐标
            y1 = int(size[1] * 0.75)  # 起始y坐标
            y2 = int(size[1] * 0.25)  # 终点y坐标
            self.driver.swipe(x1, y1, x1, y2, _time)
            return True
        except:
            return False

    def swipe_up_slow(self):
        """
        向上滑动
        :param driver:
        :param _time:
        :return:
        """
        try:
            size = self.screen_size
            x1 = int(size[0] * 0.5)  # 起始x坐标
            y1 = int(size[1] * 0.75)  # 起始y坐标
            y2 = int(size[1] * 0.45)  # 终点y坐标
            self.driver.swipe(x1, y1, x1, y2, 2000)
            return True
        except:
            return False

    def swipe_to_top(self):
        while True:
            source = self.driver.page_source
            """
            向上滑动
            :param driver:
            :param _time:
            :return:
            """
            size = self.screen_size
            x1 = int(size[0] * 0.5)  # 起始x坐标
            y1 = int(size[1] * 0.75)  # 起始y坐标
            y2 = int(size[1] * 0.5)  # 终点y坐标
            self.driver.swipe(x1, y2, x1, y1, 1000)
            sleep(2)
            current_source = self.driver.page_source
            if source == current_source:
                Logger.println(f"【swipe_to_top().已经滑动到顶部了】")
                break

    def swipe_down(self, _time: int = 1000):
        """
        向下滑动
        :param driver:
        :param _time:
        :return:
        """
        try:
            size = self.screen_size
            x1 = int(size[0] * 0.5)  # 起始x坐标
            y1 = int(size[1] * 0.9)  # 起始y坐标
            y2 = int(size[1] * 0.5)  # 终点y坐标
            self.driver.swipe(x1, y2, x1, y1, _time)
            return True
        except:
            return False

    def swipeRight(self):
        size = self.screen_size
        x = size[0]
        # 获取屏幕宽
        y = size[1]
        # 向右滑动，显示推荐tab 内容，第五个参数，时间设置大一点，否则容易看不到滑动效果
        self.driver.swipe(1 / 7 * x, 1 / 2 * y, 5 / 7 * x, 1 / 2 * y, 500)
        sleep(1)

    def swipeLeft(self):
        size = self.screen_size
        x = size[0]
        # 获取屏幕宽
        y = size[1]
        # 滑屏，大概从屏幕右边2分之一高度，往左侧滑动,滑动后显示的是 热点tab
        self.driver.swipe(6 / 7 * x, 1 / 2 * y, 1 / 7 * x, 1 / 2 * y, 500)

    def scrollElement(self, origin_el: WebElement, destination_el: WebElement):
        try:
            size = self.screen_size
            x1 = int(size[0] * 0.5)  # 起始x坐标
            location_start = origin_el.location
            location_end = destination_el.size
            Logger.println(f"【scrollElement().location_start={location_start}】")
            Logger.println(f"【scrollElement().location_start,={location_end}】")
            y_ = location_start['y']
            height_ = location_end['height'] + 20
            if y_ > height_:
                self.driver.flick(x1, y_, x1, height_)
        except Exception as e:
            Logger.println(f"【scrollElement().e={e}】")

    def find_element_by_accessibility_id(self, id, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_element_by_accessibility_id(id)
            return by_id
        except:
            return None
            pass

    def find_element_by_id(self, id, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_element_by_id(id)
            return by_id
        except:
            pass

    def find_elements_by_id(self, id, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_elements_by_id(id)
            return by_id
        except:
            pass

    def find_element_by_class_name(self, class_name, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_element_by_class_name(class_name)
            return by_id
        except:
            pass

    def find_element_by_xpath(self, xpath, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_element_by_xpath(xpath)
            return by_id
        except:
            pass

    def scan_all_text_elment(self, driver=None, text_type='text|content-desc'):
        '''
        输出所有带文本的控件id和内容
        :param text_type:
        :param driver:
        :return:
        '''
        contents = []
        try:
            driver = driver or self.driver
            txtItems = self.find_elements_by_xpath("//*", driver)
            if txtItems:
                for txitem in txtItems:
                    split = text_type.split('|')
                    if len(split) > 0:
                        for type in split:
                            content = self.get_text_elment(txitem, type)
                            if content:
                                contents.append(content)
        except Exception as e:
            Logger.println(f"【scan_all_text_elment().e={e}】")
            pass
        return contents

    def get_text_elment(self, txitem, text_type='text'):
        attribute = txitem.get_attribute(text_type)
        if attribute and str.strip(attribute):
            Logger.println(f"【找到{text_type}={attribute}")
            content = {}
            content['text'] = attribute
            try:
                resourceId = txitem.get_attribute("resource-id")
                content['resourceId'] = resourceId
                class_name = txitem.get_attribute('className')
                content['className'] = class_name
            except:
                pass
            return content
        else:
            return None

    def find_elements_by_xpath(self, xpath, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_elements_by_xpath(xpath)
            return by_id
        except:
            pass

    def getContentTextById(self, id, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_element_by_id(id)
            if by_id:
                content = by_id.get_attribute("text")
                if content is None:
                    pass
                Logger.println(content)
                return content
        except:
            pass

    def getContentText(self, driver=None):
        driver = driver or self.driver
        try:
            by_id = driver.find_element_by_class_name("android.widget.TextView")
            if by_id:
                content = by_id.get_attribute("text")
                if content is None:
                    pass
                Logger.println(content)
                return content
        except:
            pass

    def MD5(self, content):
        return hashlib.md5(content.encode(encoding='UTF-8')).hexdigest()

    def get_screenshot_as_base64(self, content_element):
        try:
            return content_element.screenshot_as_base64
        except Exception as e:
            Logger.println(f"【save_screenshot().e={e}】")
            return time_util.get_time()

    def save_screenshot(self, content_element, dir, file_name):
        """
        :param content_element:
        :param dir:
        :param file_name:
        :return:
        """
        try:
            full_dir = FilePathUtil.get_full_dir("wxfriend", "pic", dir)
            if not os.path.exists(full_dir):
                os.mkdir(full_dir)
            content_element.screenshot(FilePathUtil.get_full_dir(full_dir, file_name))
            return True
        except Exception as e:
            Logger.println(f"【save_screenshot().e={e}】")
            return False
