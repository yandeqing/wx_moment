import os
import codecs
import configparser

from common import FilePathUtil

configPath = FilePathUtil.get_full_dir('config', "test_config.ini")


# configPath = os.path.join(proDir, "config.ini")


class MonitorConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_value(self, section, name):
        if not self.cf.has_section(section):
            self.cf.add_section(section)
        if not self.cf.has_option(section, name):
            self.cf.set(section, name, "")
        value = self.cf.get(section, name)
        return value

    def set_value(self, section, name, value):
        if not self.cf.has_section(section):
            self.cf.add_section(section)
        self.cf.set(section, name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
            f.close()

    def get_users(self, name):
        return self.get_value("REGISTER_USERS", name)

    def set_users(self, name, value):
        self.set_value("REGISTER_USERS", name, value)

    def get_email(self, name):
        return self.get_value("EMAIL", name)

    def get_qiniu(self, name):
        value = self.cf.get("QINIU", name)
        return value


if __name__ == '__main__':
    monitor_config = MonitorConfig()
    config = monitor_config.cf
    # add a section(添加一个新的section)
    if not config.has_section('section2'):
        config.add_section('section2')
    # 对section1添加配置信息
    config.set('section2', 'name', 'xiaodeng')
    config.set('section2', 'age', '28')
    with open(configPath, 'w+') as f:
        config.write(f)
        f.close()

def add(a,b):
    return a+b