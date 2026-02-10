# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'application.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Application(object):
    def setupUi(self, Application):
        if not Application.objectName():
            Application.setObjectName(u"Application")
        Application.resize(734, 613)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Application.sizePolicy().hasHeightForWidth())
        Application.setSizePolicy(sizePolicy)
        Application.setMinimumSize(QSize(0, 0))
        Application.setMaximumSize(QSize(2000, 1000))
        self.gridLayout_2 = QGridLayout(Application)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.button_fold_config = QPushButton(Application)
        self.button_fold_config.setObjectName(u"button_fold_config")

        self.horizontalLayout_13.addWidget(self.button_fold_config)

        self.pushButton_crc_fonfig = QPushButton(Application)
        self.pushButton_crc_fonfig.setObjectName(u"pushButton_crc_fonfig")

        self.horizontalLayout_13.addWidget(self.pushButton_crc_fonfig)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_2)

        self.check_box_test = QCheckBox(Application)
        self.check_box_test.setObjectName(u"check_box_test")

        self.horizontalLayout_13.addWidget(self.check_box_test)


        self.gridLayout_2.addLayout(self.horizontalLayout_13, 0, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.spi_config_widget = QWidget(Application)
        self.spi_config_widget.setObjectName(u"spi_config_widget")
        self.spi_config_widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_12 = QHBoxLayout(self.spi_config_widget)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_decive = QLabel(self.spi_config_widget)
        self.label_decive.setObjectName(u"label_decive")
        self.label_decive.setMinimumSize(QSize(0, 0))
        self.label_decive.setMaximumSize(QSize(35, 25))
        font = QFont()
        font.setPointSize(9)
        self.label_decive.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_decive)

        self.line_device = QLineEdit(self.spi_config_widget)
        self.line_device.setObjectName(u"line_device")
        self.line_device.setMinimumSize(QSize(0, 0))
        self.line_device.setMaximumSize(QSize(100, 25))
        self.line_device.setFont(font)
        self.line_device.setReadOnly(True)

        self.horizontalLayout_12.addWidget(self.line_device)

        self.button_refresh = QPushButton(self.spi_config_widget)
        self.button_refresh.setObjectName(u"button_refresh")
        self.button_refresh.setMaximumSize(QSize(25, 16777215))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaylistRepeat))
        self.button_refresh.setIcon(icon)
        self.button_refresh.setIconSize(QSize(13, 13))

        self.horizontalLayout_12.addWidget(self.button_refresh)

        self.label_vcc = QLabel(self.spi_config_widget)
        self.label_vcc.setObjectName(u"label_vcc")
        self.label_vcc.setMinimumSize(QSize(0, 0))
        self.label_vcc.setMaximumSize(QSize(50, 25))
        self.label_vcc.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_vcc)

        self.combo_box_vcc = QComboBox(self.spi_config_widget)
        self.combo_box_vcc.setObjectName(u"combo_box_vcc")
        self.combo_box_vcc.setMinimumSize(QSize(0, 0))
        self.combo_box_vcc.setMaximumSize(QSize(50, 16777215))
        self.combo_box_vcc.setFont(font)

        self.horizontalLayout_12.addWidget(self.combo_box_vcc)

        self.label_io = QLabel(self.spi_config_widget)
        self.label_io.setObjectName(u"label_io")
        self.label_io.setMinimumSize(QSize(0, 0))
        self.label_io.setMaximumSize(QSize(40, 25))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_io.setFont(font1)

        self.horizontalLayout_12.addWidget(self.label_io)

        self.combo_box_io = QComboBox(self.spi_config_widget)
        self.combo_box_io.setObjectName(u"combo_box_io")
        self.combo_box_io.setMinimumSize(QSize(0, 0))
        self.combo_box_io.setMaximumSize(QSize(60, 16777215))
        self.combo_box_io.setFont(font)

        self.horizontalLayout_12.addWidget(self.combo_box_io)

        self.label_speed = QLabel(self.spi_config_widget)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setMinimumSize(QSize(0, 0))
        self.label_speed.setMaximumSize(QSize(50, 25))
        self.label_speed.setFont(font1)

        self.horizontalLayout_12.addWidget(self.label_speed)

        self.combo_box_speed = QComboBox(self.spi_config_widget)
        self.combo_box_speed.setObjectName(u"combo_box_speed")
        self.combo_box_speed.setMinimumSize(QSize(0, 0))
        self.combo_box_speed.setMaximumSize(QSize(85, 16777215))
        self.combo_box_speed.setFont(font)

        self.horizontalLayout_12.addWidget(self.combo_box_speed)

        self.label_clk = QLabel(self.spi_config_widget)
        self.label_clk.setObjectName(u"label_clk")
        self.label_clk.setMinimumSize(QSize(0, 0))
        self.label_clk.setMaximumSize(QSize(30, 25))
        self.label_clk.setFont(font1)

        self.horizontalLayout_12.addWidget(self.label_clk)

        self.combo_box_clk = QComboBox(self.spi_config_widget)
        self.combo_box_clk.setObjectName(u"combo_box_clk")
        self.combo_box_clk.setMinimumSize(QSize(0, 0))
        self.combo_box_clk.setMaximumSize(QSize(100, 16777215))
        self.combo_box_clk.setFont(font)

        self.horizontalLayout_12.addWidget(self.combo_box_clk)

        self.label_bit = QLabel(self.spi_config_widget)
        self.label_bit.setObjectName(u"label_bit")
        self.label_bit.setMinimumSize(QSize(0, 0))
        self.label_bit.setMaximumSize(QSize(40, 25))
        self.label_bit.setFont(font1)

        self.horizontalLayout_12.addWidget(self.label_bit)

        self.combo_box_bit = QComboBox(self.spi_config_widget)
        self.combo_box_bit.setObjectName(u"combo_box_bit")
        self.combo_box_bit.setMinimumSize(QSize(0, 0))
        self.combo_box_bit.setMaximumSize(QSize(60, 16777215))
        self.combo_box_bit.setFont(font)

        self.horizontalLayout_12.addWidget(self.combo_box_bit)

        self.label_s_or_q = QLabel(self.spi_config_widget)
        self.label_s_or_q.setObjectName(u"label_s_or_q")
        self.label_s_or_q.setMinimumSize(QSize(0, 0))
        self.label_s_or_q.setMaximumSize(QSize(40, 25))
        self.label_s_or_q.setFont(font1)

        self.horizontalLayout_12.addWidget(self.label_s_or_q)

        self.combo_box_s_or_q = QComboBox(self.spi_config_widget)
        self.combo_box_s_or_q.setObjectName(u"combo_box_s_or_q")
        self.combo_box_s_or_q.setMinimumSize(QSize(0, 0))
        self.combo_box_s_or_q.setMaximumSize(QSize(100, 16777215))
        self.combo_box_s_or_q.setFont(font)

        self.horizontalLayout_12.addWidget(self.combo_box_s_or_q)


        self.horizontalLayout_8.addWidget(self.spi_config_widget)


        self.gridLayout_2.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.log_widget = QWidget(Application)
        self.log_widget.setObjectName(u"log_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.log_widget.sizePolicy().hasHeightForWidth())
        self.log_widget.setSizePolicy(sizePolicy1)
        self.log_widget.setMinimumSize(QSize(0, 0))
        self.log_widget.setMaximumSize(QSize(16777215, 150))
        self.gridLayout_3 = QGridLayout(self.log_widget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.button_clear = QPushButton(self.log_widget)
        self.button_clear.setObjectName(u"button_clear")
        self.button_clear.setMinimumSize(QSize(80, 25))
        self.button_clear.setMaximumSize(QSize(50, 25))
        font2 = QFont()
        font2.setFamilies([u"\u5b8b\u4f53"])
        font2.setPointSize(10)
        self.button_clear.setFont(font2)

        self.gridLayout_3.addWidget(self.button_clear, 2, 1, 1, 1)

        self.text_log = QPlainTextEdit(self.log_widget)
        self.text_log.setObjectName(u"text_log")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.text_log.sizePolicy().hasHeightForWidth())
        self.text_log.setSizePolicy(sizePolicy2)
        self.text_log.setMinimumSize(QSize(0, 0))
        self.text_log.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamilies([u"\u5b8b\u4f53"])
        font3.setPointSize(12)
        self.text_log.setFont(font3)
        self.text_log.setFrameShadow(QFrame.Shadow.Raised)
        self.text_log.setReadOnly(True)

        self.gridLayout_3.addWidget(self.text_log, 0, 0, 1, 3)

        self.button_save = QPushButton(self.log_widget)
        self.button_save.setObjectName(u"button_save")
        self.button_save.setMinimumSize(QSize(80, 25))
        self.button_save.setMaximumSize(QSize(50, 25))
        self.button_save.setFont(font2)

        self.gridLayout_3.addWidget(self.button_save, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.log_widget, 1, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_3, 2, 1, 1, 1)

        self.comboBox_mode_select = QComboBox(Application)
        self.comboBox_mode_select.addItem("")
        self.comboBox_mode_select.addItem("")
        self.comboBox_mode_select.setObjectName(u"comboBox_mode_select")

        self.gridLayout_9.addWidget(self.comboBox_mode_select, 0, 0, 1, 1)

        self.MCU_button_stop = QPushButton(Application)
        self.MCU_button_stop.setObjectName(u"MCU_button_stop")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.MCU_button_stop.sizePolicy().hasHeightForWidth())
        self.MCU_button_stop.setSizePolicy(sizePolicy3)
        self.MCU_button_stop.setMinimumSize(QSize(0, 40))

        self.gridLayout_9.addWidget(self.MCU_button_stop, 4, 1, 1, 3)

        self.lineEdit_round_input = QLineEdit(Application)
        self.lineEdit_round_input.setObjectName(u"lineEdit_round_input")

        self.gridLayout_9.addWidget(self.lineEdit_round_input, 2, 0, 1, 1)

        self.MCU_button_send = QPushButton(Application)
        self.MCU_button_send.setObjectName(u"MCU_button_send")
        sizePolicy3.setHeightForWidth(self.MCU_button_send.sizePolicy().hasHeightForWidth())
        self.MCU_button_send.setSizePolicy(sizePolicy3)
        self.MCU_button_send.setMinimumSize(QSize(0, 40))

        self.gridLayout_9.addWidget(self.MCU_button_send, 4, 0, 1, 1)

        self.MCU_list_test = QListWidget(Application)
        self.MCU_list_test.setObjectName(u"MCU_list_test")
        self.MCU_list_test.setMinimumSize(QSize(0, 0))
        self.MCU_list_test.setMaximumSize(QSize(16777215, 16777215))
        self.MCU_list_test.setResizeMode(QListView.ResizeMode.Fixed)

        self.gridLayout_9.addWidget(self.MCU_list_test, 3, 0, 1, 4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 0, 1, 1, 3)

        self.checkBox_endless = QCheckBox(Application)
        self.checkBox_endless.setObjectName(u"checkBox_endless")

        self.gridLayout_9.addWidget(self.checkBox_endless, 2, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_9, 0, 0, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_mcu_connect = QPushButton(Application)
        self.button_mcu_connect.setObjectName(u"button_mcu_connect")
        self.button_mcu_connect.setMaximumSize(QSize(76, 24))

        self.horizontalLayout_3.addWidget(self.button_mcu_connect)

        self.button_mcu_scan = QPushButton(Application)
        self.button_mcu_scan.setObjectName(u"button_mcu_scan")
        self.button_mcu_scan.setMaximumSize(QSize(79, 24))

        self.horizontalLayout_3.addWidget(self.button_mcu_scan)

        self.button_mcu_export_pdf = QPushButton(Application)
        self.button_mcu_export_pdf.setObjectName(u"button_mcu_export_pdf")

        self.horizontalLayout_3.addWidget(self.button_mcu_export_pdf)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.MCU_list_case = QListWidget(Application)
        self.MCU_list_case.setObjectName(u"MCU_list_case")
        self.MCU_list_case.setMinimumSize(QSize(0, 0))

        self.verticalLayout_7.addWidget(self.MCU_list_case)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(2)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.MCU_line_test = QLineEdit(Application)
        self.MCU_line_test.setObjectName(u"MCU_line_test")
        self.MCU_line_test.setMinimumSize(QSize(0, 30))
        font4 = QFont()
        font4.setPointSize(14)
        self.MCU_line_test.setFont(font4)

        self.horizontalLayout_14.addWidget(self.MCU_line_test)

        self.MCU_button_test = QPushButton(Application)
        self.MCU_button_test.setObjectName(u"MCU_button_test")
        self.MCU_button_test.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_14.addWidget(self.MCU_button_test)

        self.button_receive = QPushButton(Application)
        self.button_receive.setObjectName(u"button_receive")
        self.button_receive.setMinimumSize(QSize(0, 30))
        self.button_receive.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_14.addWidget(self.button_receive)

        self.label_receive_size = QLabel(Application)
        self.label_receive_size.setObjectName(u"label_receive_size")
        self.label_receive_size.setMinimumSize(QSize(0, 30))
        self.label_receive_size.setMaximumSize(QSize(16777215, 16777215))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_receive_size.setFont(font5)

        self.horizontalLayout_14.addWidget(self.label_receive_size)

        self.combo_box_size = QComboBox(Application)
        self.combo_box_size.setObjectName(u"combo_box_size")
        self.combo_box_size.setMinimumSize(QSize(0, 30))
        self.combo_box_size.setMaximumSize(QSize(16777215, 30))
        self.combo_box_size.setFont(font1)

        self.horizontalLayout_14.addWidget(self.combo_box_size)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)


        self.gridLayout_5.addLayout(self.verticalLayout_7, 0, 1, 1, 1)

        self.gridLayout_5.setColumnStretch(1, 1)

        self.gridLayout.addLayout(self.gridLayout_5, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)


        self.retranslateUi(Application)

        QMetaObject.connectSlotsByName(Application)
    # setupUi

    def retranslateUi(self, Application):
        Application.setWindowTitle(QCoreApplication.translate("Application", u"SPI\u4e0a\u4f4d\u673a", None))
#if QT_CONFIG(tooltip)
        Application.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.button_fold_config.setText(QCoreApplication.translate("Application", u"spi\u914d\u7f6e", None))
        self.pushButton_crc_fonfig.setText(QCoreApplication.translate("Application", u"CRC\u914d\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.check_box_test.setToolTip(QCoreApplication.translate("Application", u"\u52fe\u9009\u4e0a\u6b64\u52fe\u9009\u6846\uff0c\u8fde\u63a5\u8bbe\u5907\u53d1\u9001\u548c\u63a5\u6536\u7aef\uff0c\u53ef\u81ea\u6d4b\u8bbe\u5907\u662f\u5426\u6b63\u5e38\u5de5\u4f5c", None))
#endif // QT_CONFIG(tooltip)
        self.check_box_test.setText(QCoreApplication.translate("Application", u"\u6536\u53d1\u81ea\u6d4b", None))
        self.label_decive.setText(QCoreApplication.translate("Application", u"\u8bbe\u5907", None))
        self.button_refresh.setText("")
        self.label_vcc.setText(QCoreApplication.translate("Application", u"VCC\u7535\u538b", None))
        self.label_io.setText(QCoreApplication.translate("Application", u"IO\u7535\u5e73", None))
        self.label_speed.setText(QCoreApplication.translate("Application", u"SPI\u901f\u7387", None))
        self.label_clk.setText(QCoreApplication.translate("Application", u"\u65f6\u949f", None))
        self.label_bit.setText(QCoreApplication.translate("Application", u"\u4f4d\u987a\u5e8f", None))
        self.label_s_or_q.setText(QCoreApplication.translate("Application", u"S/QSPI", None))
#if QT_CONFIG(tooltip)
        self.button_clear.setToolTip(QCoreApplication.translate("Application", u"\u6e05\u9664", None))
#endif // QT_CONFIG(tooltip)
        self.button_clear.setText(QCoreApplication.translate("Application", u"\u6e05\u9664", None))
        self.text_log.setPlainText("")
#if QT_CONFIG(tooltip)
        self.button_save.setToolTip(QCoreApplication.translate("Application", u"\u4fdd\u5b58", None))
#endif // QT_CONFIG(tooltip)
        self.button_save.setText(QCoreApplication.translate("Application", u"\u4fdd\u5b58", None))
        self.comboBox_mode_select.setItemText(0, QCoreApplication.translate("Application", u"\u5faa\u73af\u53d1\u9001", None))
        self.comboBox_mode_select.setItemText(1, QCoreApplication.translate("Application", u"\u968f\u673a\u53d1\u9001", None))

        self.MCU_button_stop.setText(QCoreApplication.translate("Application", u"\u7ec8\u6b62", None))
        self.lineEdit_round_input.setText(QCoreApplication.translate("Application", u"1", None))
        self.lineEdit_round_input.setPlaceholderText(QCoreApplication.translate("Application", u"\u6b21\u6570", None))
        self.MCU_button_send.setText(QCoreApplication.translate("Application", u"\u5f00\u59cb", None))
        self.checkBox_endless.setText(QCoreApplication.translate("Application", u"\u65e0\u9650\u53d1\u9001", None))
        self.button_mcu_connect.setText(QCoreApplication.translate("Application", u"\u8fde\u63a5", None))
        self.button_mcu_scan.setText(QCoreApplication.translate("Application", u"\u626b\u63cf", None))
        self.button_mcu_export_pdf.setText(QCoreApplication.translate("Application", u"\u5bfc\u51fa\u6d4b\u8bd5\u62a5\u544a", None))
        self.MCU_button_test.setText(QCoreApplication.translate("Application", u"\u53d1\u9001", None))
        self.button_receive.setText(QCoreApplication.translate("Application", u"\u53ea\u8bfb", None))
        self.label_receive_size.setText(QCoreApplication.translate("Application", u"\u8bfb\u6570\u636e\u957f\u5ea6", None))
    # retranslateUi

