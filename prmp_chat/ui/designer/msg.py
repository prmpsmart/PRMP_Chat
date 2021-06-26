# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'msg.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Msg(object):
    def setupUi(self, Msg):
        if not Msg.objectName():
            Msg.setObjectName(u"Msg")
        Msg.resize(252, 119)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Msg.sizePolicy().hasHeightForWidth())
        Msg.setSizePolicy(sizePolicy)
        Msg.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: white}\n"
"\n"
" QPushButton{\n"
"	border: 1px solid;\n"
"	border-radius: 4px ;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));\n"
"	color: rgb(234, 183, 78)\n"
"}\n"
"\n"
" QPushButton:pressed {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 0 rgb(170, 132, 57), stop: 1 rgb(234, 183, 78));\n"
"	color:  rgb(20, 36, 43)\n"
"  }\n"
"\n"
"")
        self.verticalLayout = QVBoxLayout(Msg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Msg)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cancelButton = QPushButton(Msg)
        self.cancelButton.setObjectName(u"cancelButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy1)
        self.cancelButton.setMinimumSize(QSize(50, 40))
        self.cancelButton.setMaximumSize(QSize(50, 40))
        self.cancelButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelButton.setStyleSheet(u"n")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Msg)

        QMetaObject.connectSlotsByName(Msg)
    # setupUi

    def retranslateUi(self, Msg):
        Msg.setWindowTitle(QCoreApplication.translate("Msg", u"Form", None))
        self.label.setText(QCoreApplication.translate("Msg", u"TextLabel", None))
        self.cancelButton.setText(QCoreApplication.translate("Msg", u"Cancel", None))
    # retranslateUi

