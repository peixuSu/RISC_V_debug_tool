#!/usr/bin/env python3
"""
SPI项目构建脚本
使用PyInstaller将项目打包为exe可执行文件
"""

import os
import sys
from pathlib import Path

def build():
    """使用PyInstaller构建可执行文件"""
    try:
        # 导入PyInstaller
        import PyInstaller.__main__
        
        # 获取项目根目录
        project_root = Path(__file__).parent.absolute()
        os.chdir(project_root)
        
        # PyInstaller参数
        args = [
            '--name=SPI_Tool',           # 可执行文件名称
            '--windowed',                # 无控制台窗口模式
            '--onefile',                 # 打包为单个文件
            '--clean',                   # 清理临时文件
            '--noconfirm',               # 不提示确认覆盖
            '--distpath=dist',           # 输出目录
            '--workpath=build',          # 构建目录
            '--specpath=.',              # spec文件目录
            '--add-data=core;core',      # 添加core模块
            '--add-data=spi;spi',        # 添加spi模块
            '--add-data=utils;utils',    # 添加utils模块
            '--add-data=spi/jtool.dll;.', # 添加DLL文件到根目录
            '--hidden-import=PySide6',
            '--hidden-import=PySide6.QtCore',
            '--hidden-import=PySide6.QtGui',
            '--hidden-import=PySide6.QtWidgets',
            '--hidden-import=PySide6.QtUiTools',
            '--hidden-import=yaml',
            '--hidden-import=reportlab',
            'main.py'                    # 主程序入口
        ]
        
        print("开始构建...")
        print(f"工作目录: {project_root}")
        print(f"执行命令: pyinstaller {' '.join(args)}")
        
        # 调用PyInstaller
        PyInstaller.__main__.run(args)
        
        print("\n构建完成!")
        print("可执行文件位置: dist/SPI_Tool.exe")
        
    except ImportError:
        print("错误: 未找到PyInstaller库")
        print("请先安装: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"构建过程中出现错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build()