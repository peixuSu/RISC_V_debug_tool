#!/usr/bin/env python3.13
"""
filename: application.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-11-25
description: 
"""

from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from .crc_manager import CRC

class CRCWindow(QObject):
    """
    CRC窗口管理类
    
    该类负责处理应用程序中的CRC校验相关功能，包括CRC模式更新和工具提示设置
    """

    def __init__(self, application):
        super().__init__()
        """
        初始化CRC窗口管理器
        
        Args:
            application: 主应用程序实例
        """

        self.application = application
        self.ui = application.ui

        self.setup_connections()

    def setup_connections(self):
        """
        设置信号与槽的连接
        
        连接列表项的进入事件，实现鼠标悬停时更新CRC工具提示
        """

        # 连接数据列表项的悬停事件
        self.ui.list_data.entered.connect(self.update_all_crc_tooltips)

        # 连接分组列表项的悬停事件
        self.ui.list_group.entered.connect(self.update_all_crc_tooltips)

    def crc_updated(self, crc_mode):
        """
        当CRC模式更新时的处理函数
        
        根据选择的CRC模式更新应用程序的当前CRC模式，并返回相应的状态信息
        
        Args:
            crc_mode: CRC模式标识符
                     - 0: CRC-16(自定义)校验启用
                     - -1: CRC-16(自定义)校验关闭
                     - 其他值: 其他CRC模式
        
        Returns:
            str: CRC模式更新的状态信息
        """
        # 更新应用程序的当前CRC模式
        self.application.current_crc_mode = crc_mode

        # 根据CRC模式返回对应的状态信息
        if crc_mode == 0:
            return "CRC-16(自定义)校验已启用"
        elif crc_mode == -1:
            return "CRC-16(自定义)校验已关闭"
        
        # print(self.current_crc_mode)
        
        self.update_all_crc_tooltips()

    def update_all_crc_tooltips(self):
        """
        更新所有列表项的CRC工具提示
        
        遍历数据列表和分组列表中的所有项，根据当前的CRC模式重新计算并设置它们的工具提示
        """
        # 获取应用程序数据组管理器中的所有数据项列表
        list_data_items = self.application.data_group_manager.get_list_data_items()
        
        # 遍历所有数据项并更新它们的CRC工具提示
        for item in list_data_items:
            # item = self.ui.list_data.item(i)
            # 获取列表项关联的用户数据元组
            data_tuple = item.data(Qt.UserRole)

            # 检查数据元组是否存在且包含至少两个元素
            if data_tuple and len(data_tuple) >= 2:
                # 解包数据元组，获取数据文本（忽略第一个元素）
                _, data_text = data_tuple
                # 为该项设置CRC工具提示
                self.set_item_crc_tooltip(item, data_text)

        # 检查分组列表是否有项
        if self.ui.list_group.count() > 0:
            # 遍历所有分组项并更新它们的CRC工具提示
            for i in range(self.ui.list_group.count()):
                # 获取指定索引的分组项
                item = self.ui.list_group.item(i)
                # 获取列表项关联的用户数据元组
                data_tuple = item.data(Qt.UserRole)

                # 检查数据元组是否存在且包含至少两个元素
                if data_tuple and len(data_tuple) >= 2:
                    # 解包数据元组，获取数据文本（忽略第一个元素）
                    _, data_text = data_tuple
                    # 为该项设置CRC工具提示
                    self.set_item_crc_tooltip(item, data_text)

    def set_item_crc_tooltip(self, item, data_text):
        """
        为列表项设置CRC工具提示
        
        根据当前的CRC模式计算数据的CRC值，并将其显示在列表项的工具提示中
        
        Args:
            item: 列表项对象
            data_text: 数据文本，以十六进制字符串形式表示（如："A1 B2 C3"）
        """

        # 检查当前是否启用了CRC-16(自定义)校验模式
        if self.application.current_crc_mode == 0:

             # 将十六进制字符串分割并转换为字节数据
            hex_parts = data_text.strip().split()
            data_bytes = [int(part, 16) for part in hex_parts]

            # 计算CRC-16校验值
            crc_value = CRC.crc_16_user(data_bytes)

            # 将CRC值分为高字节和低字节
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF

            # 构造包含CRC校验的数据文本
            crc_data_text = data_text + f" {crc_high:02X} {crc_low:02X}"
            item.setToolTip(f"校验后数据：{crc_data_text}")
        else:
            item.setToolTip(None)
