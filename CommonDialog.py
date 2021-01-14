import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QDialog, QDialogButtonBox, \
    QApplication, QLayout, QBoxLayout, QMessageBox
from qtpy import QtCore, QtWidgets

from common import FilePathUtil
from config.AppConfig import MonitorConfig
from wxfriend import WxConfig, WxAppUploader
from wxfriend.window_main_function_manager import DownloadRunthread


class CommonDialog(QDialog):
    def __init__(self, parent=None):
        super(CommonDialog, self).__init__(parent)
        result = QMessageBox.warning(self, '提示', '是否保存文件并输出', QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)  # 默认关闭界面选择No
        if result == QMessageBox.Yes:
            self.confirm()
        else:
            self.close()



    def confirm(self):
        print("confirm")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CommonDialog()
    win.show()
    win.setMinimumSize(560, 100)
    sys.exit(app.exec_())
