# coding:utf-8
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox
from qtpy import QtCore

from window import IconConfig
from window.ConfigBox import ConfigDialog
from common import Logger, FilePathUtil, Exceptionhandler
from common.FilePathUtil import startfile
from config.AppConfig import MonitorConfig
from wxfriend import WxConfig
from wxfriend.window_main_function_manager import Runthread, EventConst, StopRunthread, \
    KeyBoardRunthread


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
        win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        win.exec_()

    def openPicDir(self):
        startfile(FilePathUtil.get_full_dir('wxfriend', 'pic'))

    # def exportPhone(self):
    #     full_dir = FilePathUtil.get_full_dir("wxfriend", "excel")
    #     filepath = self.open_file(full_dir)
    #     if filepath:
    #         self.call_backlog("正在提取电话号码 ,请稍后...")
    #         self.runthread6.set_data(filepath)
    #         self.runthread6.start()

    def download(self):
        startfile(FilePathUtil.get_full_dir('dist', 'UpgradeHelper.exe'))
        self.close()

    def openPhoneDir(self):
        startfile(FilePathUtil.get_full_dir('wxfriend', 'excel', 'pic'))

    def init_ui(self):
        self.setMinimumSize(960, 760)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.config = MonitorConfig()
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

        downloadAction = QAction(QIcon('exit.png'), '下载最新版本', self)
        downloadAction.setStatusTip('下载最新版本')
        downloadAction.triggered.connect(self.download)

        # exportAction = QAction(QIcon('exit.png'), '从"描述"字段中提取手机号', self)
        # exportAction.setStatusTip('从"描述"字段中提取手机号')
        # exportAction.triggered.connect(self.exportPhone)

        # 底部状态栏
        self.statusBar().showMessage('状态栏')

        # 顶部菜单栏
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('配置')
        fileMenu.addAction(configAction)
        # exMenu = menubar.addMenu('提取手机号')
        # exMenu.addAction(exportAction)
        picMenu = menubar.addMenu('打开图片文件夹')
        picMenu.addAction(picAction)
        downloadMenu = menubar.addMenu('版本更新')
        downloadMenu.addAction(downloadAction)

        openAction = QAction(QIcon(IconConfig.SETTING_DIR), '打开手机号配置目录', self)
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

        models = [{'label': '导出微信通讯录', 'objName': 'left_label'},
                  {'label': '批量添加好友', 'objName': 'left_label'},
                  {'label': '批量修改备注为手机号', 'objName': 'left_label'},
                  {'label': '导出朋友圈信息', 'objName': 'left_label'},
                  {'label': '导出含文本朋友圈信息', 'objName': 'left_label'},
                  {'label': '导出图片到电脑', 'objName': 'left_label'},
                  {'label': '按文本内容对图片分组', 'objName': 'left_label'},
                  {'label': '上传文本到后台', 'objName': 'left_label'},
                  {'label': '上传图片到后台', 'objName': 'left_label'},
                  {'label': '开启导出图片并上传任务', 'objName': 'left_label'},
                  {'label': '恢复输入法', 'objName': 'left_label'},
                  {'label': '删除手机图片缓存', 'objName': 'left_label'},
                  {'label': '抓取当天遗漏数据', 'objName': 'left_label'},
                  {'label': '停止任务', 'objName': 'left_label'},
                  ]

        self.buttons = []
        for index, model in enumerate(models):
            btn = QtWidgets.QPushButton(model['label'])
            btn.setObjectName(model['objName'])
            self.buttons.append(btn)

        for index, btn in enumerate(self.buttons):
            self.left_layout.addWidget(btn, index, 0, 1, 3)
            if index == 0:
                btn.clicked.connect(self.clickGetContacts)
            elif index == 1:
                btn.clicked.connect(self.clickAddFriend)
            elif index == 2:
                btn.clicked.connect(self.clickModifyName)
            elif index == 3:
                btn.clicked.connect(self.clickTextWithPicMoment)
            elif index == 4:
                btn.clicked.connect(self.clickTextMoment)
            elif index == 5:
                btn.clicked.connect(self.clickExportPic)
            elif index == 6:
                btn.clicked.connect(self.clickPicClassfy)
            elif index == 7:
                btn.clicked.connect(self.clickUploadText)
            elif index == 8:
                btn.clicked.connect(self.clickUploadPic)
            elif index == 9:
                btn.clicked.connect(self.clickBatchUploadLabel)
            elif index == 10:
                btn.clicked.connect(self.clickKeyboardLabel)
            elif index == 11:
                btn.clicked.connect(self.clickClearPics)
            elif index == 12:
                btn.clicked.connect(self.clickGetLostLabel)
            elif index == 13:
                btn.clicked.connect(self.clickStopLabel)
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

        self.runthread = Runthread(EventConst.WX_CONTACT)
        self.runthread0 = Runthread(EventConst.MAIN_BULK_ADDFRIEND)
        self.runthread01 = Runthread(EventConst.MAIN_BULK_M_NAME)
        self.runthread1 = Runthread(EventConst.WX_MAIN_PIC)
        self.runthread2 = Runthread(EventConst.WX_MAIN)
        self.runthread3 = Runthread(EventConst.WX_EXPORT)
        self.runthread31 = Runthread(EventConst.WX_PICCLASSFY)
        self.runthread4 = Runthread(EventConst.WX_UPLOADER)
        self.runthread5 = Runthread(EventConst.WX_PICUPLOADER)
        self.runthread6 = Runthread(EventConst.WX_EXPORT_PHONE)
        self.runthread7 = Runthread(EventConst.WX_BATCH_UPLOAD)
        self.runthread8 = Runthread(EventConst.WX_CLEAR_PIC)
        self.runthread9 = Runthread(EventConst.WX_GET_LOST_PIC)
        self.stopRunner = StopRunthread()
        self.boardRunthread = KeyBoardRunthread()
        self.runthread.signals.connect(self.call_backlog)
        self.runthread0.signals.connect(self.call_backlog)
        self.runthread01.signals.connect(self.call_backlog)
        self.runthread1.signals.connect(self.call_backlog)
        self.runthread2.signals.connect(self.call_backlog)
        self.runthread3.signals.connect(self.call_backlog)
        self.runthread31.signals.connect(self.call_backlog)
        self.runthread4.signals.connect(self.call_backlog)
        self.runthread5.signals.connect(self.call_backlog)
        self.runthread6.signals.connect(self.call_backlog)
        self.runthread7.signals.connect(self.call_backlog)
        self.runthread8.signals.connect(self.call_backlog)
        self.runthread9.signals.connect(self.call_backlog)
        self.stopRunner.signals.connect(self.call_backlog)
        self.boardRunthread.signals.connect(self.call_backlog)

        self.right_label = QtWidgets.QTextEdit("")
        self.right_label.setPlaceholderText("日志输出区")
        self.right_label.setObjectName('right_label')
        self.right_layout.addWidget(self.right_label, 0, 0, 1, 3)
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setWindowTitle('屋聚科技自动化运营工具V2.1')
        self.setWindowIcon(QIcon(IconConfig.LOGO_DIR))
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)
        excel = WxConfig.getPhoneExcel()
        if excel:
            self.statusBar().showMessage(f'手机号文件地址:{excel}')
        else:
            self.statusBar().showMessage(f'请先点击配置菜单配置数据')

        value = self.config.get_value("wx_content", "select")
        if value == 'True':
            self.buttons[7].setEnabled(False)
        else:
            self.buttons[7].setEnabled(True)

    def call_backlog(self, text):
        self.right_label.append(f"{text}")

    def clickGetContacts(self):
        self.buttons[0].setEnabled(False)
        self.call_backlog("正在获取通讯录,请稍后...")
        self.runthread.start()

    def clickAddFriend(self):
        self.buttons[1].setEnabled(False)
        self.call_backlog("正在批量添加好友,请稍后...")
        self.runthread0.start()

    def clickModifyName(self):
        self.buttons[2].setEnabled(False)
        self.call_backlog("正在批量修改备注,请稍后...")
        self.runthread01.start()

    def clickTextWithPicMoment(self):
        self.call_backlog("正在导出朋友圈信息,请稍后...")
        self.buttons[3].setEnabled(False)
        self.runthread1.start()

    def clickTextMoment(self):
        self.buttons[4].setEnabled(False)
        self.call_backlog("导出文本朋友圈信息,请稍后...")
        self.runthread2.start()

    def clickExportPic(self):
        self.call_backlog("正在导出图片到电脑 ,请稍后...")
        self.runthread3.start()

    def clickPicClassfy(self):
        self.call_backlog("正在按文本内容对图片分组 ,请稍后...")
        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "pic")
        filepath = self.open_file(full_dir)
        if filepath:
            self.call_backlog("正在按文本内容对图片分组 ,请稍后...")
            self.runthread31.set_data(filepath)
            self.runthread31.start()

    def open_file(self, dir):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", dir,
                                                                   "All Files(*);;Text Files(*.xls)")
        print(fileName, fileType)
        return fileName

    def open_dir(self):
        config = MonitorConfig()
        value = config.get_value('leidian', 'default_dir')
        dir_path=None
        if value:
            # 选择文件夹对话框：
            dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择目录", value)
        else:
            dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择目录",
                                                                  "C://Users//Administrator//Desktop")
        if dir_path:
            config.set_value('leidian', 'default_dir',dir_path)
        print(dir_path)
        return dir_path
    def clickUploadText(self):
        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "pic")
        filepath = self.open_file(full_dir)
        if filepath:
            self.runthread4.set_data(filepath)
            self.call_backlog("正在上传文本到后台 ,请稍后...")
            self.runthread4.start()

    def clickUploadPic(self):
        full_dir = FilePathUtil.get_full_dir("wxfriend", "excel", "pic")
        filepath = self.open_file(full_dir)
        if filepath:
            self.runthread5.set_data(filepath)
            self.call_backlog("正在上传图片到后台 ,请稍后...")
            self.runthread5.start()

    def clickStopLabel(self):
        self.stopRunner.start()
        for btn in self.buttons:
            btn.setEnabled(True)

    def clickKeyboardLabel(self):
        self.boardRunthread.start()

    def clickBatchUploadLabel(self):
        filepath = self.open_dir()
        if filepath:
            self.runthread7.set_data(filepath)
            self.buttons[9].setEnabled(False)
            self.runthread7.start()


    def clickGetLostLabel(self):
        self.buttons[12].setEnabled(False)
        self.runthread9.start()

    def clickClearPics(self):
        result = QMessageBox.warning(self, '确定', '确认删除手机Weixin文件夹?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.runthread8.start()


def main():
    Exceptionhandler.main()
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
