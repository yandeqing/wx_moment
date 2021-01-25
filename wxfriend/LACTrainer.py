#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/1/21 12:44
'''
from LAC import LAC

from wxfriend.AddressUtil import get_address_by_lac, getLocFrom


def train():
    # 选择使用默认的词法分析模型
    lac = LAC()
    # 训练和测试数据集，格式一致
    train_file = "./LacModels/lac_train.tsv"
    test_file = "./LacModels/lac_test.tsv"
    lac.train(model_save_dir='./LacModels/my', train_data=train_file, test_data=test_file)

    # 使用自己训练好的模型
    my_lac = LAC(model_path='./LacModels/my')


def get_address_by_custom(texts):
    lac = LAC()
    lac.load_customization('./LacModels/custom.csv', sep=None)
    # 干预后结果
    custom_result = lac.run(texts)
    return custom_result


if __name__ == '__main__':
    # train()
    texts =str.strip(" 长中小区 中凯城市之光 凯旋路 ")
    by_lac = get_address_by_lac(texts)
    print(f"【().standard_result={by_lac}】")
    custom_result = get_address_by_custom(texts)
    print(f"【().custom_result={custom_result}】")
    loc_from = getLocFrom(custom_result)
    join = '/'.join(loc_from)
    print(f"【().custom_result={join}】")
