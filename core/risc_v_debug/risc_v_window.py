#!/usr/bin/env python3.13
"""
filename: risc_v_window.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-12-01
description: PC-MCU连接主窗口，处理PC-MCU相关的UI连接和逻辑
"""

from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import QObject
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from .scan_device import ScanDevice
from .risc_v_case import ScanCase
from .case_manager import CaseID_Manager, CaseItemWidget
from .send_controller import SendController
# from .log.log_ import CsvManager

class RiscVWindow(QObject):
    """
    PC-RISC-V连接主窗口类，负责处理与PC-RISC-V相关的UI连接和业务逻辑.
    """

    def __init__(self, application, spi_controller,case_result_parser):
        """初始化PC-RISC-V连接窗口.

        Args:
            application: 主应用程序实例
        """

        super().__init__()
        self.application = application
        self.ui = application.ui
        self.case_manager = CaseID_Manager()
        self.spi_controller = spi_controller
        self.case_result_parser = case_result_parser

        # 设置信号连接
        self.setup_connections()
        self.log_manager = []

        # 设置拖拽功能
        self.setup_drop()
        # self.log = CsvManager()

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # 循环发送状态标志
        self.is_cycle_sending = False

    def start_cycle_send(self):
        """
        启动循环发送功能，用于自动发送测试用例
        """

        # 检查是否已经在发送
        if self.is_cycle_sending:
            self.application.log_window.log("循环发送正在进行中，请先停止当前发送任务", 0)
            return
        
        # 检查MCU_list_test是否为空
        if self.ui.MCU_list_test.count() == 0:
            self.application.log_window.log("没有可发送的测试用例，请先扫描", 2)
            return
        
        # 创建并启动循环发送控制器
        self.send_controller = SendController(
            application=self.application,
            case_result_parser=self.case_result_parser,
            case_manager=self.case_manager,
            spi_controller=self.spi_controller
        )
        
        self.send_controller.log_signal.connect(self.application.log_window.log)
        self.send_controller.finished_signal.connect(self.cycle_send_finished)
        
        self.is_cycle_sending = True
        
        # 更新UI控件状态
        self.ui.MCU_button_send.setEnabled(False)
        self.ui.MCU_button_stop.setEnabled(True)
        
        self.application.log_window.log("开始循环发送测试用例...", 0)
        self.send_controller.start()
    
    def stop_cycle_send(self):
        """
        停止循环发送功能
        """
        if hasattr(self, 'send_controller') and self.send_controller:
            self.application.log_window.log("正在停止循环发送任务...", 0)
            self.send_controller.stop()
        else:
            self.application.log_window.log("没有正在运行的循环发送任务", 2)
    
    def cycle_send_finished(self):
        """
        循环发送控制器结束后的处理
        """
        self.is_cycle_sending = False
        # 更新控件状态
        self.ui.MCU_button_send.setEnabled(True)
        self.ui.MCU_button_stop.setEnabled(False)
        
        # 区分自动完成和手动停止

        if self.send_controller.is_user_stopped():
            self.application.log_window.log("循环发送任务已由用户手动停止", 0)
        else:
            self.application.log_window.log("循环发送任务已完成", 0)

        # 清除已结束的控制器引用
        if hasattr(self, 'send_controller'):
            self.send_controller = None
    
    def setup_connections(self):
        """
        设置PC_MCU相关控件的连接.
        """

        # 连接"连接"按钮的信号
        self.ui.button_mcu_connect.clicked.connect(self.scan_device)

        # 连接"扫描"按钮的信号
        self.ui.button_mcu_scan.clicked.connect(self.scan_case)
        self.ui.MCU_button_send.clicked.connect(self.start_cycle_send)
        self.ui.MCU_button_stop.clicked.connect(self.stop_cycle_send)
        self.ui.MCU_button_test.clicked.connect(self.test_send)

    def test_send (self):
        """
        发送输入框内的数据
        """

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # 获取输入框内的数据
        data = self.ui.MCU_line_test.text()

        # 发送数据
        self.application.spi_controller.spi_send(data, self.clk_mode ,self.bit_order)


    def setup_drop(self):
        """
        设置MCU_list_case的拖拽功能.
        """
        
        self.ui.MCU_list_case.setDragEnabled(True)
        self.ui.MCU_list_case.setAcceptDrops(False)
        self.ui.MCU_list_case.setDropIndicatorShown(True)

        # 设置MCU_list_test支持接收拖拽项目
        self.ui.MCU_list_test.setAcceptDrops(True)
        self.ui.MCU_list_test.setDropIndicatorShown(True)

        # 设置拖拽事件处理器
        self.ui.MCU_list_test.dragEnterEvent = self.test_list_drag_enter_event
        self.ui.MCU_list_test.dragMoveEvent = self.test_list_drag_move_event
        self.ui.MCU_list_test.dropEvent = self.test_list_drop_event

    
    def test_list_drag_enter_event(self, event: QDragEnterEvent):
        """处理拖拽进入事件，验证拖拽数据格式.

        Args:
            event: QDragEnterEvent 拖拽进入事件对象
        """

        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def test_list_drag_move_event(self, event: QDragEnterEvent):
        """处理拖拽移动事件.

        Args:
            event: 拖拽移动事件
        """

        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def test_list_drop_event(self, event: QDropEvent):
        """处理拖拽释放事件.

        Args:
            event: 拖拽释放事件
        """

        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            # 获取被拖拽的项目
            source = event.source()
            if source != self.ui.MCU_list_case:
                event.ignore()
                return

            # 从MCU_list_case拖拽到MCU_list_test
            selected_items = source.selectedItems()
            for item in selected_items:
                # 复制项目到MCU_list_test
                self.copy_item_to_test_list(item)
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def copy_item_to_test_list(self, source_item):
        """复制项目到测试列表.

        Args:
            source_item: 源列表项
        """
        # 获取原始的CaseItemWidget
        source_widget = self.ui.MCU_list_case.itemWidget(source_item)
        
        # 创建新的CaseItemWidget测例
        test_item_widget = CaseItemWidget(
            name=source_widget.name,
            id=source_widget.id,
            mode="Test"
        )
        
        # 连接删除信号
        test_item_widget.delete_requested.connect(self.remove_test_item)
        
        # 创建新的列表项
        list_item = QListWidgetItem()
        self.ui.MCU_list_test.addItem(list_item)
        self.ui.MCU_list_test.setItemWidget(list_item, test_item_widget)
        list_item.setSizeHint(test_item_widget.sizeHint())

    def auto_add_all_cases_to_test_list(self):
        """自动将MCU_list_case中的所有测例添加到MCU_list_test中"""
        # 清空测试列表
        self.ui.MCU_list_test.clear()
        
        # 遍历MCU_list_case中的所有项目
        for i in range(self.ui.MCU_list_case.count()):
            item = self.ui.MCU_list_case.item(i)
            # 复制每个项目到测试列表
            self.copy_item_to_test_list(item)

    def remove_test_item(self, test_item_widget):
        """从测试列表中移除项目.

        Args:
            test_item_widget: 要移除的测试项控件
        """
        # 查找项目在列表中的索引
        for index in range(self.ui.MCU_list_test.count()):
            item = self.ui.MCU_list_test.item(index)
            widget = self.ui.MCU_list_test.itemWidget(item)
            if widget == test_item_widget:
                # 移除项目
                self.ui.MCU_list_test.takeItem(index)
                del item
                break

    def scan_device(self):
        """
        扫描设备功能.
        """

        self.ui.button_mcu_connect.setEnabled(False)
        self.ui.button_mcu_scan.setEnabled(False)

        print("运行到禁止控件")

        # 创建扫描设备实例并执行扫描
        self.scan_device_instance = ScanDevice(
            application=self.application, 
        )
        
        self.scan_device_instance.scan()


    def scan_case(self):
        """
        扫描测例功能.
        """

        self.ui.button_mcu_connect.setEnabled(False)
        self.ui.button_mcu_scan.setEnabled(False)

        # 创建扫描实例并执行扫描
        self.scan_instance = ScanCase(
            application=self.application,
            spi_controller=self.spi_controller,
            case_result_parser = self.case_result_parser,
            case_manager=self.case_manager
        )

        # 连接日志信号
        if hasattr(self.scan_instance, 'log_signal'):
            self.scan_instance.log_signal.connect(self.application.log_window.log)
        
        self.scan_instance.scan()