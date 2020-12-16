# coding:utf-8
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QInputDialog, qApp

from ConfigBox import ConfigDialog
from common import Logger, FilePathUtil
from common.FilePathUtil import startfile
from wxfriend import WxConfig
from wxfriend.window_main_function_manager import Runthread, EventConst, StopRunthread


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def editConfigDialog(self):
        '''
        配置
        :return:
        '''
        win = ConfigDialog()
        win.show()
        win.setMinimumSize(720, 60)
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        win.setWindowModality(Qt.ApplicationModal)
        win.exec_()

    def openPicDir(self):
        startfile(FilePathUtil.get_full_dir('wxfriend', 'pic'))

    def openPhoneDir(self):
        startfile(FilePathUtil.get_full_dir('wxfriend', 'excel'))

    def init_ui(self):
        self.setMinimumSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        # 配置服务器地址
        configAction = QAction(QIcon('exit.png'), '配置', self)
        configAction.setShortcut('Ctrl+Alt+S')
        configAction.setStatusTip('配置')
        configAction.triggered.connect(self.editConfigDialog)
        # 配置服务器地址
        picAction = QAction(QIcon('exit.png'), '打开图片文件夹', self)
        picAction.setShortcut('Ctrl+O')
        picAction.setStatusTip('图片文件夹')
        picAction.triggered.connect(self.openPicDir)

        # 底部状态栏
        self.statusBar().showMessage('状态栏')

        # 顶部菜单栏
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('配置')
        fileMenu.addAction(configAction)
        picMenu = menubar.addMenu('打开图片文件夹')
        picMenu.addAction(picAction)

        openAction = QAction(QIcon('./uploader.png'), '打开手机号配置目录', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.openPhoneDir)
        self.toolbar = self.addToolBar('打开手机号配置目录')
        self.toolbar.addAction(openAction)

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 3, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_label_0 = QtWidgets.QPushButton("批量添加好友")
        self.left_label_0.setObjectName('left_label')
        self.left_label_01 = QtWidgets.QPushButton("批量修改备注为手机号")
        self.left_label_01.setObjectName('left_label')
        self.left_label_1 = QtWidgets.QPushButton("导出朋友圈文本")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("导出朋友圈图片")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("导出图片到电脑")
        self.left_label_3.setObjectName('left_label')
        self.left_label_4 = QtWidgets.QPushButton("上传文本到后台")
        self.left_label_4.setObjectName('left_label')
        self.left_label_5 = QtWidgets.QPushButton("上传图片到后台")
        self.left_label_5.setObjectName('left_label')

        self.left_label_6 = QtWidgets.QPushButton("停止任务")
        self.left_label_6.setObjectName('left_label')

        self.left_layout.addWidget(self.left_label_0, 0, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_01, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_4, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_5, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_6, 7, 0, 1, 3)
        self.left_widget.setStyleSheet('''
            QPushButton#left_label{
                padding:10px;
                font-family: "Arial","Microsoft YaHei","黑体","宋体",sans-serif;
            }
        ''')
        self.right_widget.setStyleSheet('''
            QTextEdit#right_label{
                font-family: "Arial","Microsoft YaHei","黑体","宋体",sans-serif;
            }
        ''')

        self.runthread0 = Runthread(EventConst.MAIN_BULK_ADDFRIEND)
        self.runthread01 = Runthread(EventConst.MAIN_BULK_M_NAME)
        self.runthread1 = Runthread(EventConst.WX_MAIN)
        self.runthread2 = Runthread(EventConst.WX_MAIN_PIC)
        self.runthread3 = Runthread(EventConst.PICCLASSFY)
        self.runthread4 = Runthread(EventConst.WX_UPLOADER)
        self.runthread5 = Runthread(EventConst.WX_PICUPLOADER)
        self.stopRunner = StopRunthread()
        self.runthread0.signals.connect(self.call_backlog)
        self.runthread01.signals.connect(self.call_backlog)
        self.runthread1.signals.connect(self.call_backlog)
        self.runthread2.signals.connect(self.call_backlog)
        self.runthread3.signals.connect(self.call_backlog)
        self.runthread4.signals.connect(self.call_backlog)
        self.runthread5.signals.connect(self.call_backlog)
        self.stopRunner.signals.connect(self.call_backlog)

        self.left_label_0.clicked.connect(self.clickLabel0)
        self.left_label_01.clicked.connect(self.clickLabel01)
        self.left_label_1.clicked.connect(self.clickLabel1)
        self.left_label_2.clicked.connect(self.clickLabel2)
        self.left_label_3.clicked.connect(self.clickLabel3)
        self.left_label_4.clicked.connect(self.clickLabel4)
        self.left_label_5.clicked.connect(self.clickLabel5)
        self.left_label_6.clicked.connect(self.clickLabel6)

        self.right_label = QtWidgets.QTextEdit("")
        self.right_label.setPlaceholderText("日志输出区")
        self.right_label.setObjectName('right_label')
        self.right_layout.addWidget(self.right_label, 0, 0, 1, 3)
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setWindowTitle('屋聚科技自动化运营工具V1.0')
        self.setWindowIcon(QIcon('./logo.ico'))
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

        self.statusBar().showMessage('Ready')

    def call_backlog(self, text):
        self.right_label.append(f"{text}")

    def clickLabel0(self):
        self.call_backlog("正在批量添加好友,请稍后...")
        try:
            self.left_label_0.setEnabled(False)
            self.runthread0.start()
        except Exception as e:
            self.call_backlog(f"【clickLabel0().Exception={e}】")
            pass

    def clickLabel01(self):
        self.call_backlog("正在批量修改备注,请稍后...")
        try:
            self.left_label_01.setEnabled(False)
            self.runthread01.start()
        except Exception as e:
            self.call_backlog(f"【clickLabel0().Exception={e}】")
            pass

    def clickLabel1(self):
        self.call_backlog("正在导出朋友圈文本,请稍后...")
        try:
            self.left_label_1.setEnabled(False)
            self.runthread1.start()
        except Exception as e:
            self.call_backlog(f"【clickLabel1().Exception={e}】")
            pass

    def clickLabel2(self):
        self.call_backlog("正在导出朋友圈图片,请稍后...")
        try:
            self.left_label_2.setEnabled(False)
            self.runthread2.start()
        except Exception as e:
            self.call_backlog(f"【clickLabel2().Exception={e}】")
            pass

    def clickLabel3(self):
        self.call_backlog("正在导出图片到电脑 ,请稍后...")
        try:
            self.left_label_3.setEnabled(False)
            self.runthread3.start()
        except Exception as e:
            self.call_backlog(f"【clickLabel3().Exception={e}】")
            pass

    def open_file(self, dir):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", dir,
                                                                   "All Files(*);;Text Files(*.xls)")
        print(fileName, fileType)
        return fileName

    def clickLabel4(self):
        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "text")
        filepath = self.open_file(full_dir)
        if filepath:
            self.runthread4.set_data(filepath)
            self.call_backlog("正在上传文本到后台 ,请稍后...")
            try:
                self.left_label_4.setEnabled(False)
                self.runthread4.start()
            except Exception as e:
                self.call_backlog(f"【clickLabel4().Exception={e}】")
                pass

    def clickLabel5(self):
        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "pic")
        filepath = self.open_file(full_dir)
        if filepath:
            self.runthread5.set_data(filepath)
            self.call_backlog("正在上传图片到后台 ,请稍后...")
            try:
                self.left_label_5.setEnabled(False)
                self.runthread5.start()
            except Exception as e:
                self.call_backlog(f"【clickLabel5().Exception={e}】")
                pass

    def clickLabel6(self):
        try:
            self.stopRunner.start()
        except Exception as e:
            self.call_backlog(f"【clickLabel6().Exception={e}】")

        self.left_label_0.setEnabled(True)
        self.left_label_01.setEnabled(True)
        self.left_label_1.setEnabled(True)
        self.left_label_2.setEnabled(True)
        self.left_label_3.setEnabled(True)
        self.left_label_4.setEnabled(True)
        self.left_label_5.setEnabled(True)


def main():
    linesStr = list(os.popen('adb  version').readlines())
    for line in linesStr:
        Logger.println(f"{line}")

    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.editConfigDialog()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
