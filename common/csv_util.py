import csv

ENCODING = 'utf-8'


def create_csv(path, head):
    print(f"【create_csv().head={head}】")
    with open(path, "w+", newline='', encoding=ENCODING) as file:
        csv_file = csv.writer(file)
        csv_file.writerow(head)


def append_csv(path, array):
    datas = [list(item.values()) for item in array]
    with open(path, "a+", newline='',
              encoding=ENCODING) as file:  # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
        csv_file = csv.writer(file)
        csv_file.writerows(datas)


def read_csv(path):
    array = []
    with open(path, "r+", encoding=ENCODING) as file:
        csv_file = csv.reader(file)
        array = [item for item in csv_file]
    return array


def get_head_from_arr(array):
    if (len(array)) > 0:
        item = array[0]
        keys = item.keys()
        return keys


def excel2array(path):
    arrays = []
    items = read_csv(path)
    print(f"【excel2array().excel2array={items}】")
    params_keys = items[0]
    params_values = items[1:]
    for values in params_values:
        param = {}
        for index in range(len(params_keys)):
            param[params_keys[index]] = values[index]
        arrays.append(param)
    return arrays


def main():
    array = [{'name': '小红', 'sex': 12}, {'name': '小王', 'sex': 112}]
    path = "example.csv"
    keys = get_head_from_arr(array)
    create_csv(path, keys)
    append_csv(path, array)
    data = excel2array(path)
    print("data:", data)


if __name__ == "__main__":
    main()
