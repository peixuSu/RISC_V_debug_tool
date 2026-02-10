from PySide6.QtCore import QTimer
from .frame import Frame, CMD

class ScanDevice:
    """设备扫描类，用于执行设备连接检测操作"""

    def __init__(self, application):
        """初始化设备扫描

        Args:
            application: 应用程序对象，用于访问全局资源
        """
        self.application = application 
        self.ui = self.application.ui

        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

    def scan(self):
        """执行测例扫描操作"""

        self.application.log_window.log("开始连接设备····", 3)

        # 生成帧
        send_data = Frame.generate_frame(CMD["Ping"])

        print("运行到生成帧")

        # self.LogManager.frame_record(Frame.current_msg_id, "Ping")  # 帧记录（被注释）

        self.application.spi_controller.spi_send(
            send_data.hex(),
            self.clk_mode,
            self.bit_order,
            log = False 
            )
        
        # 使用QTimer进行非阻塞延时
        QTimer.singleShot(int(1000), self.receive)

    def receive(self):
        """执行实际的扫描操作"""

        # 根据CRC模式接收响应数据
        if self.application.current_crc_mode == 0:
            # CRC模式下接收数据
            received_data = self.application.spi_controller.spi_receive(
                self.clk_mode,
                self.bit_order,
                20,  # 接收缓冲区大小为20字节
                log = False
            )
            # print(f"received_data: {received_data.hex()}")  # 打印接收数据（调试用）
            use_crc = True  # 设置CRC使用标志
        else:
            # 非CRC模式下接收数据
            received_data = self.application.spi_controller.spi_receive(
                self.clk_mode,
                self.bit_order,
                20  # 接收缓冲区大小为20字节
            )
            # print(f"received_data: {received_data.hex()}")  # 打印接收数据（调试用）
            use_crc = False  # 设置CRC使用标志

        print("运行到接收响应")

        # 接收到数据,恢复按钮
        self.ui.button_mcu_connect.setEnabled(True)
        self.ui.button_mcu_scan.setEnabled(True)

        # 解析接收到的帧数据
        success, _, cmd, payload, result = Frame.parse_receive_frame(received_data, use_crc)
        
        # 根据解析结果处理响应
        if success is True:
            # 解析成功，检查命令类型
            if cmd == CMD["Ack"]:
                # 收到确认响应，连接成功
                self.application.log_window.log("连接成功", 1)
                return True
            elif cmd == CMD["Nack"]:
                # 收到否定响应，连接失败
                self.application.log_window.log("RISC-V答应失败", 2)
                return False
            else:
                # 其他命令类型，记录日志
                self.application.log_window.log(f"收到未知命令：{hex(cmd)}", 2)
        else:
            # 解析失败，报告错误原因
            self.application.log_window.log(f"连接失败：{result}", 2)
            return False