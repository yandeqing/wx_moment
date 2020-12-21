# coding:utf-8
import time
from threading import Thread

# 继承QThread
from PyQt5.QtCore import pyqtSignal, QThread

from common import Logger
from wxfriend import wx_main, wx_main_pic, PicClassfyUtil, WxUploader, main_bulk_addfriend, \
    WxPicUploader, main_bulk_modifyname_to_phone, wx_stop


class EventConst():
    MAIN_BULK_M_NAME = 0
    MAIN_BULK_ADDFRIEND = MAIN_BULK_M_NAME + 1
    WX_MAIN = MAIN_BULK_ADDFRIEND + 1
    WX_MAIN_PIC = WX_MAIN + 1
    WX_EXPORT = WX_MAIN + 1
    WX_PICCLASSFY = WX_EXPORT + 1
    WX_UPLOADER = WX_PICCLASSFY + 1
    WX_PICUPLOADER = WX_UPLOADER + 1


class DownloadRunthread(QThread):
    signals = pyqtSignal(str)  # 定义信号对象,传递值为str类型，使用int，可以为int类型

    def __init__(self, fuc_code=None):
        super(DownloadRunthread, self).__init__()
        self.fuc_code = fuc_code

    def run(self):
        try:
            Logger.println(f"【DownloadRunthread()开始停止】")
            from wxfriend import WxAppUploader
            download = WxAppUploader.download(self.signals)
            WxAppUploader.startfile(download)
            Logger.println(f"【DownloadRunthread()任务已经停止】")
        except Exception as e:
            Logger.println(f"【run().e={e}】")


class StopRunthread(QThread):
    signals = pyqtSignal(str)  # 定义信号对象,传递值为str类型，使用int，可以为int类型

    def __init__(self, fuc_code=None):
        super(StopRunthread, self).__init__()
        self.fuc_code = fuc_code

    def run(self):
        Logger.init(self.signals)
        try:
            Logger.println(f"【run()开始停止】")
            wx_stop.stopFlag = True
            Logger.println(f"【run()任务已经停止】")
        except Exception as e:
            Logger.println(f"【run().e={e}】")


class Runthread(QThread):
    signals = pyqtSignal(str)  # 定义信号对象,传递值为str类型，使用int，可以为int类型

    def __init__(self, fuc_code=None):
        super(Runthread, self).__init__()
        #  通过类成员对象定义信号对象
        self.fuc_code = fuc_code

    def set_data(self, data):
        self.data = data

    def stop(self):
        self.exit(-1)

    def run(self):
        Logger.init(self.signals)
        wx_stop.stopFlag = False
        try:
            if self.fuc_code == EventConst.MAIN_BULK_ADDFRIEND:
                main_bulk_addfriend.Moments().main()
            elif self.fuc_code == EventConst.MAIN_BULK_M_NAME:
                main_bulk_modifyname_to_phone.Moments().main()
            elif self.fuc_code == EventConst.WX_MAIN:
                wx_main.Moments().main()
            elif self.fuc_code == EventConst.WX_MAIN_PIC:
                wx_main_pic.Moments().main()
            elif self.fuc_code == EventConst.WX_EXPORT:
                PicClassfyUtil.export()
            elif self.fuc_code == EventConst.WX_PICCLASSFY:
                PicClassfyUtil.classify(self.data)
            elif self.fuc_code == EventConst.WX_UPLOADER:
                WxUploader.main(self.data)
            elif self.fuc_code == EventConst.WX_PICUPLOADER:
                WxPicUploader.main(self.data)
            else:
                Logger.println(f'没有响应事件={self.fuc_code}')
        except Exception as e:
            Logger.println(f"【run().e={e}】")
        # self.signals.emit("任务已完成")
