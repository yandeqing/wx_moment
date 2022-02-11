#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import os
import time

import pytesseract
import requests
import wget
from PIL import Image

from common.LogUtil import LogUtil


def recognize_img_to_text(img_path):
    img = Image.open(img_path)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    s = pytesseract.image_to_string(img)  # 不加lang参数的话，默认进行英文识别
    # s = pytesseract.image_to_string(img, lang='chi_sim')  # 不加lang参数的话，默认进行英文识别
    # print(s.replace(" ", "").replace('\n',''))
    return s


def downloadFile(url, name):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    response = requests.get(url, headers=headers)
    print(f"==response headers==========================")
    for item in response.headers.items():
        print(f'"{item[0]}":"{item[1]}",')
    print(f"==response headers==========================")
    open(name, 'wb').write(response.content)

def getcode(url):
    path = f"{os.path.dirname(os.path.realpath(__file__))}\\ocr.jpg"
    downloadFile(url, path)
    image = Image.open(path)
    image.show()
    image = image.convert('L')
    threshold = 100
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    result = pytesseract.image_to_string(image)
    print(result)
if __name__ == '__main__':
    url = "https://zfzl.fgj.sh.gov.cn/UserInfo/getCode?0.48995328617428524&codeKey=36540d37-4961-4d94-8dfd-2af05082df07"
    getcode(url)

