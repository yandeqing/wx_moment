# -*- coding: utf-8 -*-
# flake8: noqa
import json

from qiniu import Auth, put_file

from common import time_util, FilePathUtil
from config.AppConfig import MonitorConfig

localReadConfig = MonitorConfig()


def upload(localfile):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = localReadConfig.get_qiniu("access_key")
    secret_key = localReadConfig.get_qiniu("secret_key")
    bucket_name = localReadConfig.get_qiniu("bucket")
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    # 上传后保存的文件名
    import os
    basename = os.path.basename(localfile)
    key = "wxmoments/" + time_util.now_to_date(
        format_string="%Y%m%d%H%M") + "/" + basename
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    ret, info = put_file(token, key, localfile)
    print("https://resources.zuber.im/" + key)
    return ret, info


if __name__ == '__main__':
    # localfile = './apk_files/app-debug.apk'
    file = FilePathUtil.get_lastmodify_file(FilePathUtil.get_full_dir("wxfriend", "pic", "WeiXin"))
    print(f"【main().file={file}】")
    ret, info = upload(file)
    print(json.dumps(ret,indent=4))
    print(info)
