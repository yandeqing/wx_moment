#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import json
import threading
import time

import requests
from qiniu import put_file

from common import FilePathUtil, excel_util, Logger
from config.AppConfig import MonitorConfig
from wxfriend import wx_stop, WxUploader, PicClassfyUtil


def put_img(md5, file_ids):
    '''
    上传图片ids
    :param md5:
    :param file_ids:
    :return:
    '''
    item = {'content_md5': md5, 'file_ids': file_ids}
    Logger.println(f"【put_img().item={item}】")
    try:
        res = requests.put("http://internal.zuker.im/moment",
                           json=item)
        res_json = res.json()
        # jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        # Logger.println(f"put_img【res={jsonstr}】")
        if res_json['code'] == 0:
            return True
        else:
            return False
    except Exception as e:
        Logger.println(f"Exception is【{e}】")
        return False


def files_token(type='image', count=1):
    try:
        res = requests.get(f"http://internal.zuker.im/files/token?type={type}&count={count}")
        res_json = res.json()
        # jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        # Logger.println(f"【files_token().jsonstr={jsonstr}】")
        if res_json['code'] == 0:
            return res_json['result']
        else:
            return None
    except Exception as e:
        Logger.println(f"Exception is【{e}】")
        return None


def upload_img(token, file):
    # 要上传文件的本地路径
    ret, info = put_file(token, None, file)
    image_ = ret['result']['image']
    # Logger.println(image_['id'])
    # Logger.println(image_['src'])
    return image_['id']


def main_backgroud():
    thread = threading.Thread(target=main)
    thread.start()


def main(full_dir):
    config = MonitorConfig()
    upload_md5_pic_position = config.get_value("wx_content", "upload_md5_pic_position")
    Logger.println(f"【().excel={full_dir}】")
    array = excel_util.excel2array(full_dir)
    # 错误
    start_index = 0
    if upload_md5_pic_position:
        Logger.println(f"【找到上次上传的下标={upload_md5_pic_position}】")
        start_index = int(upload_md5_pic_position)
    length = len(array)
    if start_index + 1 > length:
        Logger.println(f"【已经是最后一条了】")
        return
    upload_count = 0
    for index, item in enumerate(array[start_index:length]):
        if wx_stop.stopFlag:
            break
        content_md5 = item['content_md5']
        count = int(item['count'])
        if count == 0:
            Logger.println(f"【{content_md5}没有抓取到图片】")
            continue
        Logger.println(f"【().content_md5={content_md5}】")
        item['content'] = '1'
        res = WxUploader.need_upload_photo_item(item)
        # 有房源刷新的列表
        if res:
            Logger.println(f"【().开始图片上传={content_md5}】")
            try:
                files = FilePathUtil.get_files_by_dir(
                    FilePathUtil.get_full_dir("wxfriend", "pic", "WeiXinCopy", content_md5))
                tokens = files_token(count=count)
                if tokens:
                    img_ids = []
                    for index, file in enumerate(files):
                        if index > count - 1:
                            Logger.println(f"【content_md5={content_md5}图片出现重复】")
                            break
                        img_id = upload_img(tokens[index], file)
                        img_ids.append(str(img_id))
                    join = ",".join(img_ids)
                    if join:
                        put_img(content_md5, join)
                        upload_count += 1
                    else:
                        Logger.println(f"【content_md5={content_md5}没有对应的图片】")
                else:
                    Logger.println(f"【token 生成失败】")
            except Exception as e:

                break
        else:
            Logger.println(f"【()={content_md5}无需上传图片】")
    config.set_value("wx_content", "upload_md5_pic_position", length)
    Logger.println(f"【本次共完成{upload_count}条朋友圈信息的图片文件上传】")


index = 1


def batch_export_upload():
    global index
    start_time = int(time.time())
    config = MonitorConfig()
    sleeptime = 3 * 60
    value = config.get_value('appiumConfig', 'batch_pic_seconds')
    if value:
        sleeptime = int(value)
    Logger.println(
        f"【====================开始批量导出并上传图片batch_pic_seconds={sleeptime}=======================】")
    while True:
        time.sleep(5)
        time_start_time = int(time.time()) - start_time
        if sleeptime - time_start_time > 0:
            Logger.println(
                f"=================【{sleeptime - time_start_time}秒后执行第={index}个批量导出并上传图片任务===================】")
        if time_start_time >= sleeptime:
            index = index + 1
            break
        time.sleep(5)
    PicClassfyUtil.main()
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
    main(full_dir)
    if wx_stop.stopFlag:
        Logger.println(f"【===================批量导出并上传图片任务停止=================】")
        return
    batch_export_upload()


if __name__ == '__main__':
    batch_export_upload()
    # full_dir = FilePathUtil.get_lastmodify_file(
    #     FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
    # main(full_dir)
