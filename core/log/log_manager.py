#!/usr/bin/env python3.13
"""
filename: log_manager.py
author: [peixuSu]
email: [1420209272@qq.com]
date: 2025-12-31
description: 日志解析类，用于解析测试用例运行结果
"""
from datetime import datetime

import reportlab.pdfgen.canvas as canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import csv

class CaseResultParser():

    def __init__(self):
        # 失败测试的记录
        self.failure_timestamp = []
        self.failure_err_case = []
        self.failure_log_content = []
        # 成功测试的记录
        self.success_timestamp = []
        self.success_case_name = []
        self.success_log_content = []

    def save_result(self, timestamp, err_case, log_content):
        """保存失败测试用例运行结果

        Args:
            timestamp: 时间戳
            err_case: 错误测例名称
            log_content: 日志内容
        """
        self.failure_timestamp.append(timestamp)
        self.failure_err_case.append(err_case)
        self.failure_log_content.append(log_content)

    def save_success_result(self, timestamp, case_name, log_content):
        """保存成功测试用例运行结果

        Args:
            timestamp: 时间戳
            case_name: 成功测例名称
            log_content: 日志内容
        """
        self.success_timestamp.append(timestamp)
        self.success_case_name.append(case_name)
        self.success_log_content.append(log_content)

    def get_statistics(self):
        """获取测试结果统计信息"""
        total_count = len(self.failure_timestamp) + len(self.success_timestamp)
        success_count = len(self.success_timestamp)
        failure_count = len(self.failure_timestamp)
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        
        return {
            'total_count': total_count,
            'success_count': success_count,
            'failure_count': failure_count,
            'success_rate': success_rate
        }

    def parse_all_case_results(self):
        """
        解析所有已保存的测试用例运行结果，返回按测例分组的错误记录
        """
        grouped_error_records = {}
        
        # 处理失败的测试用例
        for idx, (timestamp, err_case, log_content) in enumerate(zip(self.failure_timestamp, self.failure_err_case, self.failure_log_content)):
            unique_key = f"failure_{timestamp}_{idx}"

            case_name = f"错误测例{err_case}"  # 添加"错误测例"前缀
            
            # 直接解析原始log_content（移除多余的分号拼接，避免分割错误）
            # 过滤空字符串 + 处理末尾分号
            log_parts = [part.strip() for part in log_content.split(';') if part.strip()]
            
            if len(log_parts) < 2:
                continue
            
            # 3. 解析表头和数据
            header_str = log_parts[0]
            error_info = [field.strip() for field in header_str.split(',')]
            field_count = len(error_info)
            data_rows = log_parts[1:]
            
            # 4. 初始化测例记录
            grouped_error_records[unique_key] = {
                'timestamp': timestamp,
                'case_name': case_name,
                'error_info': error_info,
                'error_records': []
            }
            
            # 5. 解析每一行数据
            for row_idx, data_str in enumerate(data_rows):
                data_values = [value.strip() for value in data_str.split(',')]
                
                # 校验字段数量
                if len(data_values) != field_count:
                    print(f"警告: 第{row_idx+1}行数据字段不匹配（期望{field_count}个，实际{len(data_values)}个）- {data_str}")
                    continue
                
                # 构建数据记录
                record = dict(zip(error_info, data_values))
                grouped_error_records[unique_key]['error_records'].append(record)
        
        # 处理成功的测试用例
        for idx, (timestamp, case_name, log_content) in enumerate(zip(self.success_timestamp, self.success_case_name, self.success_log_content)):
            unique_key = f"success_{timestamp}_{idx}"

            case_name_formatted = f"正确测例{case_name}"  # 添加"正确测例"前缀
            
            # 为成功记录创建简单的条目，格式为：时间、正确测例
            grouped_error_records[unique_key] = {
                'timestamp': timestamp,
                'case_name': case_name_formatted,
                'error_info': [],  # 成功记录不需要额外的状态和说明列
                'error_records': [{}]  # 空记录，因为不需要状态和说明
            }
        
        return grouped_error_records

    def export_csv(self, file_path):
        """
        导出所有错误记录到CSV文件
        """
        # 先写入统计信息
        stats = self.get_statistics()
        
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            
            # 写入统计信息行 - 按要求格式化
            writer.writerow(['总测例数', '成功个数', '失败个数', '成功率'])
            writer.writerow([stats['total_count'], stats['success_count'], stats['failure_count'], f"{stats['success_rate']:.2f}%"])
            writer.writerow([]) # 空行分隔
            
            # 获取详细结果
            grouped_error_records = self.parse_all_case_results()
            
            if not grouped_error_records:
                return
            
            # 将所有记录按时间戳排序
            sorted_records = sorted(grouped_error_records.items(), key=lambda x: x[1]['timestamp'])
            
            for _, case_data in sorted_records:
                # 根据记录前缀判断是成功还是失败案例
                is_success_case = case_data['case_name'].startswith('正确测例')
                
                if is_success_case:
                    # 如果不保留正确信息，直接跳过成功案例
                    continue

                    # 成功案例：只需要时间、正确测例两列
                    header_row = ['时间', '正确测例']
                    writer.writerow(header_row)
                    
                    # 数据行：时间戳 + 测例名（去掉"正确测例"前缀）
                    time_case_row = [case_data['timestamp'], case_data['case_name'][4:]]
                    writer.writerow(time_case_row)
                else:
                    # 失败案例：时间 + 错误测例 + 自定义字段
                    header_row = ['时间', '错误测例'] + case_data['error_info']
                    writer.writerow(header_row)
                    
                    # 第二行：时间戳 + 测例名（后续列空）
                    time_case_row = [case_data['timestamp'], case_data['case_name']] + [''] * len(case_data['error_info'])
                    writer.writerow(time_case_row)
                    
                    # 数据行：前两列空，填充数据
                    for record in case_data['error_records']:
                        data_row = ['', ''] # 前两列空
                        for field in case_data['error_info']:
                            value = record.get(field, '')

                            # 检查值是否为纯数字且长度较长，如果是则转换为文本格式
                            if self.format_as_text(value):
                                # 在值前添加制表符以确保Excel将其视为文本
                                formatted_value = '\t' + str(value)
                            else:
                                formatted_value = value
                            data_row.append(formatted_value)
                        writer.writerow(data_row)
                
                # 测例间分隔（空行）
                writer.writerow([])
                writer.writerow([])

    # def export_pdf(self, file_path):
    #     """
    #     导出所有错误记录到PDF文件
    #     """
    #     grouped_error_records = self.parse_all_case_results()
        
    #     if not grouped_error_records:
    #         return
        
    #     # 按时间戳对所有记录进行排序
    #     sorted_records = sorted(grouped_error_records.items(), key=lambda x: x[1]['timestamp'])
        
    #     # 创建PDF文档
    #     doc = canvas.Canvas(file_path, pagesize=landscape(A4))
    #     elements = []
    #     styles = getSampleStyleSheet()
        
    #     # 添加标题
    #     title_style = ParagraphStyle(
    #         'CustomTitle',
    #         parent=styles['Heading1'],
    #         fontSize=18,
    #         spaceAfter=30,
    #     )
    #     title = Paragraph("测试用例运行结果报告", title_style)
    #     elements.append(title)
        
    #     # 添加统计信息 - 按要求格式化
    #     stats = self.get_statistics()
    #     stats_text = f"总测例数: {stats['total_count']}<br/>成功个数: {stats['success_count']}<br/>失败个数: {stats['failure_count']}<br/>成功率: {stats['success_rate']:.2f}%"
    #     stats_para = Paragraph(stats_text, styles['Normal'])
    #     elements.append(stats_para)
    #     elements.append(Spacer(1, 12))
        
    #     for key, case_data in sorted_records:
    #         # 根据记录前缀判断是成功还是失败案例
    #         is_success_case = case_data['case_name'].startswith('正确测例')
            
    #         if is_success_case:
    #             # 成功案例：只显示时间和测例名
    #             case_title = Paragraph(f"时间: {case_data['timestamp']} | 正确测例: {case_data['case_name'][4:]}", styles['Heading2'])
    #             elements.append(case_title)
    #             elements.append(Spacer(1, 12))
    #         else:
    #             # 失败案例：正常显示
    #             if not case_data['error_records']:
    #                 continue
                
    #             # 添加测例标题
    #             case_title = Paragraph(f"时间: {case_data['timestamp']} | 测例状态: {case_data['case_name']}", styles['Heading2'])
    #             elements.append(case_title)
    #             elements.append(Spacer(1, 12))
                
    #             # 准备表格数据
    #             table_data = []
                
    #             # 表头
    #             header_row = ['序号'] + case_data['error_info']
    #             table_data.append(header_row)
                
    #             # 数据行
    #             for idx, record in enumerate(case_data['error_records'], 1):
    #                 data_row = [str(idx)] + [record.get(field, '') for field in case_data['error_info']]
    #                 table_data.append(data_row)
                
    #             # 创建表格
    #             table = Table(table_data)
    #             table.setStyle(TableStyle([
    #                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #                 ('FONTSIZE', (0, 0), (-1, 0), 10),
    #                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #                 ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #             ]))
                
    #             elements.append(table)
    #             elements.append(Spacer(1, 24))
        
    #     # 构建PDF
    #     for element in elements:
    #         if isinstance(element, Paragraph):
    #             element.wrapOn(doc, 0, 0)
    #             element.drawOn(doc, 30, 0)
    #             doc.showPage()
    #         elif isinstance(element, Spacer):
    #             # 简单跳过Spacer，或者我们可以在PDF中处理它
    #             pass
    #         else:  # 假设是Table或其他元素
    #             # 简单地移动到下一页
    #             doc.showPage()
        
    #     # 保存PDF
    #     doc.save()

    def format_as_text(self, value):
        """
        判断值是否应该格式化为文本格式
        """
        if not value:
            return False

        str_value = str(value)

        # 检查是否为纯数字
        if str_value.isdigit():
            # 如果数字长度大于10位，或者以0开头（除了单独的0），则格式化为文本
            return len(str_value) > 10 or (len(str_value) > 1 and str_value[0] == '0')

        # 检查是否为十六进制数（如FFFF格式）或包含字母E的格式（如68E9）
        if isinstance(value, str):
            # 如果包含字母E（可能是十六进制或类似68E9的格式），则格式化为文本
            if 'E' in str_value.upper():
                # 检查是否符合十六进制格式或类似68E9的格式（字母E前后都是十六进制字符）
                # 这种格式应该作为文本处理以避免被Excel解释为科学计数法
                return True
            # 检查是否为十六进制数（如FFFF格式）
            if all(c.upper() in '0123456789ABCDEF' for c in str_value):
                return len(str_value) > 4  # 如果十六进制数长度超过4位，也视为文本

        return False