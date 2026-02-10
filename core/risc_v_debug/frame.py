#!/usr/bin/env python3.13
"""
filename: frame.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-12-01
description: 数据帧相关函数
"""

from utils.crc.crc_manager import CRC

# 帧头标识，用于识别数据帧的开始
Header = 0x5AA5

# 消息ID，用于标识消息的唯一性，递增
Msg_ID = 0x0000

# 命令字典定义，包含PC到MCU和MCU到PC的所有命令
CMD = {
    # PC -> MCU 命令
    "Ping": 0x0001,           # PC请求与MCU建立通用连接
    "GetCaseList": 0x0002,    # PC请求获取MCU的测试用例列表
    "Getlog": 0x0003,         # PC请求获取MCU的日志信息
    "RunCase": 0x1001,        # PC向MCU发送运行测试用例命令
    "Stop": 0x1002,           # PC向MCU发送停止命令
    "SendData": 0x1003,       # PC向MCU发送交件或其他二进制数据
    "GetCaseResult": 0x1004,  # PC请求获取测试用例执行结果
    "GetLog": 0x1005,         # PC请求获取MCU的日志信息

    # MCU -> PC 响应
    "Ack": 0x8001,            # MCU返回的通用确认响应
    "Nack": 0x8002,           # MCU返回的通用否定响应
    "CaseList": 0x8003,       # MCU返回的测试用例列表
    "CaseRunning": 0x8004,    # MCU返回的测试用例运行状态

    "CaseResult": 0x9001,     # MCU返回的测试用例执行结果
    "LogSending": 0x9002,     # MCU返回的部分日志信息
    "LogFinished": 0x9003,    # MCU返回日志信息完成标志

}

# 当前消息ID，用于跟踪消息序列
current_msg_id = Msg_ID

# 测试用例列表
# case_list = []

class Frame():
    """
    数据帧处理类
    
    负责生成发送到MCU的数据帧以及解析从MCU接收到的数据帧
    """
    def generate_frame(cmd, data=None):
        """
        生成数据帧
        
        根据提供的命令和数据生成符合协议格式的数据帧,不包含CRC校验
        
        Args:
            cmd (int): 命令码，来自CMD字典中的定义
            data (bytes, optional): 要发送的数据，默认为None
            
        Returns:
            bytearray: 生成的数据帧
        """

        global current_msg_id

        # 获取当前消息ID并递增
        msg_id = current_msg_id
        current_msg_id = (current_msg_id + 1) % 0x10000

        # 转换数据为字节格式
        if data is None:
            # 如果没有数据，则数据长度为0，负载为空
            data_length = 0
            payload = b''
        else:
            # 转换为字节格式
            payload = bytes(data)
            # 获取数据长度
            data_length = len(payload)

        # 生成数据帧
        frame = bytearray()

        # 添加帧头(2字节)
        frame.append((Header >> 8) & 0xFF)
        frame.append(Header & 0xFF)
        
        # 添加消息ID(2字节)
        frame.append((msg_id >> 8) & 0xFF)
        frame.append(msg_id & 0xFF)
        
        # 添加命令码(2字节)
        frame.append((cmd >> 8) & 0xFF)
        frame.append(cmd & 0xFF)
        
        # 添加数据长度(4字节)
        frame.append((data_length >> 24) & 0xFF)
        frame.append((data_length >> 16) & 0xFF)
        frame.append((data_length >> 8) & 0xFF)
        frame.append(data_length & 0xFF)
        
        # 添加负载数据
        frame.extend(payload)

        # 返回生成的数据帧
        return frame

    def parse_receive_frame(receive_data, use_crc=False):
        """
        解析接收到的数据帧
        
        验证帧格式的正确性，提取帧中的各个字段，并可选择进行CRC校验
        
        Args:
            receive_data (bytes): 接收到的原始数据
            use_crc (bool): 是否使用CRC校验，默认为False
            
        Returns:
            tuple: (success, msg_id, cmd, payload, message)
                   - success (bool): 解析是否成功
                   - msg_id (int): 消息ID
                   - cmd (int): 命令码
                   - payload (bytes): 负载数据
                   - message (str): 状态信息或错误信息
        """

        if receive_data is None:
            return False, None, None, None, "接收到的数据为 None"

        # 基本帧长度（不包含数据和CRC）
        basic_length = 10

        # print(f"origin_receive_data: {receive_data.hex()}")

        # 检查数据长度是否足够基本帧长度
        if len(receive_data) < basic_length:
            return False,None,None,None,"data length error"
        
        # 提取并验证帧头
        header = (receive_data[0] << 8) | receive_data[1]
        if header != Header:
            # print(f"header: {header:04x}")
            return False,None,None,None,f"帧头错误：{header:04x}"
        
        # 提取消息ID
        msg_id = (receive_data[2] << 8) | receive_data[3]

        # 提取命令字
        cmd = (receive_data[4] << 8) | receive_data[5]

        # 提取数据长度
        data_length = (receive_data[6] << 24) | (receive_data[7] << 16) | (receive_data[8] << 8) | receive_data[9]
        
        # 计算期望的数据帧长度
        expected_length = basic_length + data_length

        # 如果启用CRC，则期望长度还需加上CRC字段长度(2字节)
        if use_crc:
            expected_length += 2
        
        # 检查实际接收数据长度是否满足期望长度
        if len(receive_data) < expected_length:
            payload = receive_data[basic_length:basic_length + data_length]
            # print(f"payload: {payload.hex()}")
            # print(f"receive_data: {receive_data.hex()}")
            print(f"expected_length: {expected_length}")
            print(f"real_length: {len(receive_data)}")
            return False, None, None, None, "data length error"

        # 提取负载数据
        payload = receive_data[basic_length:basic_length + data_length]

        # 如果启用CRC校验，检查CRC值是否正确
        if use_crc:
            original_data = receive_data[:basic_length + data_length]

            crc_calc = CRC.crc_16_user(original_data)

            receive_crc = (receive_data[expected_length - 2] << 8) | receive_data[expected_length - 1]
            print(f"crc_calc: {crc_calc:04x}, receive_crc: {receive_crc:04x}")

            # # 比较计算的CRC值与接收到的CRC值
            # if crc_calc != receive_crc:
            #     return False, None, None, None, "CRC error"
            
        # 解析成功，返回解析结果
        return True, msg_id, cmd, payload, "Success"

    # Parse case data from payload
    def parse_case(payload):
        """
        解析负载数据中的测试用例
        
        将接收到的字节数据解码为ASCII字符串，并按分号分割成测试用例列表
        
        Args:
            payload (bytes): 包含测试用例信息的字节数据
            
        Returns:
            list or str: 成功时返回测试用例列表，失败时返回错误信息字符串
        """
        # 如果payload是列表，则转换为字节对象
        if isinstance(payload, list):
            # 将整数列表转换为字节对象
            payload = bytes(payload)

        # 将字节数据解码为ASCII字符串
        case_str = payload.decode('ascii')

        # 按分号分割字符串得到测试用例列表
        case_list = case_str.split(';')
        # 移除空字符串
        case_list = [case for case in case_list if case]

        # print(f"case_list: {case_list}")

        # 返回测试用例列表
        return case_list


    def normal_parse(payload):
        """
        普通解析方法
        
        将接收到的字节数据解码为ASCII字符串
        
        Args:
            payload (bytes): 需要解码的字节数据
            
        Returns:
            str or str: 成功时返回解码后的字符串，失败时返回错误信息字符串
        """

        # 将字节数据解码为ASCII字符串
        str = payload.decode('ascii')
        
        # 将字节数据解码为ASCII字符串
        return str



