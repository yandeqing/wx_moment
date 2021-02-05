import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QDialog, QDialogButtonBox, \
    QApplication, QCheckBox
from qtpy import QtCore, QtWidgets

from common import FilePathUtil, Logger
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

        self.label = QLabel("任务暂停后继续执行的时间间隔(秒):")
        self.le31 = QLineEdit()
        max_count = WxConfig.get_addfriend_inte_seconds()
        self.le31.setText(max_count)
        layout.addRow(self.label, self.le31)

        self.label = QLabel("每次抓取任务上线数量(条):")
        self.le32 = QLineEdit()
        crawl_max_count = WxConfig.get_crawl_max_count()
        self.le32.setText(crawl_max_count)
        layout.addRow(self.label, self.le32)

        self.label = QLabel("批量导出图片上传脚本时间间隔(秒):")
        self.le41 = QLineEdit()
        batch_pic_seconds = self.config.get_value('appiumConfig', 'batch_pic_seconds')
        self.le41.setText(batch_pic_seconds)
        layout.addRow(self.label, self.le41)

        self.addbtn = QPushButton("设置手机号文件地址")
        self.addbtn.clicked.connect(self.add_phone_excel)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.le4 = QLineEdit()
        phone_excel = WxConfig.getPhoneExcel()
        self.le4.setText(phone_excel)
        layout.addRow(self.addbtn, self.le4)

        self.label5 = QLabel("最新朋友圈图片md5值")
        self.le5 = QLineEdit()
        self.config = MonitorConfig()
        md5_pic = self.config.get_value("wx_content", "md5_pic")
        self.le5.setText(md5_pic)
        layout.addRow(self.label5, self.le5)

        self.label6 = QLabel("最新朋友圈文本md5值")
        self.le6 = QLineEdit()
        self.config = MonitorConfig()
        md5 = self.config.get_value("wx_content", "md5")
        self.le6.setText(md5)
        layout.addRow(self.label6, self.le6)

        self.label7 = QLabel("抓取文本时同时同步到云端")
        self.select_checkbox = QCheckBox("")
        value = self.config.get_value("wx_content", "select")
        if value=='True':
            self.select_checkbox.setChecked(True)
        else:
            self.select_checkbox.setChecked(False)

        layout.addRow(self.label7, self.select_checkbox)
        self.label8 = QLabel("是否输出日志")
        self.log_checkbox = QCheckBox("")
        if Logger.debug:
            self.log_checkbox.setChecked(True)
        else:
            self.log_checkbox.setChecked(False)
        layout.addRow(self.label8, self.log_checkbox)

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
        self.config.set_value('appiumConfig', 'driver_server', server_url)

        max = self.le3.text()
        self.config.set_value('appiumConfig', 'addFriendMaxCount', max)

        addfriend_inte_seconds = self.le31.text()
        self.config.set_value('appiumConfig', 'addfriend_inte_seconds', addfriend_inte_seconds)

        crawl_max_count = self.le32.text()
        self.config.set_value('appiumConfig', 'crawl_max_count', crawl_max_count)

        md5_pic = self.le5.text()
        self.config.set_value("wx_content", "md5_pic", md5_pic)

        md5 = self.le6.text()
        self.config.set_value("wx_content", "md5", md5)

        select = self.select_checkbox.isChecked()
        self.config.set_value("wx_content", "select", str(select))
        selectLog = self.log_checkbox.isChecked()
        Logger.debug=selectLog

        batch_pic_seconds = self.le41.text()
        self.config.set_value('appiumConfig', 'batch_pic_seconds',batch_pic_seconds)
        self.close()


    def reconnect(self):
        config = WxConfig.getAppiumConfig()
        deviceId = config["deviceName"]
        platformVersion = config["platformVersion"]

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
