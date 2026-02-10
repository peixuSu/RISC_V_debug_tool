#!/usr/bin/env python3.13
"""
filename: application.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-11-22
description: 
"""

from PySide6.QtWidgets import QWidget, QMessageBox, QStatusBar
from PySide6.QtCore import Qt, QTimer
from .ui.Ui_application import Ui_Application
from spi.spi_window import SPIWindow
from spi.spi_controller import SPIController
from spi.spi_driver import SPIDriver
from .sub_window.sub_window import SubWindow
from .log.log_window import LogWindow
from .log.log_manager import CaseResultParser
from .risc_v_debug.risc_v_window import RiscVWindow

# from utils.crc.crc_manager import CRC

class Applicaton(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Application()
        self.ui.setupUi(self)
        self.driver = SPIDriver()

        # self.yaml_template = YAMLTemplate()

        # 初始化当前CRC模式为0 (默认使用CRC)
        self.current_crc_mode = 0

        self.case_result_parser = CaseResultParser()

        # 初始化日志窗口
        self.log_window = LogWindow(self,self.case_result_parser)

        # 初始化SPI窗口
        self.spi_controller = SPIController(self, self.driver)
        self.spi_controller.log_signal.connect(self.log_window.log)
        self.spi_window = SPIWindow(self, self.log_window, self.driver)

        # 初始化窗口
        self.risc_v_window = RiscVWindow(self, self.spi_controller,self.case_result_parser)

        # 初始化子窗口
        self.sub_window = SubWindow(self)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("就绪")

    def closeEvent(self, event):
        """
        处理窗口关闭事件，在关闭前提示用户确认
        
        Args:
            event: 关闭事件对象
        """
        reply = QMessageBox.question(
                self, 
                '关闭确认', 
                '请确认是否关闭',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
        if reply == QMessageBox.StandardButton.Yes:
            # 用户确认关闭，接受关闭事件
            event.accept()
        elif reply == QMessageBox.StandardButton.No:
            # 用户取消关闭，忽略关闭事件
            event.ignore()

    

    def crc_mode_updated(self, crc_value):
        """
        接收CRC窗口更新信号，更新current_crc_mode
        
        Args:
            crc_value: 新的CRC值
        """
        self.current_crc_mode = crc_value

        if crc_value == 0:
            self.log_window.log("CRC-16(自定义)校验已启用", 1)
        elif crc_value == -1:
            self.log_window.log("CRC-16(自定义)校验已关闭", 1)