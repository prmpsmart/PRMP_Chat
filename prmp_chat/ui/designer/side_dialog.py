# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'side_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_SideDialog(object):
    def setupUi(self, SideDialog):
        if not SideDialog.objectName():
            SideDialog.setObjectName(u"SideDialog")
        SideDialog.resize(260, 384)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SideDialog.sizePolicy().hasHeightForWidth())
        SideDialog.setSizePolicy(sizePolicy)
        SideDialog.setMinimumSize(QSize(200, 0))
        SideDialog.setMaximumSize(QSize(260, 384))
        SideDialog.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: white}\n"
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
        self.verticalLayout_2 = QVBoxLayout(SideDialog)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(SideDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(260, 100))
        self.frame.setMaximumSize(QSize(16777215, 100))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(1)
        self.pushButton_5 = QPushButton(self.frame)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(210, 10, 40, 30))
        self.pushButton_5.setStyleSheet(u"")
        self.pushButton_5.setFlat(True)
        self.pushButton_6 = QPushButton(self.frame)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(10, 10, 80, 80))
        self.pushButton_6.setStyleSheet(u"\n"
" QPushButton{\n"
"	border: 1px solid;\n"
"	border-radius: 40px ;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 0 rgb(170, 132, 57), stop: 1 rgb(234, 183, 78));\n"
"	color:  rgb(20, 36, 43)\n"
"}\n"
"\n"
"\n"
" QPushButton:pressed {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));\n"
"	color: rgb(234, 183, 78)\n"
"  }\n"
"\n"
"\n"
"")
        self.pushButton_6.setAutoDefault(False)
        self.pushButton_6.setFlat(False)

        self.verticalLayout_2.addWidget(self.frame)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 4, 20, 4)
        self.newContactButton = QPushButton(SideDialog)
        self.newContactButton.setObjectName(u"newContactButton")
        self.newContactButton.setMinimumSize(QSize(0, 40))
        self.newContactButton.setLayoutDirection(Qt.LeftToRight)
        self.newContactButton.setFlat(True)

        self.verticalLayout.addWidget(self.newContactButton)

        self.newGroupButton = QPushButton(SideDialog)
        self.newGroupButton.setObjectName(u"newGroupButton")
        self.newGroupButton.setMinimumSize(QSize(0, 40))
        self.newGroupButton.setFlat(True)

        self.verticalLayout.addWidget(self.newGroupButton)

        self.newChannelButton = QPushButton(SideDialog)
        self.newChannelButton.setObjectName(u"newChannelButton")
        self.newChannelButton.setMinimumSize(QSize(0, 40))
        self.newChannelButton.setFlat(True)

        self.verticalLayout.addWidget(self.newChannelButton)

        self.settingsButton = QPushButton(SideDialog)
        self.settingsButton.setObjectName(u"settingsButton")
        self.settingsButton.setMinimumSize(QSize(0, 40))
        self.settingsButton.setStyleSheet(u"")
        self.settingsButton.setFlat(True)

        self.verticalLayout.addWidget(self.settingsButton)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.textBrowser = QTextBrowser(SideDialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMaximumSize(QSize(16777215, 80))
        self.textBrowser.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.textBrowser)


        self.retranslateUi(SideDialog)

        self.pushButton_5.setDefault(True)
        self.pushButton_6.setDefault(True)
        self.newContactButton.setDefault(False)
        self.newGroupButton.setDefault(False)
        self.newChannelButton.setDefault(False)
        self.settingsButton.setDefault(False)


        QMetaObject.connectSlotsByName(SideDialog)
    # setupUi

    def retranslateUi(self, SideDialog):
        SideDialog.setWindowTitle(QCoreApplication.translate("SideDialog", u"Dialog", None))
        self.pushButton_5.setText(QCoreApplication.translate("SideDialog", u"Edit", None))
        self.pushButton_6.setText(QCoreApplication.translate("SideDialog", u"Image", None))
        self.newContactButton.setText(QCoreApplication.translate("SideDialog", u"New Contact", None))
        self.newGroupButton.setText(QCoreApplication.translate("SideDialog", u"New Group", None))
        self.newChannelButton.setText(QCoreApplication.translate("SideDialog", u"New Channel", None))
        self.settingsButton.setText(QCoreApplication.translate("SideDialog", u"Settings", None))
    # retranslateUi

