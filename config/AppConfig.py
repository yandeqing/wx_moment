import os
import codecs
import configparser

from common import FilePathUtil

configPath =FilePathUtil.get_full_dir('config', "test_config.ini")
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
        if not self.cf.__contains__(section):
            return None
        value = self.cf.get(section, name)
        return value

    def set_value(self, section, name, value):
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
