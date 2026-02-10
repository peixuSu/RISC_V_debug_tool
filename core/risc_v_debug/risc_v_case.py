#!/usr/bin/env python3.13
"""
filename: frame.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-12-01
description: 测试用例相关函数
"""

from PySide6.QtWidgets import QListWidgetItem, QMessageBox
from PySide6.QtCore import QTimer
from datetime import datetime
# from controller.crc import CRC
from .case_manager import CaseItemWidget, CaseID_Manager
from .frame import Frame, CMD


class ScanCase:
    """实例扫描类，用于执行测例扫描操作"""
    
    def __init__(self, application, spi_controller, case_result_parser, case_manager):
        """初始化实例扫描

        Args:
            application: 应用程序对象
            delay: 扫描延迟时间（秒），默认为1秒
        """
        self.application = application
        self.ui = self.application.ui

        self.spi_controller = spi_controller

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        self.case_manager = case_manager

        self.case_result_parser = case_result_parser

    def scan(self):
        """执行测例扫描操作"""

        self.application.log_window.log("开始扫描测例····", 3)

        send_data = Frame.generate_frame(CMD["GetCaseList"])

        # print(f"发送的数据：{send_data}，类型：{type(send_data)}")  # 打印发送数据（调试用）
        
        # 发送数据
        self.application.spi_controller.spi_send(
            send_data.hex(),
            self.clk_mode,              # SPI时钟模式
            self.bit_order,
            log = False 
        )

        # print(f"send_data: {send_data.hex()}")  # 打印发送数据（调试用）
        
        # 使用QTimer进行非阻塞延时
        QTimer.singleShot(int(1000), self.receive)

    def receive(self):
        """执行实际的扫描操作"""
        
        # 提供一个128字节的接收区域来接收数据
        received_data = self.application.spi_controller.spi_receive(
            self.clk_mode,
            self.bit_order,
            1024,                        # 接收缓冲区大小为1024字节
            log = False
        )
        
        # print(f"测试接收128字节数据：received_data: {received_data.hex()}")  # 打印接收数据（调试用）

        # 根据CRC模式设置解析标志
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # 恢复按钮
        self.ui.button_mcu_connect.setEnabled(True)
        self.ui.button_mcu_scan.setEnabled(True)

        # 解析接收到的帧数据
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查解析是否成功
        if success is False:
            self.application.log_window.log(f"获取测例失败：{result}", 2)
            return None
        
        # 检查命令是否为否定应答(Nack)
        if cmd == CMD["Nack"]:
            self.application.log_window.log("RISC-V答应失败", 2)
            return None
        
        # print(f"payload: {payload}")  # 打印负载数据（调试用）

        # 解析测例数据
        case = Frame.parse_case(payload)

        # print(f"case: {case}")  # 打印测例数据（调试用）

        self.handle_scan_case_result(case)

    def handle_scan_case_result(self, case_list):
        """处理扫描测例结果，将测例添加到MCU_list_case.

        Args:
            case_list: 测例列表
        """

        self.case_manager.clear_processed_case()

        if not case_list:
            self.application.log_window.log("测例扫描失败", 2)
            return

        # 清空现有列表
        self.ui.MCU_list_case.clear()
        
        # 为测例分配ID
        self.case_manager.assign_id(case_list)
        processed_case = self.case_manager.get_processed_case()

        # 检查处理后的用例是否为空
        if processed_case is None:
            self.application.log_window.log("没有处理任何case", 1)
            return
        
        # 为每个测例创建控件
        for name, id_bytes in processed_case.items():
            case_item = CaseItemWidget(name, id_bytes)

            case_item.send_frame.connect(self.send_frame)

            list_item = QListWidgetItem()
            self.ui.MCU_list_case.addItem(list_item)
            self.ui.MCU_list_case.setItemWidget(list_item, case_item)
            
            list_item.setSizeHint(case_item.sizeHint())
            
        self.application.log_window.log(f"获取 {len(processed_case)} 个测例", 0)

        # 通知主窗口自动将所有测例添加到测试列表
        if hasattr(self.application, 'risc_v_window'):
            QTimer.singleShot(100, lambda: self.application.risc_v_window.auto_add_all_cases_to_test_list())

    def send_frame(self, frame, correct, case_name):
        """通过SPI向MCU发送帧.

        Args:
            frame: 要发送的帧数据
            correct: 数据是否正确
        """
        if correct is False:
            QMessageBox.warning(self.application, "警告", "数据错误，请检查输入")
            return

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        # print(f"发送的数据：{frame.hex()}")
        self.spi_controller.spi_send(
            frame.hex(),
            self.clk_mode,
            self.bit_order,
            log = False
        )

        # print(f"发送的数据：{frame.hex()}")

        # 处理后续命令下发流程
        self.case_execution = CaseExecution(self.application, self.spi_controller, self.case_result_parser, self.case_manager, case_name)
        QTimer.singleShot(1000, lambda: self.case_execution.receive_ack_response())


class CaseExecution:
    """测例执行类，用于执行测例运行、获取结果和日志等操作"""
    
    def __init__(self, application, spi_controller, case_result_parser, case_manager, case_name, completion_callback=None, error_callback=None):
        self.application = application
        self.ui = self.application.ui
        self.spi_controller = spi_controller
        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()
        self.case_result_parser = case_result_parser
        self.case_manager = case_manager  # 添加对case_manager的引用
        self.log = []
        self.case_name = case_name
        self.get_case_result_retry_count = 0
        self.get_log_retry_count = 0
        self.completion_callback = completion_callback
        self.error_callback = error_callback  # 添加错误回调引用

    def receive_ack_response(self):
        """接收Ack响应."""

        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.spi_controller.spi_receive(
            self.clk_mode, 
            self.bit_order, 
            128, 
            log=False
        )

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)
        
        # 检查命令字是否为Ack
        if cmd == CMD["Ack"]:

            # Ack确认成功，开始流程二：获取CaseResult
            self.application.log_window.log("测例开始运行", 3)
            self.get_case_result_retry_count = 0
            # print("下一步开始流程二")
            self.send_get_case_result()
        else:
            self.application.log_window.log(f"收到非Ack命令：{hex(int(cmd))}", 2)
            # 在遇到错误时调用完成回调，通知send_controller停止
            if self.error_callback:
                self.error_callback()
            return
    
    def send_get_case_result(self):
        """发送GetCaseResult指令."""

        generate_frame = Frame.generate_frame(CMD["GetCaseResult"])

        self.spi_controller.spi_send(
            generate_frame.hex(), 
            self.clk_mode, 
            self.bit_order,
            log = False
        )

        # self.application.log_window.log("发送GetCaseResult指令", 1)

        # 准备接收响应
        QTimer.singleShot(1000, self.receive_case_result)

    def receive_case_result(self):
        """接收CaseResult响应."""

        # self.application.log_window.log("接收CaseResult响应", 1)
        
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.spi_controller.spi_receive(
            self.clk_mode, 
            self.bit_order, 
            1024, 
            log=False
        )

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查帧解析是否成功
        if not success:
            self.application.log_window.log(f"接收CaseResult失败：{result}", 2)
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 3:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                # 在多次尝试失败后调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return
            # 重新尝试获取CaseResult
            QTimer.singleShot(5000, self.send_get_case_result)
            return

        # 检查命令字类型
        if cmd == CMD["CaseResult"]:
            # self.application.log_window.log("测例运行完成", 1)
            self.result_parse(received_data)
            self.get_case_result_retry_count = 0
        elif cmd == CMD["CaseRunning"]:
            self.application.log_window.log(f"{self.case_name}运行中····", 3)
            # 测例运行，重新尝试获取结果
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 40:
                self.application.log_window.log("运行超时", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                # 在超时后调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return
            QTimer.singleShot(5000, self.send_get_case_result)
        elif cmd == CMD["Nack"]:
            # if bytes(payload).hex() == "250a":
            #     self.application.log_window.log("退出测试", 2)
            #     return
            
            self.application.log_window.log(f"收到Nack响应，负载: {bytes(payload).hex()}", 2)
            # Nack响应，重新尝试获取结果
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 3:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                # 在多次Nack后调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return
            QTimer.singleShot(5000, self.send_get_case_result)
        else:
            self.application.log_window.log(f"收到意外命令字：{hex(int(cmd))}，负载: {bytes(payload).hex()}", 2)
            # 重新尝试获取结果
            # 增加重试计数
            self.get_case_result_retry_count += 1
            if self.get_case_result_retry_count >= 3:
                self.application.log_window.log("无法接收到测例结果", 2)
                # 重置计数器
                self.get_case_result_retry_count = 0
                # 在收到意外命令后调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return
            QTimer.singleShot(5000, self.send_get_case_result)

    def result_parse(self, received_data):
        """解析测例结果.

        Args:
            received_data: 接收到的数据
        """

        # 检查是否使用CRC校验
        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        # 解析接收到的帧数据
        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查解析结果是否成功
        if success is False:
            self.application.log_window.log(f"接收数据失败：{result}", 2)
            # 在解析失败时调用完成回调，通知send_controller停止
            if self.error_callback:
                self.error_callback()
            return
        
        # 检查命令是否为否定应答(Nack)
        if cmd == (CMD["Nack"]):
            self.application.log_window.log("RISC-V答应失败", 2)
            self.application.log_window.log(f"负载: {bytes(payload[:2])}")
            # 在Nack响应时调用完成回调，通知send_controller停止
            if self.error_callback:
                self.error_callback()
            return
        
        if cmd == (CMD["CaseResult"]):

            if len(payload) > 3:
                self.application.log_window.log(f"测例结果负载长度过长，负载: {bytes(payload).hex()}", 2)
                # 在负载长度异常时调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return
            
            if len(payload) < 3:
                self.application.log_window.log(f"测例结果负载长度过短，负载: {bytes(payload).hex()}", 2)
                # 在负载长度异常时调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return

            # 格式化结果负载
            payload = bytes(payload)
            case_id = payload[0:2]
            case_result = payload[2]

            # 获取已处理的测例信息
            processed_result = self.case_manager.get_processed_case()

            # 查找对应的测例, 并记录测例名称
            for case_name, case_payload in processed_result.items():
                if bytes(case_id) == case_payload:
                    self.case_name = case_name
                    break

            if case_result == 0:
                self.application.log_window.log(f"{self.case_name}测试通过", 1)
                
                # 记录成功的测试结果
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.case_result_parser.save_success_result(timestamp, self.case_name, f"{self.case_name}运行结果正确")
                
                # 测例成功，直接调用完成回调
                if self.completion_callback:
                    self.completion_callback()
            elif case_result == 1:
                self.application.log_window.log(f"{self.case_name}测试未通过", 2)

                # 失败时请求日志（不立即保存失败记录）
                self.ask_log()
            else:
                self.application.log_window.log(f"测例{self.case_name}执行结果未知，负载: {bytes(payload).hex()}", 2)
                # 在未知结果时调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
        else:
            self.application.log_window.log(f"收到意外命令字：{hex(int(cmd))}，负载: {bytes(payload).hex()}", 2)
            # 对于未知结果也调用完成回调
            if self.error_callback:
                self.error_callback()
            return

    def ask_log(self):
        """
        请求获取日志信息.
        """
        self.application.log_window.log("正在请求日志信息····", 3)

        self.get_log_retry_count = 0
        
        # 发送GetLog命令
        QTimer.singleShot(1000, self.log_request)

    def log_request(self):
        """
        发送GetLog命令，请求获取日志信息.
        """

        generate_frame = Frame.generate_frame(CMD["GetLog"])
        self.spi_controller.spi_send(
            generate_frame.hex(), 
            self.clk_mode, 
            self.bit_order,
            log = False
        )

        # 准备接收Log响应
        QTimer.singleShot(1000, self.log_response)

    def log_response(self):
        """
        接收Log响应
        """

        if self.application.current_crc_mode == 0:
            use_crc = True
        else:
            use_crc = False

        received_data = self.spi_controller.spi_receive(
            self.clk_mode, 
            self.bit_order, 
            512, 
            log=False
        )

        success, msg_id, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)

        # 检查帧解析是否成功
        if not success:
            self.application.log_window.log(f"接收CaseResult失败：{result}", 2)
            # 增加重试计数
            self.get_log_retry_count += 1
            if self.get_log_retry_count >= 3:
                self.application.log_window.log("无法接收到日志信息", 2)
                # 重置计数器
                self.get_log_retry_count = 0
                # 在多次尝试失败后调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return
            # 重新尝试获取Log
            QTimer.singleShot(1000, self.log_request)
            return
        
        if cmd != CMD["LogSending"] and cmd != CMD["LogFinished"]:
            self.application.log_window.log(f"收到意外命令字：{hex(int(cmd))}，负载: {bytes(payload).hex()}", 2)
            # 增加重试计数
            self.get_log_retry_count += 1
            if self.get_log_retry_count >= 3:
                self.application.log_window.log("无法接收到日志信息", 2)
                # 重置计数器
                self.get_log_retry_count = 0
                # 在收到意外命令时调用完成回调，通知send_controller停止
                if self.error_callback:
                    self.error_callback()
                return
            # 重新尝试获取Log
            QTimer.singleShot(1000, self.log_request)
            return

        if cmd == CMD["LogSending"]:
            
            # self.log.append(bytes(payload).decode("ascii"))
            # print(f"解码成功: {bytes(payload).decode('ascii')}")

            self.log.append(bytes(payload).decode("latin-1"))
            print(f"解码成功: {bytes(payload).decode('latin-1')}") 

            QTimer.singleShot(1000, self.log_request)
                
        elif cmd == CMD["LogFinished"]:

            self.log.append(bytes(payload).decode("latin-1"))
            print(f"解码成功: {bytes(payload).decode('latin-1')}") 

            self.application.log_window.log("日志传输完成", 0)

            # 合并所有日志内容
            log = '\n'.join(self.log)
            self.application.log_window.log(f"完整日志内容: {log}", 0)

            log = ''.join(self.log)

            # 格式化时间戳
            timestamp = datetime.now().strftime("%H:%M:%S")


            # 保存失败案例的详细日志
            self.case_result_parser.save_result(timestamp, self.case_name, log)

            # 清空日志缓冲区，为下次使用做准备
            self.log.clear()

            if self.completion_callback:
                self.completion_callback()
