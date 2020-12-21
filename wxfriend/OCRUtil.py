#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import pytesseract
from PIL import Image


def recognize_img_to_text(img_path):
    img = Image.open(img_path)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    s = pytesseract.image_to_string(img, lang='chi_sim')  # 不加lang参数的话，默认进行英文识别
    # print(s.replace(" ", "").replace('\n',''))
    return s


if __name__ == '__main__':
    text = recognize_img_to_text('./pic/ocr.jpg')
    print(text)
