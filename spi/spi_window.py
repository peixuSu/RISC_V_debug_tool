#!/usr/bin/env python3.13
"""
filename: spi_window.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-11-22
description: 
"""

from PySide6.QtCore import QObject
from PySide6.QtCore import QTimer, Signal
from ctypes import c_int, byref
from core.log.log_window import LogWindow
from core.log.log_manager import CaseResultParser

class SPIWindow(QObject):
    """
    SPI通信窗口类
    
    负责管理SPI配置和通信相关的用户界面交互和业务逻辑，提供设备连接管理、
    数据传输、参数配置等核心功能。
    """

    restart_timer_signal = Signal()
    
    current_clk_index = 0
    current_bit_index = 0
    current_s_or_q_index = 0
    current_size_index = 0

    def __init__(self, application, log_window, driver=None):
        """
        初始化SPI通信窗口
        
        完成SPI通信窗口的初始化工作，包括界面连接设置、配置面板状态初始化等。
        
        Args:
            application: 主窗口实例对象，提供UI访问和日志功能
            
        Note:
            初始化时会执行以下操作:
            1. 保存主窗口实例引用
            2. 设置SPI相关控件的信号槽连接
            3. 初始化配置面板折叠状态
            4. 隐藏SPI配置面板(默认折叠状态)
        """
        super().__init__()
        self.application = application
        self.ui = application.ui
        self.driver = driver
        self.log_window = log_window
        self.spi_controller = application.spi_controller

        # 默认关闭日志的折叠
        self.ui.button_fold_config.clicked.connect(self.fold_spi_config)
        self.visible_state = False
        self.ui.spi_config_widget.setVisible(False)

        self.ui.button_refresh.clicked.connect(self.refresh_connect)
        self.ui.button_receive.clicked.connect(self.spi_receive)

        # 设备定时器，检测设备连接状态
        self.device_detection_timer = QTimer(self)
        self.device_detection_timer.timeout.connect(self.setup_connect)
        self.device_detection_timer.start(500)  # 每1秒检测一次

        self.restart_timer_signal.connect(self._restart_timer_safe)

        # 标记设备是否已连接
        self.device_connected = False

        self.vcc_index = False
        self.io_index = False
        self.speed_index = False
        self.clk_index = False
        self.bit_index = False
        self.s_or_q_index = False
        self.size_index = False


    def _restart_timer_safe(self):
        """在GUI线程中安全地重启定时器"""
        if not self.device_detection_timer.isActive():
            self.device_detection_timer.start(1000)

    def spi_receive(self):
        """
        接收SPI数据
        
        从SPI设备接收数据并显示在日志窗口中。
        """

        self.spi_controller.spi_receive(
            self.ui.combo_box_clk.currentData(),
            self.ui.combo_box_bit.currentData(),
            self.ui.combo_box_size.currentData()
        )

    def fold_spi_config(self):
        """
        折叠/展开SPI配置面板
        
        切换SPI配置面板的显示状态，实现配置区域的折叠和展开功能。
        """
        if self.visible_state:
            self.ui.spi_config_widget.setVisible(False)
            self.visible_state = False
        else:
            self.ui.spi_config_widget.setVisible(True)
            self.visible_state = True
    
    def vcc_changed(self, index):
        """
        VCC电压值变更处理
        
        响应VCC电压选择下拉框的变化事件，设置SPI设备的VCC输出电压。
        
        Args:
            index (int): 选中的电压选项索引
        """
        if not self.device_connected or self.driver.dev_handle is None:
            return

        try:
            result = self.driver.jtool.JSPISetVcc(
                self.driver.dev_handle, c_int(index)
            )
            if result != 0:
                self.log_window.log(f"VCC设置失败,{self.driver.ERROR_CODES.get(result)}",2)
                return

            # self.log_window.log(f"VCC设置为: {self.ui.combo_box_vcc.currentText()}",1)

            # self.application.yaml_window.update_spi_config()

            # 存储索引值
            self.vcc_index = index

        except Exception as e:
            self.log_window.log(f"VCC设置失败: {str(e)}",2)


    def io_changed(self, index):
        """
        IO电压值变更处理
        
        响应IO电压选择下拉框的变化事件，设置SPI设备的IO接口电压。
        
        Args:
            index (int): 选中的电压选项索引
        """
        if not self.device_connected or self.driver.dev_handle is None:
            return

        try:
            result = self.driver.jtool.JSPISetVio(
                self.driver.dev_handle, c_int(index)
            )
            if result != 0:
                self.log_window.log(f"IO电压设置失败,{self.driver.ERROR_CODES.get(result)}",2)
                return

            # self.log_window.log(f"IO电压设置为: {self.ui.combo_box_io.currentText()}",1)

            # self.application.yaml_window.update_spi_config()

            # 存储索引值
            self.io_index = index
        except Exception as e:
            self.log_window.log(f"IO电压设置失败: {str(e)}",2)


    def speed_changed(self, index):
        """
        SPI通信速度变更处理
        
        响应SPI速度选择下拉框的变化事件，设置SPI设备的通信时钟频率。
        
        Args:
            index (int): 选中的速度选项索引
        """
        if not self.device_connected or self.driver.dev_handle is None:
            return

        try:
            result = self.driver.jtool.JSPISetSpeed(
                self.driver.dev_handle, c_int(index)
            )
            if result != 0:
                self.log_window.log(f"SPI速度设置失败,{self.driver.ERROR_CODES.get(result)}",2)
                return
            
            # self.log_window.log(f"SPI速度设置为: {self.ui.combo_box_speed.currentText()}",1)

            # self.application.yaml_window.update_spi_config()

            # 存储索引值
            self.speed_index = index
        except Exception as e:
            self.log_window.log(f"SPI速度设置失败: {str(e)}",2)

    def clk_changed(self, index):
        """
        SPI时钟模式变更处理
        
        响应SPI时钟模式选择下拉框的变化事件，更新主窗口的时钟模式配置。
        
        Args:
            index (int): 选中的时钟模式索引
        """
        if not self.device_connected or self.driver.dev_handle is None:
            return

        SPIWindow.current_clk_index = index

        # self.log_window.log(f"SPI时钟模式设置为: {self.ui.combo_box_clk.currentText()}",1)

        # self.application.yaml_window.update_spi_config()

        # 存储索引值
        self.clk_index = index

    def bit_changed(self, index):
        """
        SPI位序模式变更处理
        
        响应SPI位序选择下拉框的变化事件，更新主窗口的数据位序配置。
        
        Args:
            index (int): 选中的位序模式索引
        """
        if not self.device_connected or self.driver.dev_handle is None:
            return
        
        SPIWindow.current_bit_index = index

        # self.log_window.log(f"SPI位序设置为: {self.ui.combo_box_bit.currentText()}",1)

        # self.application.yaml_window.update_spi_config()

        # 存储索引值
        self.bit_index = index

    def s_or_q_changed(self, index):
        """
        SPI模式变更处理
        
        响应SPI模式选择下拉框的变化事件，更新主窗口的SPI通信模式配置。
        
        Args:
            index (int): 选中的SPI模式索引
        """
        if not self.device_connected or self.driver.dev_handle is None:
            return

        SPIWindow.current_s_or_q_index = index
        
        # self.log_window.log(f"SPI模式设置为: {self.ui.combo_box_s_or_q.currentText()}",1)

        # self.application.yaml_window.update_spi_config()

        # 存储索引值
        self.s_or_q_index = index

    def size_changed(self, index):
        """
        接收数据长度变更处理
        
        响应接收数据长度选择下拉框的变化事件，更新主窗口的SPI接收数据长度配置。
        
        Args:
            index (int): 选中的数据长度选项索引
        """
        if not self.device_connected or self.driver.dev_handle is None:
            return

        SPIWindow.current_size_index = index
        
        # self.log_window.log(f"接收数据字节数设置为: {self.ui.combo_box_size.currentText()}",1)

        # self.application.yaml_window.update_spi_config()

        # 存储索引值
        self.size_index = index

    def spi_combobox_init(self):
        """
        初始化SPI配置下拉框选项
        
        为所有SPI相关配置的下拉框添加选项项，并建立信号槽连接。
        设置默认的配置参数值。
        
        配置项包括:
            - VCC电压: 5V、=IO、关闭
            - IO电压: 3.3V、1.8V
            - 通信速度: 468.75KHz到60MHz共8档
            - 时钟模式: 4种CPOL/CPHA组合
            - 位序模式: MSB、LSB
            - SPI模式: 全单线SPI
            - 接收长度: 2字节到64字节共6档
        
        Note:
            初始化时会设置默认参数值:
            - VCC: 关闭(索引2)
            - IO: 1.8V(索引1)  
            - 速度: 468.75KHz(索引0)
        """
        self.ui.combo_box_vcc.addItem("5V", 0)
        self.ui.combo_box_vcc.addItem("=IO", 1)
        self.ui.combo_box_vcc.addItem("关闭", 2)

        self.ui.combo_box_io.addItem("3.3V", 0)
        self.ui.combo_box_io.addItem("1.8V", 1)

        self.ui.combo_box_speed.addItem("468.75K", 0)
        self.ui.combo_box_speed.addItem("937.5K", 1)
        self.ui.combo_box_speed.addItem("1.875M", 2)
        self.ui.combo_box_speed.addItem("3.75M", 3)
        self.ui.combo_box_speed.addItem("7.5M", 4)
        self.ui.combo_box_speed.addItem("15M", 5)
        self.ui.combo_box_speed.addItem("30M", 6)
        self.ui.combo_box_speed.addItem("60M", 7)

        self.ui.combo_box_clk.addItem("LOW/1EDG", 0)
        self.ui.combo_box_clk.addItem("LOW/2EDG", 1)
        self.ui.combo_box_clk.addItem("HIGH/1EDG", 2)
        self.ui.combo_box_clk.addItem("HIGH/2EDG", 3)

        self.ui.combo_box_bit.addItem("MSB", 0)
        self.ui.combo_box_bit.addItem("LSB", 1)

        self.ui.combo_box_s_or_q.addItem("全单线SPI", 0)

        self.ui.combo_box_size.addItem("2字节", 2)
        self.ui.combo_box_size.addItem("4字节", 4)
        self.ui.combo_box_size.addItem("8字节", 8)
        self.ui.combo_box_size.addItem("16字节", 16)
        self.ui.combo_box_size.addItem("32字节", 32)
        self.ui.combo_box_size.addItem("64字节", 64)

        self.ui.combo_box_vcc.currentIndexChanged.connect(self.vcc_changed)
        self.ui.combo_box_io.currentIndexChanged.connect(self.io_changed)
        self.ui.combo_box_speed.currentIndexChanged.connect(self.speed_changed)
        self.ui.combo_box_clk.currentIndexChanged.connect(self.clk_changed)
        self.ui.combo_box_bit.currentIndexChanged.connect(self.bit_changed)
        self.ui.combo_box_s_or_q.currentIndexChanged.connect(self.s_or_q_changed)
        self.ui.combo_box_size.currentIndexChanged.connect(self.size_changed)

    def setup_connect(self):
        """
        建立SPI设备连接
        
        通过调用驱动程序的设备扫描功能，检测SPI设备是否连接。
        """
        try:
            # 仅执行设备扫描，不每次都打开设备
            dev_cnt = c_int(0)
            devices_str = self.driver.jtool.DevicesScan(self.driver.dev_spi, byref(dev_cnt))
            # print(f"设备数量: {dev_cnt.value}, 设备信息: {devices_str}")

            # 检查是否有设备连接
            if dev_cnt.value > 0 and devices_str and devices_str != b'':

                # 检查是否之前未连接设备
                if self.device_connected:
                    return
                
                # 检测到新设备，建立连接
                result_msg, _, _ = self.driver.open_device()
                if self.driver.dev_handle is not None:
                    # print(f"SPIWindow:dev_handle: {self.driver.dev_handle}")
                    self.device_connected = True

                    # 解析设备信息并显示在界面上
                    device_name = self.driver.parse_device_info(devices_str)
                    self.ui.line_device.setText(device_name)
                            
                    # 初始化SPI配置下拉框
                    self.spi_combobox_init()
                    self.set_combox_index()

                    # 连接成功后，设置按键颜色为绿色
                    self.ui.button_fold_config.setStyleSheet("background-color: #BFFFCE;")
                    # print(f"连接情况: {result_msg}")

                    self.log_window.log("设备连接成功", 1)
            else:
                # 没有检测到设备，如果之前是连接状态则断开连接
                if self.device_connected:
                    self.device_connected = False
                    self.driver.dev_handle = None  # 清除设备句柄

                    # 清空设备信息显示框
                    self.ui.line_device.clear()
                    self.spi_combobox_clear()

                    # 恢复按键颜色
                    self.ui.button_fold_config.setStyleSheet("")
                    
                    self.log_window.log("设备已断开")

        except Exception as e:
            self.log_window.log(f"设备检测异常: {str(e)}")

    def refresh_connect(self):
        """
        刷新设备连接
        
        手动触发设备连接刷新，检测是否连接SPI设备。
        """

        if self.device_connected is False:
            self.setup_connect()

    def spi_combobox_clear(self):
        """
        清空所有SPI配置下拉框选项
        
        在断开设备连接时调用，清空所有SPI相关配置下拉框的选项。
        """
        
        self.ui.combo_box_vcc.clear()
        self.ui.combo_box_io.clear()
        self.ui.combo_box_speed.clear()
        self.ui.combo_box_clk.clear()
        self.ui.combo_box_bit.clear()
        self.ui.combo_box_s_or_q.clear()
        self.ui.combo_box_size.clear()

        self.ui.combo_box_vcc.currentIndexChanged.disconnect(self.vcc_changed)
        self.ui.combo_box_io.currentIndexChanged.disconnect(self.io_changed)
        self.ui.combo_box_speed.currentIndexChanged.disconnect(self.speed_changed)
        self.ui.combo_box_clk.currentIndexChanged.disconnect(self.clk_changed)
        self.ui.combo_box_bit.currentIndexChanged.disconnect(self.bit_changed)
        self.ui.combo_box_s_or_q.currentIndexChanged.disconnect(self.s_or_q_changed)
        self.ui.combo_box_size.currentIndexChanged.disconnect(self.size_changed)
    
    def set_combox_index(self):
        """
        手动再一次设置下拉框索引
        """

        if self.vcc_index is not False:
            self.ui.combo_box_vcc.setCurrentIndex(self.vcc_index)

        if self.io_index is not False:
            self.ui.combo_box_io.setCurrentIndex(self.io_index)

        if self.speed_index is not False:
            self.ui.combo_box_speed.setCurrentIndex(self.speed_index)

        if self.clk_index is not False:
            self.ui.combo_box_clk.setCurrentIndex(self.clk_index)

        if self.bit_index is not False:
            self.ui.combo_box_bit.setCurrentIndex(self.bit_index)

        if self.s_or_q_index is not False:
            self.ui.combo_box_s_or_q.setCurrentIndex(self.s_or_q_index)

        if self.size_index is not False:
            self.ui.combo_box_size.setCurrentIndex(self.size_index)
