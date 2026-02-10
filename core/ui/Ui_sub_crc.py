# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_crc.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSplitter, QWidget)

class Ui_SubForm_CRC(object):
    def setupUi(self, SubForm_CRC):
        if not SubForm_CRC.objectName():
            SubForm_CRC.setObjectName(u"SubForm_CRC")
        SubForm_CRC.resize(308, 329)
        self.horizontalLayout = QHBoxLayout(SubForm_CRC)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.check_box_crc_enable = QCheckBox(SubForm_CRC)
        self.check_box_crc_enable.setObjectName(u"check_box_crc_enable")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.check_box_crc_enable)

        self.splitter = QSplitter(SubForm_CRC)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.label_crc_range = QLabel(self.splitter)
        self.label_crc_range.setObjectName(u"label_crc_range")
        self.splitter.addWidget(self.label_crc_range)
        self.label_crc_type = QLabel(self.splitter)
        self.label_crc_type.setObjectName(u"label_crc_type")
        self.splitter.addWidget(self.label_crc_type)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.splitter)

        self.splitter_2 = QSplitter(SubForm_CRC)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.combo_box_crc_range = QComboBox(self.splitter_2)
        self.combo_box_crc_range.setObjectName(u"combo_box_crc_range")
        self.splitter_2.addWidget(self.combo_box_crc_range)
        self.combo_box_crc_type = QComboBox(self.splitter_2)
        self.combo_box_crc_type.setObjectName(u"combo_box_crc_type")
        self.splitter_2.addWidget(self.combo_box_crc_type)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.splitter_2)

        self.line = QFrame(SubForm_CRC)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.line)

        self.splitter_3 = QSplitter(SubForm_CRC)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Vertical)
        self.label_crc_width = QLabel(self.splitter_3)
        self.label_crc_width.setObjectName(u"label_crc_width")
        self.splitter_3.addWidget(self.label_crc_width)
        self.label_crc_poly = QLabel(self.splitter_3)
        self.label_crc_poly.setObjectName(u"label_crc_poly")
        self.splitter_3.addWidget(self.label_crc_poly)
        self.label_crc_formula = QLabel(self.splitter_3)
        self.label_crc_formula.setObjectName(u"label_crc_formula")
        self.splitter_3.addWidget(self.label_crc_formula)
        self.label_crc_init = QLabel(self.splitter_3)
        self.label_crc_init.setObjectName(u"label_crc_init")
        self.splitter_3.addWidget(self.label_crc_init)
        self.label_crc_xorout = QLabel(self.splitter_3)
        self.label_crc_xorout.setObjectName(u"label_crc_xorout")
        self.splitter_3.addWidget(self.label_crc_xorout)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.splitter_3)

        self.splitter_4 = QSplitter(SubForm_CRC)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Orientation.Vertical)
        self.combo_box_crc_width = QComboBox(self.splitter_4)
        self.combo_box_crc_width.setObjectName(u"combo_box_crc_width")
        self.splitter_4.addWidget(self.combo_box_crc_width)
        self.line_edit_crc_poly = QLineEdit(self.splitter_4)
        self.line_edit_crc_poly.setObjectName(u"line_edit_crc_poly")
        self.splitter_4.addWidget(self.line_edit_crc_poly)
        self.line_edit_crc_formula = QLineEdit(self.splitter_4)
        self.line_edit_crc_formula.setObjectName(u"line_edit_crc_formula")
        self.splitter_4.addWidget(self.line_edit_crc_formula)
        self.line_edit_crc_init = QLineEdit(self.splitter_4)
        self.line_edit_crc_init.setObjectName(u"line_edit_crc_init")
        self.splitter_4.addWidget(self.line_edit_crc_init)
        self.line_edit_crc_xorout = QLineEdit(self.splitter_4)
        self.line_edit_crc_xorout.setObjectName(u"line_edit_crc_xorout")
        self.splitter_4.addWidget(self.line_edit_crc_xorout)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.splitter_4)

        self.check_box_in_reversal = QCheckBox(SubForm_CRC)
        self.check_box_in_reversal.setObjectName(u"check_box_in_reversal")
        self.check_box_in_reversal.setCheckable(True)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.check_box_in_reversal)

        self.check_box_out_reversal = QCheckBox(SubForm_CRC)
        self.check_box_out_reversal.setObjectName(u"check_box_out_reversal")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.check_box_out_reversal)

        self.line_2 = QFrame(SubForm_CRC)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.line_2)

        self.splitter_5 = QSplitter(SubForm_CRC)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Orientation.Horizontal)
        self.button_crc_confirm = QPushButton(self.splitter_5)
        self.button_crc_confirm.setObjectName(u"button_crc_confirm")
        self.splitter_5.addWidget(self.button_crc_confirm)
        self.button_crc_cancel = QPushButton(self.splitter_5)
        self.button_crc_cancel.setObjectName(u"button_crc_cancel")
        self.splitter_5.addWidget(self.button_crc_cancel)

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.splitter_5)

        self.check_box_high_first = QCheckBox(SubForm_CRC)
        self.check_box_high_first.setObjectName(u"check_box_high_first")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.check_box_high_first)

        self.label_byte_order = QLabel(SubForm_CRC)
        self.label_byte_order.setObjectName(u"label_byte_order")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_byte_order)


        self.horizontalLayout.addLayout(self.formLayout)


        self.retranslateUi(SubForm_CRC)

        QMetaObject.connectSlotsByName(SubForm_CRC)
    # setupUi

    def retranslateUi(self, SubForm_CRC):
        SubForm_CRC.setWindowTitle(QCoreApplication.translate("SubForm_CRC", u"CRC\u6821\u9a8c\u8bbe\u7f6e", None))
        self.check_box_crc_enable.setText(QCoreApplication.translate("SubForm_CRC", u"\u6821\u9a8c\u4f7f\u80fd", None))
        self.label_crc_range.setText(QCoreApplication.translate("SubForm_CRC", u"\u68c0\u9a8c\u533a\u95f4", None))
        self.label_crc_type.setText(QCoreApplication.translate("SubForm_CRC", u"\u6821\u9a8c\u7c7b\u578b", None))
        self.label_crc_width.setText(QCoreApplication.translate("SubForm_CRC", u"\u5bbd\u5ea6(WIDTH)", None))
        self.label_crc_poly.setText(QCoreApplication.translate("SubForm_CRC", u"\u591a\u9879\u5f0f(POLY)", None))
        self.label_crc_formula.setText(QCoreApplication.translate("SubForm_CRC", u"\u591a\u9879\u5f0f\u516c\u5f0f", None))
        self.label_crc_init.setText(QCoreApplication.translate("SubForm_CRC", u"\u521d\u59cb\u503c(INIT)", None))
        self.label_crc_xorout.setText(QCoreApplication.translate("SubForm_CRC", u"\u7ed3\u679c\u5f02\u6216\u503c(XOROUT)", None))
        self.line_edit_crc_poly.setText("")
        self.line_edit_crc_formula.setText("")
        self.line_edit_crc_init.setText("")
        self.line_edit_crc_xorout.setText("")
        self.check_box_in_reversal.setText(QCoreApplication.translate("SubForm_CRC", u"\u8f93\u5165\u53cd\u8f6c", None))
        self.check_box_out_reversal.setText(QCoreApplication.translate("SubForm_CRC", u"\u8f93\u51fa\u53cd\u8f6c", None))
        self.button_crc_confirm.setText(QCoreApplication.translate("SubForm_CRC", u"\u786e\u8ba4", None))
        self.button_crc_cancel.setText(QCoreApplication.translate("SubForm_CRC", u"\u53d6\u6d88", None))
        self.check_box_high_first.setText(QCoreApplication.translate("SubForm_CRC", u"\u9ad8\u5b57\u8282\u5728\u524d", None))
        self.label_byte_order.setText(QCoreApplication.translate("SubForm_CRC", u"\u5b57\u8282\u987a\u5e8f", None))
    # retranslateUi

