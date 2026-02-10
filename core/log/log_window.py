#!/usr/bin/env python3.13
"""
filename: normal_log.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-12-31
description: 窗口类，负责处理日志显示、保存、清除、导出等操作
"""

import datetime
import os
import stat
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QMenu
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QAction
from PySide6.QtCore import Qt

class LogWindow(QWidget):
    """
    日志窗口类，负责处理日志显示、保存、清除等操作
    """

    def __init__(self, application, case_result_parser):
        """
        初始化日志窗口
        
        Args:
            application: 主应用程序实例
        """
        super().__init__()
        # 保存UI界面引用和应用程序实例
        self.ui = application.ui
        self.application = application

        self.case_result_parser = case_result_parser

        # 设置日志文本框的右键菜单策略
        self.ui.text_log.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.text_log.customContextMenuRequested.connect(self.show_text_log_menu)

        # 设置信号连接
        self.setup_connect()

    def setup_connect(self):
        """
        设置按钮信号与槽函数的连接
        """
        
        # 连接保存日志按钮点击信号
        self.ui.button_save.clicked.connect(self.log_save)

        # 连接清除日志按钮点击信号
        self.ui.button_clear.clicked.connect(self.log_clear)
        
        # 连接导出PDF按钮点击信号
        self.ui.button_mcu_export_pdf.clicked.connect(self.export_log)

    def log(self, message, state=0):
        """
        在日志窗口中记录消息并显示
        
        Args:
            message (str): 要记录的消息内容
            state (int): 消息状态，决定文本颜色
                        0 - 默认黑色（普通消息）
                        1 - 绿色（成功消息）
                        2 - 红色（错误消息）
                        3 - 蓝色（加载中消息）
        """
        # 获取当前时间并格式化为年-月-日 时:分:秒格式
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取日志文本框的光标对象，用于控制文本插入位置和格式
        cursor = self.ui.text_log.textCursor()

        # 检查光标是否在文本末尾，如果不是则移动到末尾
        if not cursor.atEnd():
            cursor.movePosition(QTextCursor.End)

        # 创建时间戳文本格式对象，设置为蓝色字体
        time_format = QTextCharFormat()
        time_format.setForeground(QColor('blue'))
        # 应用时间戳格式并插入时间戳文本
        cursor.setCharFormat(time_format)
        cursor.insertText(f"[{current_time}]:")

        # 根据消息状态创建内容文本格式对象
        content_format = QTextCharFormat()
        if state == 0:
            # 状态0：默认黑色字体
            content_format.setForeground(QColor('black'))
        elif state == 1:
            # 状态1：绿色字体（表示成功）
            content_format.setForeground(QColor('green'))
        elif state == 2:
            # 状态2：红色字体（表示错误）
            content_format.setForeground(QColor('red'))
        elif state == 3:
            # 状态3：蓝色字体（表示加载中）
            content_format.setForeground(QColor('blue'))

        # 应用内容格式并插入消息内容和换行符
        cursor.setCharFormat(content_format)
        cursor.insertText(f" {message}\n")

        # print(f"需要发送的消息:{message}")
        
        # 更新文本框的光标位置，确保新消息可见
        self.ui.text_log.setTextCursor(cursor)

    def show_text_log_menu(self, position):
        """
        显示日志文本框的右键菜单
        """
        # 创建右键菜单
        menu = QMenu(self)
        
        # 添加清除日志动作
        clear_action = QAction("清除日志", self)
        clear_action.triggered.connect(self.log_clear)
        menu.addAction(clear_action)
        
        # 添加保存日志动作
        save_action = QAction("保存日志", self)
        save_action.triggered.connect(self.log_save)
        menu.addAction(save_action)
        
        # 在鼠标位置显示菜单
        menu.exec(self.ui.text_log.viewport().mapToGlobal(position))

    def log_clear(self):
        """
        清除日志内容（带确认提示）
        """
        # 获取当前日志文本内容
        log_text = self.ui.text_log.toPlainText()

        # 只有当日志内容非空时才显示确认对话框
        if log_text:
            # 显示确认对话框询问用户是否清除日志
            reply = QMessageBox.information(
                self, '提示', '是否清除日志？',
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            # 如果用户确认清除，则清空日志文本框
            if reply == QMessageBox.StandardButton.Ok:
                self.ui.text_log.clear()

    def log_save(self):
        """
        保存日志内容到文件
        """
        # 获取日志文本内容
        log_content = self.ui.text_log.toPlainText()

        # 弹出文件保存对话框，让用户选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存日志", "log", "文本文件 (*.txt);;所有文件 (*)"
        )
        # 如果用户选择了保存路径
        if file_path:
            try:
                # 尝试将日志内容写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
            except Exception as e:
                # 如果保存失败，记录错误日志
                self.log(f"保存日志失败：{str(e)}", 2)

    def export_log(self):
        """
        设置日志相关控件的连接.
        """

        # 弹出文件保存对话框，让用户选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出日志", "log_export", "CSV文件 (*.csv)"
        )

        if file_path:
            try:
                # 尝试将日志内容写入文件
                self.case_result_parser.export_csv(file_path)

                # # 设置文件为只读
                # os.chmod(file_path, stat.S_IREAD)  # 设置为只读文件

            except Exception as e:
                # 如果保存失败，记录错误日志
                self.log(f"导出日志失败：{str(e)}", 2)

