# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chat_menu_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_ChatMenu(object):
    def setupUi(self, ChatMenu):
        if not ChatMenu.objectName():
            ChatMenu.setObjectName(u"ChatMenu")
        ChatMenu.resize(94, 70)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ChatMenu.sizePolicy().hasHeightForWidth())
        ChatMenu.setSizePolicy(sizePolicy)
        ChatMenu.setMaximumSize(QSize(94, 70))
        ChatMenu.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: rgb(41, 58, 76)}\n"
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
        self.verticalLayout = QVBoxLayout(ChatMenu)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 4, 8, 4)
        self.pushButton = QPushButton(ChatMenu)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 23))

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(ChatMenu)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.pushButton_2)


        self.retranslateUi(ChatMenu)

        QMetaObject.connectSlotsByName(ChatMenu)
    # setupUi

    def retranslateUi(self, ChatMenu):
        ChatMenu.setWindowTitle(QCoreApplication.translate("ChatMenu", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("ChatMenu", u"Delete Chat", None))
        self.pushButton_2.setText(QCoreApplication.translate("ChatMenu", u"Clear History", None))
    # retranslateUi

