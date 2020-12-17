import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QDialog, QDialogButtonBox, \
    QApplication
from qtpy import QtCore, QtWidgets

from common import FilePathUtil
from config.AppConfig import MonitorConfig
from wxfriend import WxConfig, WxAppUploader
from wxfriend.window_main_function_manager import DownloadRunthread


class UpgradeHelperDialog(QDialog):
    def __init__(self, parent=None):
        super(UpgradeHelperDialog, self).__init__(parent)
        layout = QFormLayout()
        self.config = MonitorConfig()

        self.label = QLabel("更新文件地址:")
        self.le2 = QLineEdit()
        url = WxConfig.getAppDownloadUrl()
        self.le2.setText(url)
        layout.addRow(self.label, self.le2)
        self.progressLabel = QLabel("已下载 0%")
        layout.addRow(self.progressLabel)

        self.cacelButton = QPushButton("关闭")
        self.saveButton = QPushButton("升级")
        self.cacelButton.clicked.connect(self.close)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.saveButton.clicked.connect(self.save)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。
        self.buttonBox = QDialogButtonBox(QtCore.Qt.Horizontal)
        self.buttonBox.addButton(self.saveButton, QDialogButtonBox.RejectRole)
        self.buttonBox.addButton(self.cacelButton, QDialogButtonBox.YesRole)
        layout.addRow(self.buttonBox)

        self.setLayout(layout)
        self.setWindowTitle("微信运营小工具升级")
        self.setWindowIcon(QIcon('./logo.ico'))
        self.runthread = DownloadRunthread()
        self.runthread.signals.connect(self.call_backlog)

    def call_backlog(self, text):
        self.progressLabel.setText(f"{text}")

    def save(self):
        self.runthread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = UpgradeHelperDialog()
    win.show()
    win.setMinimumSize(360, 100)
    sys.exit(app.exec_())
