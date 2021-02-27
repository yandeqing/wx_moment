import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QDialog, QDialogButtonBox, \
    QApplication
from qtpy import QtCore, QtWidgets

from common import FilePathUtil
from config.AppConfig import MonitorConfig
from window import IconConfig
from wxfriend import WxConfig, WxAppUploader
from wxfriend.window_main_function_manager import DownloadRunthread


class UpgradeHelperDialog(QDialog):
    def __init__(self, parent=None):
        super(UpgradeHelperDialog, self).__init__(parent)
        layout = QFormLayout()
        self.config = MonitorConfig()

        self.updateBtn = QPushButton("替换目标文件:")
        self.le1 = QLineEdit()
        dir = WxConfig.getAppexeReplaceDir()
        self.le1.setText(dir)
        layout.addRow(self.updateBtn, self.le1)
        self.updateBtn.clicked.connect(self.clickUpdateBtn)  # 当点击save按钮时，对话框将会消失，点击Cacel按钮时，则不会消失。

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
        self.setWindowTitle("万能升级小工具")
        self.setWindowIcon(QIcon(IconConfig.LOGO_DIR))
        self.runthread = DownloadRunthread()
        self.runthread.signals.connect(self.call_backlog)

    def call_backlog(self, text):
        self.progressLabel.setText(f"{text}")

    def clickUpdateBtn(self):
        full_dir = FilePathUtil.get_full_dir("dist")
        filepath = self.open_file(full_dir)
        if filepath:
            WxConfig.setAppexeReplaceDir(filepath)
            self.le1.setText(filepath)

    def open_file(self, dir):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", dir,
                                                                   "All Files(*);;Text Files(*.exe)")
        print(fileName, fileType)
        return fileName

    def save(self):
        text = self.le1.text()
        WxConfig.setAppexeReplaceDir(text)
        self.runthread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = UpgradeHelperDialog()
    win.show()
    win.setMinimumSize(560, 100)
    sys.exit(app.exec_())
