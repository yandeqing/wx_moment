#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/12/9 18:39
'''
import json

import cpca
import numpy as np
import pandas as pd


def recongnize_address():
    global pd
    location_str = ["陕西南路188弄洋房二楼 温馨舒适一室户 仅租6800 陕西南路地铁步行2分钟"]
    pd = cpca.transform(location_str, pos_sensitive=True)
    print(pd.keys)
    print(pd.values)
    array = np.array(pd)[0]
    keys = list(pd)
    data = {}
    for index in range(len(keys)):
        data[keys[index]] = array[index]
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    recongnize_address()
