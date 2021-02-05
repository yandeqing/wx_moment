import csv
import os
import re

ENCODING_GBK = 'GBK'
ENCODING_UTF8 = 'utf-8'


# r 只能读 （带r的文件必须先存在）
# r+ 可读可写 不会创建不存在的文件 从顶部开始写 会覆盖之前此位置的内容
# w+ 可读可写 如果文件存在 则覆盖整个文件不存在则创建  //要close 之后才算完成写入
# w 只能写 覆盖整个文件 不存在则创建
# a 只能写 从文件底部添加内容 不存在则创建
# a+ 可读可写 从文件顶部读取内容 从文件底部添加内容 不存在则创建

def create_csv(path, head, force=False, encoding=ENCODING_UTF8):
    if os.path.exists(path):
        if force:
            os.remove(path)
        else:
            print(f"【create_csv(文件已存在).path={path}】")
            return
    print(f"【create_csv().head={head}】")
    with open(path, "w+", newline='', encoding=encoding) as file:
        csv_file = csv.writer(file)
        csv_file.writerow(head)


def append_csv(path, array, encoding=ENCODING_UTF8):
    datas = [list(item.values()) for item in array]
    with open(path, "a+", newline='',
              encoding=encoding) as file:  # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
        csv_file = csv.writer(file)
        csv_file.writerows(datas)


def write_csv(path, array, encoding=ENCODING_UTF8):
    datas = [list(item.values()) for item in array]
    with open(path, "r+", newline='',
              encoding=encoding) as file:  # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
        csv_file = csv.writer(file)
        csv_file.writerows(datas)


def read_csv(path, encoding=ENCODING_UTF8):
    array = []
    with open(path, "r+", encoding=encoding) as file:
        csv_file = csv.reader(file)
        array = [item for item in csv_file]
    return array


def get_head_from_arr(array):
    if (len(array)) > 0:
        item = array[0]
        keys = item.keys()
        return keys


def read_csv2array(path, encoding=ENCODING_UTF8):
    arrays = []
    items = read_csv(path, encoding=encoding)
    params_keys = items[0]
    params_values = items[1:]
    for values in params_values:
        param = {}
        for index in range(len(params_keys)):
            param[params_keys[index]] = values[index]
        arrays.append(param)
    return arrays


if __name__ == "__main__":
    data = read_csv2array("bjshhshenzhenhangzhou.csv", encoding=ENCODING_GBK)
    array = []
    for index_position, item in enumerate(data):
        road = item['道路号']
        if road:
            print(f"{index_position}【main().road={item}】")
