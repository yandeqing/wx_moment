#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import json
import os
import threading
from urllib import request

import requests
from qiniu import put_file

from common import FilePathUtil, excel_util, time_util, Logger
from wxfriend import wx_stop


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
        jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
        Logger.println(f"【res={jsonstr}】")
        if res_json['code'] == 0:
            return True
        else:
            return False
    except:
        return False


def files_token(type='image', count=1):
    res = requests.get(f"http://internal.zuker.im/files/token?type={type}&count={count}")
    res_json = res.json()
    jsonstr = json.dumps(res_json, indent=4, ensure_ascii=False)
    Logger.println(f"【files_token().jsonstr={jsonstr}】")
    if res_json['code'] == 0:
        return res_json['result']
    else:
        return None




def upload_img(token, file):
    # 要上传文件的本地路径
    ret, info = put_file(token, None, file)
    image_ = ret['result']['image']
    Logger.println(image_['id'])
    Logger.println(image_['src'])
    return image_['id']


def main_backgroud():
    thread = threading.Thread(target=main)
    thread.start()


def main(full_dir):
    sheetname = os.path.basename(full_dir)[0:11]
    Logger.println(f"【().excel={full_dir}】")
    Logger.println(f"【().sheetname={sheetname}】")
    array = excel_util.excel2array(full_dir, sheetname)
    for index, item in enumerate(array):
        if wx_stop.stopFlag:
            break
        content_md5 = item['content_md5']
        Logger.println(f"【().content_md5={content_md5}】")
        files = FilePathUtil.get_files_by_dir(
            FilePathUtil.get_full_dir("wxfriend", "pic", "WeiXinCopy", content_md5))
        count = len(files)
        tokens = files_token(count=count)
        img_ids = []
        for index, file in enumerate(files):
            img_id = upload_img(tokens[index], file)
            img_ids.append(str(img_id))
        join = ",".join(img_ids)
        if join:
            put_img(content_md5, join)
        else:
            Logger.println(f"【content_md5={content_md5}没有对应的图片】")


if __name__ == '__main__':
    full_dir = FilePathUtil.get_lastmodify_file(
        FilePathUtil.get_full_dir("wxfriend", "excel", "pic"))
    main(full_dir)
