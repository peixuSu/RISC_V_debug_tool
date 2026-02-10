#!/usr/bin/env python3.13
"""
filename: spi_controller.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-11-22
description: 
"""

from PySide6.QtCore import Signal, QObject
from ctypes import c_ubyte, c_uint32, c_int
from utils.crc.crc_manager import CRC

class SPIController(QObject):
    """
    SPI控制类
    
    负责处理SPI通信的发送和接收功能
    """
    
    log_signal = Signal(str, int)

    def __init__(self, application, driver=None):
        super().__init__()

        self.application = application
        self.ui = application.ui
        self.driver = driver

    def spi_send(self, data, clk_mode, bit_order, log = True, data_name = ""):
        """
        发送SPI数据
        
        格式化输入数据，添加CRC校验（可选），并通过SPI驱动发送。
        
        Args:
            data (str): 要发送的十六进制数据字符串（例如 "A1B2C3"）
            clk_mode (int): SPI时钟模式（0-3）
            bit_order (int): 位序模式（0-1）
            crc (bool, optional): 是否添加CRC校验。默认为True。
        
        Returns:
            str: 发送结果消息
        """

        # 检查SPI设备是否已连接
        if self.driver.jtool is None or self.driver.dev_handle is None:
            self.log_signal.emit("设备未连接", 2)
            return

        data_bytes = []

        # 清理非法字符，只保留有效的十六进制字符 (0-9, A-F, a-f)
        clean_text = ''.join(c for c in data if c in '0123456789ABCDEFabcdef')

        # 如果数据长度为奇数，在前面补0
        if len(clean_text) % 2 != 0:
            clean_text = '0' + clean_text

        # 将十六进制字符串转换为字节数组
        for i in range(0, len(clean_text), 2):
            data_bytes.append(int(clean_text[i:i+2], 16))


        # 如果启用CRC校验，则计算并添加CRC16校验码
        if self.application.current_crc_mode != -1:
            crc_value = CRC.crc_16_user(data_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF
            data_bytes.append(crc_high)
            data_bytes.append(crc_low)

         # 将数据转换为C兼容的数组格式
        data_array = (c_ubyte * len(data_bytes))(*data_bytes)

        # print(f"发送的数据：{data_bytes}")
        
        # 若开启自测，使用全双工模式
        if self.ui.check_box_test.isChecked():
            
            self.spi_transfer(data, clk_mode, bit_order)
        else:
            # 否则，使用单工模式发送数据
            result = self.driver.jtool.SPIWriteOnly(
                self.driver.dev_handle,
                c_int(clk_mode),
                c_int(bit_order),
                c_uint32(len(data_bytes)),
                data_array
            )

            # print(f"发送成功: {' '.join([f'{byte:02X}' for byte in data_bytes])}")

            # 检查发送结果
            if result == 0:
                if log is True and data_name != "":
                    self.log_signal.emit(f"发送成功,{data_name},{' '.join([f'{byte:02X}' for byte in data_bytes])}", 1)
                elif log is True:
                    self.log_signal.emit(f"发送成功: {' '.join([f'{byte:02X}' for byte in data_bytes])}", 1)
            else:
                if log is True:
                    self.log_signal.emit(f"数据发送失败: {self.driver.ERROR_CODES.get(result)}", 2)

    def spi_receive(self, clk_mode, bit_order, rx_size, log = True):
        """
        从SPI设备接收数据
        
        通过SPI接口从连接的设备接收指定长度的数据，并将接收到的数据
        以十六进制格式显示在日志中。
        
        Args:
            clk_mode (int): SPI时钟模式（0-3）
            bit_order (int): 位序模式（0-1）
            rx_size (int): 要接收的数据字节数

        Returns:
            str: 接收结果消息
        """

        # 检查SPI设备是否已连接
        if self.driver.jtool is None or self.driver.dev_handle is None:
            self.log_signal.emit("设备未连接", 2)
            return

        # 创建接收数据缓冲区
        rx_buffer = (c_ubyte * rx_size)()
        
        # 通过SPI驱动接收数据
        result = self.driver.jtool.SPIReadOnly(
            self.driver.dev_handle,
            c_int(clk_mode),
            c_int(bit_order),
            c_uint32(rx_size),
            rx_buffer
        )
        
        # print(f"clk_mode: {clk_mode}, bit_order: {bit_order}, rx_size: {rx_size}")

         # 检查接收结果
        if result == 0:
            # 将接收到的数据转换为列表
            received_data = [rx_buffer[i] for i in range(rx_size)]
            
            # 格式化数据为十六进制字符串
            formatted_data = ' '.join([f"{byte:02X}" for byte in received_data])

            print(f"接收的数据：{formatted_data}")

            if log is True:
                self.log_signal.emit(f"数据接收: {formatted_data}", 1)

            return rx_buffer
        else:
            if log is True:
                self.log_signal.emit(f"数据接收失败: {self.driver.ERROR_CODES.get(result)}", 2)

    def spi_transfer(self, data, clk_mode, bit_order, log = True):
        """全双工SPI传输模式
        
        Args:
            data: 要发送的数据，可以是bytes、bytearray、list或hex字符串
            clk_mode: 时钟模式，默认为low_1edg
            bit_order: 位序，默认为msb
            
        Returns:
            bytes: 接收到的数据，如果失败则返回None
        """

        # 检查SPI设备是否已连接
        if self.driver.jtool is None or self.driver.dev_handle is None:
            self.log_signal.emit("设备未连接", 2)
            return

        data_bytes = []

        # 清理非法字符，只保留有效的十六进制字符 (0-9, A-F, a-f)
        clean_text = ''.join(c for c in data if c in '0123456789ABCDEFabcdef')

        # 如果数据长度为奇数，在前面补0
        if len(clean_text) % 2 != 0:
            clean_text = '0' + clean_text

        # 将十六进制字符串转换为字节数组
        for i in range(0, len(clean_text), 2):
            data_bytes.append(int(clean_text[i:i+2], 16))


        # 如果启用CRC校验，则计算并添加CRC16校验码
        if self.application.current_crc_mode != -1:
            crc_value = CRC.crc_16_user(data_bytes)
            crc_high = (crc_value >> 8) & 0xFF
            crc_low = crc_value & 0xFF
            data_bytes.append(crc_high)
            data_bytes.append(crc_low)

         # 将数据转换为C兼容的数组格式
        data_array = (c_ubyte * len(data_bytes))(*data_bytes)

            
        # 创建接收缓冲区
        rx_buffer = (c_ubyte * len(data_bytes))()
            
        # 执行全双工传输
        result = self.driver.jtool.SPIWriteRead(
            self.driver.dev_handle,
            c_int(clk_mode),
            c_int(bit_order),
            c_uint32(len(data_bytes)),
            data_array,
            rx_buffer
        )

        # print(f"clk_mode: {clk_mode}, bit_order: {bit_order}, data_bytes: {data_array}, rx_buffer: {rx_buffer}")

        # 检查发送结果
        if result == 0:
            if log is True:
                self.log_signal.emit(f"发送成功: {' '.join([f'{byte:02X}' for byte in data_bytes])}", 1)

                # 将接收到的数据转换为列表
                received_data = [rx_buffer[i] for i in range(len(data_bytes))]
                
                # 格式化数据为十六进制字符串
                formatted_data = ' '.join([f"{byte:02X}" for byte in received_data])

                self.log_signal.emit(f"接收成功: {formatted_data}", 1)
        else:
            if log is True:
                self.log_signal.emit(f"SPI全双工传输异常: {self.driver.ERROR_CODES.get(result)}", 2)

