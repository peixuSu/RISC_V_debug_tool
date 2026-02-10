#!/usr/bin/env python3.13
"""
filename: spi_driver.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-11-22
description:
"""

import os
import re
from ctypes import (c_int, POINTER, c_void_p, 
        c_uint32, c_ubyte, byref, windll, c_char_p
    )

class SPIDriver:
    """
    SPI设备驱动类
    
    该类封装了SPI设备的底层操作，包括设备扫描、连接、配置和数据传输。
    通过调用jtool.dll实现与硬件设备的通信。
    """

    # SPI错误代码映射表，这些错误代码对应jtool.dll返回的错误状态
    ERROR_CODES = {
        1: "参数错误",
        2: "USB 断开",
        4: "USB发送忙",
        8: "正在等待回复",
        16: "通信超时",
        32: "通信数据错误",
        64: "返回失败参数"
    }

    # 设备句柄，用于标识已打开的SPI设备
    dev_handle = None
    
    def __init__(self, usb_dev=-1):
        """
        初始化SPI驱动器
        
        加载jtool.dll并初始化SPI设备的相关函数指针。
        
        Args:
            usb_dev (int): USB设备ID，默认为-1表示使用默认设备
        Raises:
            Exception: 当jtool.dll加载失败时抛出异常
        """
        self.usb_id = usb_dev
        self.jtool = None
        self.device_name = ""
        self.dev_spi = 2  # SPI设备类型标识符，默认为2

        # 构建DLL文件的完整路径
        dll_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "jtool.dll"
        )
        
        # 加载jtool.dll动态链接库
        self.jtool = windll.LoadLibrary(dll_path)
        
        # 设置DLL函数的参数类型和返回类型，确保数据类型正确转换

        # 设备扫描函数 - 扫描可用的SPI设备
        self.jtool.DevicesScan.argtypes = [c_int, POINTER(c_int)]
        self.jtool.DevicesScan.restype = c_char_p
        
        # 设备打开函数 - 建立与SPI设备的连接
        self.jtool.DevOpen.argtypes = [c_int, c_void_p, c_int]
        self.jtool.DevOpen.restype = c_void_p

        # SPI配置函数 - 设置电压和IO电平
        self.jtool.JSPISetVcc.argtypes = [c_void_p, c_int]  # 设置VCC电压
        self.jtool.JSPISetVcc.restype = c_int
        self.jtool.JSPISetVio.argtypes = [c_void_p, c_int]  # 设置IO电压
        self.jtool.JSPISetVio.restype = c_int
        self.jtool.JSPISetSpeed.argtypes = [c_void_p, c_int]  # 设置SPI速度
        self.jtool.JSPISetSpeed.restype = c_int

        # SPI数据传输函数 - 只写模式
        self.jtool.SPIWriteOnly.argtypes = [
            c_void_p,    # 设备句柄
            c_int,       # SPI模式
            c_int,       # 数据位顺序MSB\LSB
            c_uint32,    # 数据长度
            POINTER(c_ubyte)  # 数据缓冲区指针
        ]
        self.jtool.SPIWriteOnly.restype = c_int

        # SPI数据传输函数 - 只读模式
        self.jtool.SPIReadOnly.argtypes = [
            c_void_p,    # 设备句柄
            c_int,       # SPI模式
            c_int,       # 数据位顺序MSB\LSB
            c_uint32,    # 数据长度
            POINTER(c_ubyte)  # 数据缓冲区指针
        ]
        self.jtool.SPIReadOnly.restype = c_int
        
        # 添加全双工模式函数声明
        self.jtool.SPIWriteRead.argtypes = [
            c_void_p,    # 设备句柄
            c_int,       # SPI模式
            c_int,       # 数据位顺序MSB\LSB
            c_uint32,    # 数据长度
            POINTER(c_ubyte),  # 发送数据缓冲区指针
            POINTER(c_ubyte)   # 接收数据缓冲区指针
        ]
        self.jtool.SPIWriteRead.restype = c_int

    def open_device(self):
        """
        打开SPI设备连接
        
        扫描可用的SPI设备并建立连接，配置设备的基本参数。
        
        Returns:
            tuple: (result_message, device_count, devices_string)
                - result_message (str): 操作结果信息
                - device_count (int): 设备数量，出错时为0
                - devices_string (str): 设备信息字符串，出错时为None
        """
        if self.jtool is None:
            print("错误：jtool.dll未加载")
            return "错误：jtool.dll未加载"
        
        try:
            # 关闭已存在的设备连接，重新连接前释放之前的资源
            if self.dev_handle is not None:
                self.dev_handle = None

            # 初始化设备计数器
            dev_cnt = c_int(0)

            # 获取设备列表和设备数量
            devices_str = self.jtool.DevicesScan(self.dev_spi, byref(dev_cnt))

            # 打开SPI设备连接
            # 使用指定的USB ID选择设备
            self.dev_handle = self.jtool.DevOpen(
                self.dev_spi, None, self.usb_id
            )

            # print(f"打开设备句柄: {self.dev_handle}")

            # 验证设备是否成功打开
            if not self.dev_handle:
                # print("错误：SPI设备打开失败")
                return "错误：SPI设备打开失败", 0, None
            
            # 配置设备基本参数
            # 设置默认的VCC电压、IO电平和SPI速度
            if self.dev_handle and self.jtool:
                self.jtool.JSPISetVcc(self.dev_handle, c_int(0))    # 设置VCC电压为默认值
                self.jtool.JSPISetVio(self.dev_handle, c_int(0))   # 设置IO电平为默认值
                self.jtool.JSPISetSpeed(self.dev_handle, c_int(0))   # 设置SPI速度为默认值
                # print(dev_cnt.value, devices_str)
                return f"成功：SPI设备已打开 - {self.device_name}", dev_cnt.value, devices_str

        except Exception as e:
            self.dev_handle = None
            # print(f"异常：打开设备时发生错误 - {str(e)}")
            return f"异常：打开设备时发生错误 - {str(e)}", 0, None
        
    def parse_device_info(self, devices_str):
        """
        解析设备信息字符串
        
        从设备扫描返回的字符串中提取设备类型和序列号信息。
        
        Args:
            devices_str (bytes): 设备扫描返回的原始字节字符串
        """
        # 将字节字符串解码为UTF-8文本
        device_info = devices_str.decode('utf-8')

        # 查找序列号标记位置
        sn_start = device_info.find('SN:')

        if sn_start != -1:
            # 提取SN:后面的内容
            sn_part = device_info[sn_start+3:]
            
            # 使用正则表达式匹配8位十六进制序列号
            sn_match = re.search(r'([A-F0-9]{8})', sn_part)
            
            if sn_match:
                # 获取完整的8位序列号
                full_sn = sn_match.group(1)
                # 提取序列号的后4位作为显示用序列号
                middle_sn = full_sn[4:8] if len(full_sn) >= 8 else full_sn

                # 使用正则表达式匹配设备类型
                device_type_match = re.search(r'(JTool-[A-Za-z]+)', device_info)
                device_type = device_type_match.group(1) if device_type_match else "SPI设备"
                
                # 生成格式化的设备名称: "设备类型(序列号后4位)"
                device_name = f"{device_type}({middle_sn})"
                
                return device_name


# if __name__ == "__main__":
#     driver = SPIDriver()
#     result = driver.open_device()