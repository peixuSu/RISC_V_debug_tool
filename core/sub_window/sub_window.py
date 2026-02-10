#!/usr/bin/env python3.13
"""
filename: sub_window.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-12-25
description: 子窗口基类，提供所有子窗口的通用功能和接口
"""

from PySide6.QtWidgets import QWidget
from .sub_crc import SubWindowCRC 

class SubWindow(QWidget):
    """
    子窗口基类，提供所有子窗口的通用功能和接口

    """

    def __init__(self, application):
        """
        初始化子窗口基类
        
        Args:
            application: 主应用程序实例
        """
        super().__init__()
        self.application = application
        self.ui = application.ui
    
        self.setup_connections()

    def setup_connections(self):
        """
        设置信号槽连接
        """

        self.ui.pushButton_crc_fonfig.clicked.connect(self.crc_window)

    def crc_window(self, callback_function=None):
        """
        打开CRC窗口
        """
        self.crc_window_instance = SubWindowCRC(self.application)
        self.crc_window_instance.crc_updated.connect(self.application.crc_mode_updated)
        self.crc_window_instance.show()

    
