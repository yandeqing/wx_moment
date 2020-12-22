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

from common import FilePathUtil, Logger, time_util

proDir = FilePathUtil.getProjectRootDir()


def get_xls(xlsPath, sheet_name=None):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    file = xlrd.open_workbook(xlsPath)
    if sheet_name:
        sheet = file.sheet_by_name(sheet_name)
    else:
        sheet = file.sheets()[0]
    nrows = sheet.nrows
    for i in range(nrows):
        if i > 0:
            cls.append(sheet.row_values(i))
    return cls


def get_xls_heads(xlsPath, sheet_name=None):
    """
    get interface data from xls file
    :return:
    """
    file = xlrd.open_workbook(xlsPath)
    if sheet_name:
        sheet = file.sheet_by_name(sheet_name)
    else:
        sheet = file.sheets()[0]
    return sheet.row_values(0)


def excel2array(xlsPath, sheet_name=None):
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
    except Exception as e:
        Logger.println(f"【modify().e={e}】")
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


def data_write(ws, items):
    for num, rows in enumerate(items):
        rows_write(ws, num + 1, rows)


style = xlwt.easyxf('font:height 200, name 微软雅黑;')  # 字体自定义


def rows_write(ws, row_x, rows):
    Logger.println(f"【rows_write().rows={rows}】")
    style.alignment.wrap = 1  # 自动换行
    for num, value in enumerate(rows):
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


def write_excel_append(filename, worksheet_name, items):
    if not os.path.exists(filename):
        write_excel(filename, worksheet_name, items)
    else:
        appendData(filename, items)


def appendData(full_dir, items):
    # !/usr/bin/env python
    # -*- coding:utf-8 -*-
    from xlrd import open_workbook
    from xlutils.copy import copy
    r_xls = open_workbook(full_dir)  # 读取excel文件
    row = r_xls.sheets()[0].nrows  # 获取已有的行数
    excel = copy(r_xls)  # 将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 获取要操作的sheet
    for index, item in enumerate(items):
        Logger.println(f"【write_excel().index={row + index}】")
        values = list(item.values())
        for sub_index, sub_item in enumerate(values):
            table.write(row + index, sub_index, sub_item)  # 括号内分别为行数、列数、内容
    excel.save(full_dir)  # 保存并覆盖文件


def get_phone_from_txt(text):
    # phone_reg = re.compile("([0-9]{2,4}[-.\s]{,1}){5}", re.MULTILINE)
    phone_reg = re.compile('[0-9]{11}', re.MULTILINE)
    search = phone_reg.search(text)
    if search and search.group:
        return search.group(0).strip()
    else:
        return ''


def exportPhone(full_dir):
    array = excel2array(full_dir)
    datas = []
    phones = []
    for item in array:
        new_item = {}
        txt = get_phone_from_txt(item['描述'])
        if txt in phones:
            continue
        else:
            if txt:
                new_item['描述'] = item['描述']
                new_item['手机'] = txt
                datas.append(new_item)
                phones.append(txt)
    date = time_util.now_to_date('%Y%m%d_%H')
    des_dir = FilePathUtil.get_full_dir("wxfriend", "excel", f"手机号列表{date}.xlsx")
    write_excel(des_dir, '手机号列表', datas)
    Logger.println(f"【main().检测到重复电话号码={len(array) - len((datas))}条】")
    Logger.println(f"【main().获取到电话号码={len((datas))}条】")
    FilePathUtil.startfile(des_dir)
    return des_dir


if __name__ == '__main__':
    # full_dir = FilePathUtil.get_full_dir("business_service/test.xls")
    # datas = [{'id': 1, 'text': "dsd", "abs": 1},
    #          {'id': 2, 'text': "dsd2"},
    #          {'id': 3, 'text': "dsd3"}]
    # # write_excel(full_dir, 'test', datas)
    # full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text")
    # full_dir = FilePathUtil.get_lastmodify_file(full_dir)
    # appendData(full_dir, datas)
    full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "上架记录（1210开始）.xlsx")
    exportPhone(full_dir)
