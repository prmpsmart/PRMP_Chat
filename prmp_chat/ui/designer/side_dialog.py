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
        SideDialog.resize(303, 334)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SideDialog.sizePolicy().hasHeightForWidth())
        SideDialog.setSizePolicy(sizePolicy)
        SideDialog.setMinimumSize(QSize(200, 0))
        SideDialog.setMaximumSize(QSize(350, 384))
        SideDialog.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: rgb(234, 183, 78)}\n"
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
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(SideDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(260, 130))
        self.frame.setMaximumSize(QSize(16777215, 150))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(0)
        self.editButton = QPushButton(self.frame)
        self.editButton.setObjectName(u"editButton")
        self.editButton.setGeometry(QRect(240, 90, 40, 30))
        self.editButton.setStyleSheet(u"")
        self.editButton.setFlat(True)
        self.iconButton = QPushButton(self.frame)
        self.iconButton.setObjectName(u"iconButton")
        self.iconButton.setGeometry(QRect(10, 10, 80, 80))
        self.iconButton.setStyleSheet(u"\n"
" QPushButton{\n"
"	border: 1px solid;\n"
"	border-radius: 8px ;\n"
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
        self.iconButton.setAutoDefault(False)
        self.iconButton.setFlat(False)
        self.lastLoginLabel = QLabel(self.frame)
        self.lastLoginLabel.setObjectName(u"lastLoginLabel")
        self.lastLoginLabel.setGeometry(QRect(100, 60, 181, 21))
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        self.lastLoginLabel.setFont(font)
        self.lastLoginLabel.setStyleSheet(u"color: #34aa1f")
        self.nameLabel = QLabel(self.frame)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setGeometry(QRect(100, 10, 171, 31))
        font1 = QFont()
        font1.setFamily(u"Times New Roman")
        font1.setPointSize(14)
        font1.setUnderline(True)
        self.nameLabel.setFont(font1)
        self.lastLoginLabel_2 = QLabel(self.frame)
        self.lastLoginLabel_2.setObjectName(u"lastLoginLabel_2")
        self.lastLoginLabel_2.setGeometry(QRect(100, 40, 141, 21))
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        font2.setPointSize(11)
        font2.setBold(True)
        self.lastLoginLabel_2.setFont(font2)

        self.verticalLayout_2.addWidget(self.frame)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(5)
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


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.plainTextEdit = QPlainTextEdit(SideDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(0, 40))
        self.plainTextEdit.setMaximumSize(QSize(16777215, 40))
        font3 = QFont()
        font3.setFamily(u"Times New Roman")
        font3.setPointSize(16)
        font3.setBold(True)
        font3.setUnderline(True)
        font3.setStrikeOut(False)
        font3.setKerning(False)
        font3.setStyleStrategy(QFont.NoAntialias)
        self.plainTextEdit.setFont(font3)
        self.plainTextEdit.setStyleSheet(u"")
        self.plainTextEdit.setFrameShape(QFrame.NoFrame)
        self.plainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout_2.addWidget(self.plainTextEdit)


        self.retranslateUi(SideDialog)

        self.editButton.setDefault(True)
        self.iconButton.setDefault(True)
        self.newContactButton.setDefault(False)
        self.newGroupButton.setDefault(False)
        self.newChannelButton.setDefault(False)


        QMetaObject.connectSlotsByName(SideDialog)
    # setupUi

    def retranslateUi(self, SideDialog):
        SideDialog.setWindowTitle(QCoreApplication.translate("SideDialog", u"Dialog", None))
        self.editButton.setText(QCoreApplication.translate("SideDialog", u"Edit", None))
        self.iconButton.setText(QCoreApplication.translate("SideDialog", u"Image", None))
        self.lastLoginLabel.setText(QCoreApplication.translate("SideDialog", u"last seen 2021/06/25 at 06:11 PM", None))
        self.nameLabel.setText(QCoreApplication.translate("SideDialog", u"Apata Miracle Peter", None))
        self.lastLoginLabel_2.setText(QCoreApplication.translate("SideDialog", u"prmpsmart", None))
        self.newContactButton.setText(QCoreApplication.translate("SideDialog", u"New Contact", None))
        self.newGroupButton.setText(QCoreApplication.translate("SideDialog", u"New Group", None))
        self.newChannelButton.setText(QCoreApplication.translate("SideDialog", u"New Channel", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("SideDialog", u"   PRMP Chat by PRMPSmart   ", None))
    # retranslateUi

