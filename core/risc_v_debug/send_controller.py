from PySide6.QtCore import QObject, Signal, QTimer
import random
from .risc_v_case import CaseExecution  # 导入CaseExecution类
import time

class SendController(QObject):
    """
        非线程发送控制器，负责从MCU_list_test中获取item并发送
    """
    log_signal = Signal(str, int)
    finished_signal = Signal()
    
    def __init__(self, application, case_result_parser, case_manager, spi_controller):
        super().__init__()
        self.application = application
        self.ui = self.application.ui
        self.case_result_parser = case_result_parser
        self.running = False
        
        self.clk_mode = self.ui.combo_box_clk.currentIndex()
        self.bit_order = self.ui.combo_box_bit.currentIndex()

        self.case_manager = case_manager
        self.spi_controller = spi_controller

        # 初始化变量
        self.current_item_index = 0
        self.item_count = 0
        self.round_count = 0
        self.current_round = 0
        self.mode = "循环发送"  # 默认模式
        self.current_case_name = ""
        
        # 添加停止标志
        self.user_initiated_stop = False
        
        # 用于管理定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.execute_next_case)
        
        # 添加开始时间记录和运行的case计数
        self.start_time = None
        self.executed_case_count = 0

    def start(self):
        """开始执行测试序列"""
        self.running = True
        self.user_initiated_stop = False  # 重置用户停止标志
        self.start_time = time.time()  # 记录开始时间
        self.executed_case_count = 0  # 重置执行的case计数

        # 获取模式选择
        self.mode = self.ui.comboBox_mode_select.currentText()

        # 获取是否无限循环
        self.is_endless = self.ui.checkBox_endless.isChecked()

        # 获取循环次数
        if self.is_endless is False:
            try:
                round_input_text = self.ui.lineEdit_round_input.text()
                if round_input_text.strip() == "":
                    # 如果输入为空，默认为1次
                    self.round_count = 1
                    self.log_signal.emit("未输入，使用默认值1", 1)
                else:
                    self.round_count = int(round_input_text)
                    if self.round_count <= 0:
                        self.round_count = 1
                        self.log_signal.emit("输入必须大于0，使用默认值1", 1)
            except ValueError:
                self.log_signal.emit("输入无效，使用默认值1", 1)
                self.round_count = 1
        else:
            self.round_count = 0  # 无限循环用0表示
        
        # 从MCU_list_test中获取所有item
        test_list = self.ui.MCU_list_test
        self.item_count = test_list.count()
        
        if self.item_count == 0:
            self.log_signal.emit("MCU测试列表为空，无法进行测试", 2)
            self.show_time()
            return
        
        # 初始化当前轮次
        self.current_round = 0
        
        # 开始执行第一个测例
        self.execute_next_case()

    def execute_next_case(self):
        """执行下一个测例"""
        # 检查是否仍在运行
        if not self.running:
            self.running = False
            self.show_time()
            return
        
        # 检查是否达到循环次数限制（如果不是无限循环）
        if not self.is_endless and self.round_count > 0 and self.current_round >= self.round_count:
            self.log_signal.emit("已达到设定的循环次数", 1)
            self.running = False
            self.show_time()
            return

        # 获取列表项
        test_list = self.ui.MCU_list_test

        if self.mode == "循环发送":
            # 循环发送模式
            if self.current_item_index >= self.item_count:
                # 一轮完成，开始下一轮
                self.current_item_index = 0
                self.current_round += 1
                if not self.is_endless and self.round_count > 0 and self.current_round >= self.round_count:
                    self.log_signal.emit("已达到设定的循环次数", 1)
                    self.running = False
                    self.show_time()
                    return
            list_item = test_list.item(self.current_item_index)
        elif self.mode == "随机发送":
            # 随机发送模式
            if self.item_count > 0:
                random_index = random.randint(0, self.item_count - 1)
                list_item = test_list.item(random_index)

                # 在随机模式下，每次执行完一个case就增加round计数
                # 因为每次都是随机选择，所以需要通过round计数来控制总次数
                if self.current_round >= self.round_count and self.round_count > 0:
                    self.log_signal.emit("已达到设定的随机次数", 1)
                    self.running = False
                    self.show_time()
                    return
                
                # 对于随机模式，我们增加round计数，而不是item_index
                self.current_round += 1
            else:
                list_item = None

        if not list_item:
            # 如果没有找到列表项，继续下一个
            if self.running:  # 检查是否需要继续
                if self.mode == "循环发送":
                    self.current_item_index += 1
                QTimer.singleShot(1000, self.execute_next_case)  # 非阻塞延时1s后继续
            return

        # 获取item对应的widget（这是一个CaseItemWidget）
        widget = test_list.itemWidget(list_item)
        if not widget:
            if self.running:  # 检查是否需要继续
                if self.mode == "循环发送":
                    self.current_item_index += 1
                QTimer.singleShot(1000, self.execute_next_case)  # 非阻塞延时1s后继续
            return

        # 记录当前执行的测例名称
        self.current_case_name = widget.name

        # 临时连接信号以发送数据
        widget.send_frame.connect(self.send_frame_data)
        try:
            # 开始执行测例
            # self.log_signal.emit(f"开始执行测例: {widget.name}", 1)
            widget.send_clicked()
            
            # 增加执行的case计数
            self.executed_case_count += 1
        except Exception as e:
            self.log_signal.emit(f"执行测例 {widget.name} 时出错: {str(e)}", 2)
        finally:
            # 断开临时连接
            try:
                widget.send_frame.disconnect(self.send_frame_data)
            except TypeError:
                pass  # 如果没有连接，则忽略错误

    def send_frame_data(self, frame, correct, case_name=None):
        """发送帧数据并启动CaseExecution实例来处理后续流程"""
        if correct is False:
            self.log_signal.emit("请输入正确的数据", 2)
            return
        
        try:
            # 发送数据到SPI
            self.application.spi_controller.spi_send(
                frame.hex(),
                self.clk_mode,
                self.bit_order,
                log=False
            )

            # 创建CaseExecution实例来处理后续流程
            # 注意：这里需要传递case_name参数和完成回调
            if case_name is None:
                case_name = self.current_case_name  # 如果没有传递case_name，则使用当前记录的名称
            
            # 定义完成回调，用于继续执行下一个测例
            def on_case_completion():
                # 在执行下一个测例前，先递增索引
                if self.mode == "循环发送":
                    self.current_item_index += 1
                QTimer.singleShot(3000, self.execute_next_case)  # 3秒后执行下一个测例

                    # 定义错误回调，用于在出现错误时停止控制器
            def on_error_callback(error_message=None):
                self.running = False
                self.log_signal.emit("出现错误，已终止", 2)
                if error_message:
                    self.log_signal.emit(f"错误详情: {error_message}", 2)
                self.show_time()  # 显示运行时间

            self.case_execution = CaseExecution(
                self.application,
                self.spi_controller,
                self.case_result_parser,
                self.case_manager,
                case_name,
                completion_callback=on_case_completion,  # 传递完成回调
                error_callback=on_error_callback  # 传递错误回调
            )

            # 启动CaseExecution的流程
            # self.log_signal.emit(f"启动CaseExecution来处理 {case_name} 的响应", 1)
            QTimer.singleShot(1000, lambda: self.case_execution.receive_ack_response())

        except Exception as e:
            self.log_signal.emit(f"发送数据时出错: {str(e)}", 2)
            # 即使发生错误，也要继续执行下一个测例
            QTimer.singleShot(1000, self.execute_next_case)
    
    def stop(self):
        """
            停止发送控制
        """
        self.running = False
        self.user_initiated_stop = True  # 设置用户停止标志
        # 停止任何正在运行的计时器
        if self.timer.isActive():
            self.timer.stop()
    
    def is_user_stopped(self):
        """
            检查是否是用户手动停止的
        """
        return self.user_initiated_stop
    
    def show_time(self):
        """
            发送完成信号并显示运行时间和执行的case数量
        """
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = elapsed_time % 60
            
            if hours > 0:
                time_str = f"{hours}小时{minutes}分{seconds:.2f}秒"
            elif minutes > 0:
                time_str = f"{minutes}分{seconds:.2f}秒"
            else:
                time_str = f"{seconds:.2f}秒"
            
            if self.user_initiated_stop:
                self.log_signal.emit(f"用户手动停止 - 总运行时间: {time_str}, 执行了 {self.executed_case_count} 个case", 1)
            else:
                self.log_signal.emit(f"测试完成 - 总运行时间: {time_str}, 执行了 {self.executed_case_count} 个case", 1)
        
        self.finished_signal.emit()