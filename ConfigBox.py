import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qtpy import QtCore, QtWidgets

from common import FilePathUtil
from config.AppConfig import MonitorConfig
from wxfriend import WxConfig


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        layout = QFormLayout()
        self.config = MonitorConfig()

        self.label = QLabel("已连接设备名称:")
        self.le0 = QLineEdit()
        deviceId = WxConfig.getAppiumConfig()["deviceName"]
        self.le0.setPlaceholderText("未检测到设备")
        self.le0.setText(deviceId)
        layout.addRow(self.label, self.le0)
        self.label = QLabel("已连接安卓版本:")
        self.le1 = QLineEdit()
        platformVersion = WxConfig.getAppiumConfig()["platformVersion"]
        self.le1.setPlaceholderText("未检测到版本")
        self.le1.setText(platformVersion)
        layout.addRow(self.label, self.le1)

        self.label = QLabel("服务器地址:")
        self.le2 = QLineEdit()
        url = WxConfig.getServerUrl()
        self.le2.setText(url)
        layout.addRow(self.label, self.le2)

        self.label = QLabel("最大添加好友上限(人数):")
        self.le3 = QLineEdit()
        add_friend_max_count = WxConfig.get_add_friend_max_count()
        self.le3.setText(add_friend_max_count)
        layout.addRow(self.label, self.le3)

        self.addbtn = QPushButton("设置手机号文件地址")
        self.addbtn.clicked.connect(self.add_phone_excel)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.le4 = QLineEdit()
        phone_excel = WxConfig.getPhoneExcel()
        self.le4.setText(phone_excel)
        layout.addRow(self.addbtn, self.le4)

        self.cacelButton = QPushButton("重新检测")
        self.saveButton = QPushButton("保存")
        self.cacelButton.clicked.connect(self.reconnect)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.saveButton.clicked.connect(self.save)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.buttonBox = QDialogButtonBox(QtCore.Qt.Horizontal)
        self.buttonBox.addButton(self.saveButton, QDialogButtonBox.RejectRole)
        self.buttonBox.addButton(self.cacelButton, QDialogButtonBox.YesRole)
        layout.addRow(self.buttonBox)

        self.setLayout(layout)
        self.setWindowTitle("配置服务器地址")
        self.setWindowIcon(QIcon('./logo.ico'))

    def save(self):
        server_url = self.le2.text()
        WxConfig.setServerUrl(server_url)
        max = self.le3.text()
        WxConfig.set_friend_max_count(max)
        self.close()

    def reconnect(self):
        deviceId = WxConfig.getAppiumConfig()["deviceName"]
        platformVersion = WxConfig.getAppiumConfig()["platformVersion"]

        self.le0.setText(deviceId)
        self.le1.setText(platformVersion)

    def open_file(self, dir):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", dir,
                                                                   "All Files(*);;Text Files(*.xls)")
        print(fileName, fileType)
        return fileName

    def add_phone_excel(self):
        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel")
        filepath = self.open_file(full_dir)
        if filepath:
            WxConfig.setPhoneExcel(filepath)
            self.le4.setText(filepath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConfigDialog()
    win.show()
    win.setMinimumSize(720, 60)
    sys.exit(app.exec_())
