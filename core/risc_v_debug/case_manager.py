#!/usr/bin/env python3.13
"""
filename: case_manager.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-12-02
description: 管理有关测试用例的控件
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QPushButton, QLineEdit, QLabel
)
from PySide6.QtCore import Signal, Qt
from .frame import Frame, CMD

class CaseID_Manager:
    """
    用例ID管理器类
    
    负责为测试用例分配唯一的ID，并管理这些ID与用例之间的映射关系
    """
    def __init__(self):
        # 存储已处理的用例，键为用例，值为对应的ID
        self.processed_case = {}
    
    def assign_id(self, case_list):
        """
        为用例列表中的每个用例分配递增的ID
        
        Args:
            case_list (list): 需要分配ID的用例列表
            
        Process:
            1. 遍历用例列表
            2. 为每个用例生成递增的ID（从1开始）
            3. 将ID转换为大端序的2字节十六进制格式
            4. 将用例和对应的ID存储到字典中
        """

        # 为每个用例分配ID，ID递增
        for index, case in enumerate(case_list):

            # 生成从1开始的递增ID，并转换为大端序的2字节
            hex_id = (index + 1).to_bytes(2, byteorder='big')

            # 将用例和ID存入字典
            self.processed_case[case] = hex_id

    def get_processed_case(self):
        """
        获取已处理的用例字典
        
        Returns:
            dict or None: 如果processed_case不为空则返回该字典，否则返回None
        """
        # 检查processed_case字典是否为空，不为空则返回，为空则返回None
        if self.processed_case:
            return self.processed_case
        else:
            return None
    def clear_processed_case(self):
        """
        清空已处理的用例字典
        """
        self.processed_case.clear()
        
class CasePackage:
    def __init__(self):
        """
        用例打包器类
    
        负责将用例ID和负载数据打包成帧格式，便于传输
        """
        self.CMD = CMD

    def package_frame(self, case_id, payload):
        """
        将用例ID和负载数据打包成帧
        
        Args:
            case_id (bytes): 用例的唯一标识符
            payload (bytes): 负载数据
            use_crc (bool): 是否使用CRC校验
            
        Returns:
            bytearray: 打包后的帧数据
            
        Process:
            1. 创建bytearray对象存储运行用例数据
            2. 将用例ID和负载数据扩展到运行用例数据中
            3. 使用Frame.generate_frame方法生成完整的帧
            4. 返回打包好的帧数据
        """
        
        # 创建bytearray用于存储运行用例数据
        run_case_data = bytearray()

        # 将用例ID扩展到数据中
        run_case_data.extend(case_id)

        # 将负载数据扩展到数据中
        run_case_data.extend(payload)

        # 生成帧
        packaged_frame = Frame.generate_frame(
            cmd=self.CMD["RunCase"],
            data=run_case_data
        )
        
        # 返回打包好的帧
        return packaged_frame


class CaseItemWidget(QWidget):
    """
    用例项控件类
    
    继承自QWidget，用于在界面上显示单个用例项，包含名称、输入框和发送按钮
    """

    # 点击发送按钮时发出的信号，携带打包好的帧数据和发送状态
    send_frame = Signal(bytearray, bool, str)

    # 右键删除时发出的信号，携带当前控件实例
    delete_requested = Signal(QWidget)
    
    def __init__(self, name="", id=b"", mode="send", parent=None):
        """
        初始化用例项控件
        
        Args:
            name (str): 用例名称，默认为空字符串
            id (bytes): 用例ID，默认为空字节
            use_crc (bool): 是否使用CRC校验，默认为False
            mode (str): 控件模式，"send"表示发送模式，"Test"表示测试模式，默认为"send"
            parent (QWidget): 父控件，默认为None
        """
        super().__init__(parent)

        # 用例名称
        self.name = name

        # 用例ID
        self.id = id

        # 控件模式
        self.mode = mode

        # 初始化控件
        self.init_widget()
        
    def init_widget(self, button = True, delay = False):
        """
        初始化测例项控件
        
        根据不同的模式创建不同的界面元素：
        - 发送模式：包含名称标签、输入框和发送按钮
        - 测试模式：包含case+id名称标签、负载输入框和删除按钮
        """
        # 创建水平布局
        layout = QHBoxLayout(self)

        # 设置布局边距
        layout.setContentsMargins(5, 2, 5, 2)
        
        # 左侧：用例名称标签
        if self.mode == "send":
            self.name_text = QLabel(self.name)
            self.name_text.setMinimumWidth(80)  # Send模式保持原来的宽度
        elif self.mode == "Test":
            # 在Test模式下，显示为"case+id"格式
            id_int = int.from_bytes(self.id, byteorder='big') if self.id else 0
            self.name_text = QLabel(f"case{id_int}")
            self.name_text.setMaximumWidth(50)  # Test模式使用较小的宽度
        
        self.name_text.setMaximumHeight(35)
        self.name_text.setStyleSheet("color: #696969; font-weight: normal; font-size: 14px;")
        self.name_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.name_text, 2)

        # 忽略长文本换行
        self.name_text.setWordWrap(False)
        self.name_text.setTextFormat(Qt.PlainText)
        self.name_text.setTextInteractionFlags(Qt.NoTextInteraction)
        
        # 中间：负载数据输入框
        self.input_payload = QLineEdit()
        self.input_payload.setMinimumWidth(60)
        self.input_payload.setPlaceholderText("请输入负载数据...")
        self.input_payload.setText("1")
        layout.addWidget(self.input_payload, 1)

        # 根据模式创建不同的右侧控件
        if self.mode == "send":
            # 右侧：发送按钮
            self.send_button = QPushButton("发送")
            self.send_button.setMinimumSize(60, 25)
            self.send_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
            
            # 连接发送按钮点击信号
            self.send_button.clicked.connect(self.send_clicked)
            layout.addWidget(self.send_button, 1)

        elif self.mode == "Test": 
            # Test模式：只保留删除按钮，不显示延时输入框
            self.del_button = QPushButton("-")
            self.del_button.setMaximumSize(25, 25)
            layout.addWidget(self.del_button, 1)
            self.del_button.clicked.connect(self.delete_clicked)
        
        layout.addStretch()
        self.setLayout(layout)

    def send_clicked(self):
        """
        发送按钮点击事件处理函数
        
        获取输入的负载数据，将其转换为十六进制格式，然后打包成帧并发送
        
        Process:
            1. 获取输入框中的文本
            2. 验证输入是否为数字
            3. 将输入转换为十六进制格式
            4. 使用CasePackage打包帧数据
            5. 发出send_frame信号
        """

        # 获取输入框中的文本
        input_text = self.input_payload.text()

        # 检查输入是否为数字，如果不是则发送空帧并返回
        if input_text.isdigit() is False:
            self.send_frame.emit(b"", False)
            # print(f"input_text: {input_text}")
            return

        # 如果输入为空，则负载值为0，否则转换为整数
        if input_text == "":
            decimal_value = 0
        else:
            decimal_value = int(input_text)

        # 将十进制值转换为十六进制字符串
        hex_string = f"{decimal_value:X}"

        # 如果十六进制字符串长度为奇数，则在前面补0
        if len(hex_string) % 2 != 0:
            hex_string = "0" + hex_string

        # 将十六进制字符串转换为字节
        payload = bytes.fromhex(hex_string)

         # 使用CasePackage打包帧数据
        frame = CasePackage().package_frame(self.id, payload)

        # 发出发送帧信号，携带打包好的帧和发送状态True
        self.send_frame.emit(frame, True, self.name)

    def delete_clicked(self):
        """
        删除按钮点击事件处理函数
        
        发出delete_requested信号，通知父控件删除当前控件
        """
        self.delete_requested.emit(self)