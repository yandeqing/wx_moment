#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/6/11 17:50
'''
import os
import re

import xlrd

import xlwt

from common import FilePathUtil, Logger

proDir = FilePathUtil.getProjectRootDir()


def get_xls(xlsPath, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    file = xlrd.open_workbook(xlsPath)
    sheet = file.sheet_by_name(sheet_name)
    nrows = sheet.nrows
    for i in range(nrows):
        if i > 0:
            cls.append(sheet.row_values(i))
    return cls


def get_xls_heads(xlsPath, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    file = xlrd.open_workbook(xlsPath)
    sheet = file.sheet_by_name(sheet_name)
    return sheet.row_values(0)


def excel2array(xlsPath, sheet_name):
    try:
        arrays = []
        params_keys = get_xls_heads(xlsPath, sheet_name)
        Logger.println(f"【excel2array().params_keys={params_keys}】")
        params_values = get_xls(xlsPath, sheet_name)
        for values in params_values:
            param = {}
            for index in range(len(params_keys)):
                param[params_keys[index]] = values[index]
            arrays.append(param)
        return arrays
    except:
        return None


def modify(xlsx_path, sheet_name, case_name, model):
    '''
    :param xlsx_path: "excelCase", "biz_roomCase.xlsx"
    :param sheet_name:  biz_beds_state
    :param case_name: biz_beds_state2
    :return:
    '''
    from xlutils.copy import copy
    # 打开想要更改的excel文件
    old_excel = xlrd.open_workbook(filename=xlsx_path)
    # 将操作文件对象拷贝，变成可写的workbook对象
    new_excel = copy(old_excel)
    # 获得第一个sheet的对象
    sheet = old_excel.sheet_by_name(sheet_name)  # 通过名称获取
    names = old_excel.sheet_names()
    ws = new_excel.get_sheet(names.index(sheet_name))
    nrows = sheet.nrows
    value_x = 0
    values = []
    for i in range(nrows):
        Logger.println(sheet.row_values(i))
        for index, name in enumerate(sheet.row_values(i)):
            if name == case_name:
                value_x = i
                Logger.println(f"【modify().index={value_x}】")
    for i in range(nrows):
        Logger.println(sheet.row_values(i))
        for index, name in enumerate(sheet.row_values(i)):
            keys = model.keys()
            if name in keys:
                value = {
                    'value_x': value_x,
                    'value_y': index,
                    'value': model[name]
                }
                values.append(value)
    for value in values:
        Logger.println(f"【modify().value={value}】")
        # 写入数据
        ws.write(value['value_x'], value['value_y'], value['value'])
    # 另存为excel文件，并将文件命名
    new_excel.save(xlsx_path)


def title_write(worksheet, rows):
    # 生成标题
    for i in range(0, len(rows)):
        col = worksheet.col(i)
        col.width = 256 * 26
        # if 0 <= i <= 2:
        #     worksheet.col(i).width = 256 * 18 * 4
        style = xlwt.easyxf(
            'font:height 200, name 微软雅黑, colour_index black, bold on;align: horiz center;')
        worksheet.write(0, i, rows[i], style)


def data_write(ws, data):
    for num, rows in enumerate(data):
        rows_write(ws, num + 1, rows)


style = xlwt.easyxf('font:height 200, name 微软雅黑;')  # 字体自定义


def rows_write(ws, row_x, item):
    Logger.println(f"【rows_write().item={item}】")
    style.alignment.wrap = 1  # 自动换行
    for num, value in enumerate(item):
        value = value if value != None else ''
        pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        url = re.findall(pattern, value)
        if len(url) > 0:
            s = str(url[0])
            if (len(s) <= 255):
                value = xlwt.Formula('HYPERLINK("%s","链接详情")' % s)
        ws.write(row_x, num, value, style)


def write_excel(filename, worksheet_name, items):
    if not os.path.exists(filename):
        f = open(filename, "w+")
        f.close()
    '''
    :return:
    '''
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(worksheet_name)
    if len(items) > 0:
        keys = list(items[0].keys())
        Logger.println(f"【write_excel().keys={keys}】")
        title_write(worksheet, keys)
    excel_items = []
    for item in items:
        values = list(item.values())
        excel_items.append(values)
    data_write(worksheet, excel_items)
    workbook.save(filename)



if __name__ == '__main__':
    # full_dir = FilePathUtil.get_full_dir("business_service/test.xls")
    # datas = [{'id': 1, 'text': "dsd"},
    #          {'id': 2, 'text': "dsd2"},
    #          {'id': 3, 'text': "dsd3"}]
    # write_excel(full_dir, 'test', datas)
    full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "手机号列表.xls")
    array = excel2array(full_dir, "手机号列表")
    for item in array:
        phone = int(item['手机'])
        Logger.println(f"【main().array={phone}】")

