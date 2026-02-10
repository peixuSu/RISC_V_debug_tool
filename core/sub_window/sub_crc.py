#!/usr/bin/env python3.13
"""
filename: sub_crc.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-11-25
description: CRC配置子窗口，处理CRC校验相关的配置和设置
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from core.ui.Ui_sub_crc import Ui_SubForm_CRC


class SubWindowCRC(QWidget):
    """
    CRC配置子窗口类，负责处理CRC校验相关的配置和设置
    """
    # 定义CRC更新信号，用于通知主窗口CRC配置已更改
    crc_updated = Signal(int)

    # 用户自定义标志
    user_define = False

    def __init__(self, application):
        """
        初始化CRC配置子窗口
        
        Args:
            application: 应用程序实例
        """
        super().__init__()

         # 初始化UI界面
        self.ui = Ui_SubForm_CRC()
        self.ui.setupUi(self)

        # 设置窗口标题
        self.setWindowTitle("CRC修改页面")

        # 保存父窗口引用
        self.application = application

        # 初始化CRC相关控件状态
        self.crc_init()

        # 如果父窗口当前CRC模式设置不等于-1，则启用CRC配置
        if self.application.current_crc_mode != -1:
            self.ui.check_box_crc_enable.setChecked(True)
            self.crc_enable()

        # 连接信号与槽函数
        self.ui.check_box_crc_enable.stateChanged.connect(self.crc_enable)
        self.ui.button_crc_confirm.clicked.connect(self.crc_confirm)
        self.ui.button_crc_cancel.clicked.connect(self.crc_close)        

    def crc_init(self):
        """
        初始化CRC相关控件状态
        
        将所有CRC配置相关的控件设置为禁用状态
        """
        # 定义需要禁用的控件列表
        setEnable_widgets = [
            self.ui.combo_box_crc_range,
            self.ui.combo_box_crc_type,
            self.ui.combo_box_crc_width,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.check_box_in_reversal,
            self.ui.check_box_out_reversal,
            self.ui.check_box_high_first
        ]

        # 禁用所有CRC配置控件
        for widget in setEnable_widgets:
            widget.setEnabled(False)

    def crc_enable(self):
        """
        启用或禁用CRC配置控件
        
        根据CRC启用复选框的状态，启用或禁用相关配置控件
        """
        # 获取CRC启用状态
        is_enabled = self.ui.check_box_crc_enable.isChecked()

         # 定义需要清空的控件列表
        clear_widgets = [
            self.ui.combo_box_crc_range,
            self.ui.combo_box_crc_type,
            self.ui.combo_box_crc_width,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
        ]

        # 定义需要设置启用状态的控件列表
        setEnable_widgets = [
            self.ui.combo_box_crc_range,
            self.ui.combo_box_crc_type,
            self.ui.combo_box_crc_width,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.line_edit_crc_poly,
            self.ui.line_edit_crc_formula,
            self.ui.line_edit_crc_init,
            self.ui.line_edit_crc_xorout,
            self.ui.check_box_in_reversal,
            self.ui.check_box_out_reversal,
            self.ui.check_box_high_first
        ]
        
        # 定义需要设置选中状态的复选框列表
        check_boxes = [
            self.ui.check_box_in_reversal,
            self.ui.check_box_out_reversal,
            self.ui.check_box_high_first
        ]

        # 根据启用状态管理控件
        if not is_enabled:
             # 如果未启用CRC，则清空并禁用所有相关控件
            for widget in clear_widgets:
                widget.clear()

            for widget in setEnable_widgets:
                widget.setEnabled(False)

            for check_box in check_boxes:
                check_box.setChecked(False)
        else:
            # 如果启用CRC，则初始化相关配置选项
            self.crc_range()
            self.crc_type()
            self.crc_16_user_show()

    def crc_range(self):
        """
        设置CRC范围选项
        
        添加并启用CRC范围下拉框的选项
        """
        # 添加CRC范围选项并启用控件
        self.ui.combo_box_crc_range.addItems(["写校验"])
        self.ui.combo_box_crc_range.setEnabled(True)
    
    def crc_type(self):
        """
        设置CRC类型选项
        
        添加并启用CRC类型下拉框的选项
        """
        # 添加CRC类型选项并启用控件
        self.ui.combo_box_crc_type.addItems(["CRC-16(自定义)"])
        self.ui.combo_box_crc_type.setEnabled(True)

    def crc_16_user_show(self):
        """
        显示CRC-16用户配置
        
        设置CRC-16的默认参数值
        """
        # 设置CRC宽度为16
        self.ui.combo_box_crc_width.addItems(["16"])
        
        # 设置CRC多项式
        self.ui.line_edit_crc_poly.setText("8005")
        
        # 设置CRC公式
        self.ui.line_edit_crc_formula.setText("x16 + x15 + x2 + 1")
        
        # 设置CRC初始值
        self.ui.line_edit_crc_init.setText("FFFF")
        
        # 设置CRC异或输出值
        self.ui.line_edit_crc_xorout.setText("0000")
        
        # 设置输入反转为False
        self.ui.check_box_in_reversal.setChecked(False)
        
        # 设置输出反转为False
        self.ui.check_box_out_reversal.setChecked(False)
        
        # 设置高位在前为True
        self.ui.check_box_high_first.setChecked(True)
    
    def crc_confirm(self):
        """
        确认CRC配置
        
        根据CRC启用状态发送相应的信号到主窗口
        """
        # 如果未启用CRC，则发送-1信号
        if not self.ui.check_box_crc_enable.isChecked():
            self.crc_updated.emit(-1)
        else:
            # 如果启用了CRC，则发送当前CRC类型的索引信号
            self.crc_updated.emit(self.ui.combo_box_crc_type.currentIndex())
        
        # 关闭当前窗口
        self.close()

    def crc_close(self):
        """
        关闭CRC配置窗口
        """
        # 关闭当前窗口
        self.close()