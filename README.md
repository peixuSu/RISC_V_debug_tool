# 文件夹框架

```
├── main.py                   # 应用程序入口
├── requirements.txt          # 依赖包声明
├── build.py                  # 构建.exe的脚本
├── doc/
│   ├── Qt界面使用手册.md            
│   ├── Qt界面使用手册.assets   # 存放图片文件夹
│   ├── Qt界面软件文档.md            
│   ├── Qt界面软件文档.assets   # 存放图片文件夹
│
├── core/                     # 核心功能模块
│   ├── applicaton.py         # 主应用窗口控制器
│   ├── ui/                   # UI界面文件
│   │   ├── Ui_application.py # 主界面UI类
│   │   ├── Ui_sub_crc.py     # CRC配置界面UI类
│   │   ├── application.ui    # 主界面设计文件
│   │   └── sub_crc.ui        # CRC配置界面设计文件
│   ├── risc_v_debug/         # RISC-V调试核心功能
│   │   ├── risc_v_window.py  # RISC-V主窗口控制器
│   │   ├── risc_v_case.py    # 测试用例执行管理
│   │   ├── send_controller.py # 发送控制器
│   │   ├── scan_device.py    # 设备扫描功能
│   │   ├── case_manager.py   # 测试用例管理
│   │   └── frame.py          # 通信协议帧定义
│   ├── log/                  # 日志管理模块
│   │   ├── log_window.py     # 日志窗口
│   │   └── log_manager.py    # 日志解析和报告生成
│   └── sub_window/           # 子窗口模块
│       ├── sub_window.py     # 子窗口基类
│       └── sub_crc.py        # CRC配置子窗口
├── spi/                      # SPI通信模块
│   ├── spi_window.py         # SPI窗口管理
│   ├── spi_controller.py     # SPI控制器
│   ├── spi_driver.py         # SPI底层驱动接口
│   └── jtool.dll             # SPI硬件驱动库
└── utils/                    # 工具模块
    └── crc/                  # CRC校验工具
        ├── crc_manager.py    # CRC计算管理
        └── crc_window.py     # CRC窗口界面
```
