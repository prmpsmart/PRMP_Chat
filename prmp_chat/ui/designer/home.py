
import sys
sys.path.append(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\PRMP_Chat\prmp_chat\ui')
from chatList import ChatList, ChatRoomList

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_PRMPChat(object):
    def setupUi(self, PRMPChat):
        if not PRMPChat.objectName():
            PRMPChat.setObjectName(u"PRMPChat")
        PRMPChat.resize(881, 510)
        PRMPChat.setStyleSheet(u"QWidget {background: rgb(41, 58, 76); color: rgb(41, 58, 76)}\n"
"\n"
" QPushButton{\n"
"	border: 1px solid;\n"
"	border-radius: 4px ;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));\n"
"	color: rgb(234, 183, 78)\n"
"}\n"
"\n"
"\n"
" QPushButton:pressed {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 0 rgb(170, 132, 57), stop: 1 rgb(234, 183, 78));\n"
"	color:  rgb(20, 36, 43)\n"
"  }\n"
"\n"
"")
        self.verticalLayout_4 = QVBoxLayout(PRMPChat)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(PRMPChat)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(35, 28))
        self.frame.setMaximumSize(QSize(909090, 35))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.winflag = QPushButton(self.frame)
        self.winflag.setObjectName(u"winflag")
        self.winflag.setMinimumSize(QSize(20, 24))
        self.winflag.setMaximumSize(QSize(20, 24))

        self.horizontalLayout_5.addWidget(self.winflag)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(600, 0))
        self.label.setStyleSheet(u" QLabel{\n"
"	border: 1px solid;\n"
"	border-radius: 4px ;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));\n"
"	color: rgb(234, 183, 78)\n"
"}")

        self.horizontalLayout_5.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.minimizeButton = QPushButton(self.frame)
        self.minimizeButton.setObjectName(u"minimizeButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minimizeButton.sizePolicy().hasHeightForWidth())
        self.minimizeButton.setSizePolicy(sizePolicy)
        self.minimizeButton.setMinimumSize(QSize(20, 24))
        self.minimizeButton.setMaximumSize(QSize(20, 24))
        icon = QIcon()
        icon.addFile(u"minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeButton.setIcon(icon)
        self.minimizeButton.setIconSize(QSize(15, 15))

        self.horizontalLayout_5.addWidget(self.minimizeButton)

        self.maximizeButton = QPushButton(self.frame)
        self.maximizeButton.setObjectName(u"maximizeButton")
        sizePolicy.setHeightForWidth(self.maximizeButton.sizePolicy().hasHeightForWidth())
        self.maximizeButton.setSizePolicy(sizePolicy)
        self.maximizeButton.setMinimumSize(QSize(20, 24))
        self.maximizeButton.setMaximumSize(QSize(20, 24))
        icon1 = QIcon()
        icon1.addFile(u"maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeButton.setIcon(icon1)
        self.maximizeButton.setIconSize(QSize(15, 15))

        self.horizontalLayout_5.addWidget(self.maximizeButton)

        self.exitButton = QPushButton(self.frame)
        self.exitButton.setObjectName(u"exitButton")
        sizePolicy.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.setMinimumSize(QSize(20, 24))
        self.exitButton.setMaximumSize(QSize(20, 24))
        icon2 = QIcon()
        icon2.addFile(u"exit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.exitButton.setIcon(icon2)
        self.exitButton.setIconSize(QSize(15, 15))
        self.exitButton.setCheckable(False)

        self.horizontalLayout_5.addWidget(self.exitButton)


        self.verticalLayout_4.addWidget(self.frame)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, -1, 8, 9)
        self.frame_2 = QFrame(PRMPChat)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(60, 0))
        self.frame_2.setMaximumSize(QSize(60, 16777215))
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 4, 0)
        self.menuButton = QPushButton(self.frame_2)
        self.menuButton.setObjectName(u"menuButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menuButton.sizePolicy().hasHeightForWidth())
        self.menuButton.setSizePolicy(sizePolicy1)
        self.menuButton.setMinimumSize(QSize(50, 40))
        self.menuButton.setMaximumSize(QSize(60, 40))
        self.menuButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.menuButton.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.menuButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.contactButton = QPushButton(self.frame_2)
        self.contactButton.setObjectName(u"contactButton")
        sizePolicy1.setHeightForWidth(self.contactButton.sizePolicy().hasHeightForWidth())
        self.contactButton.setSizePolicy(sizePolicy1)
        self.contactButton.setMinimumSize(QSize(50, 40))
        self.contactButton.setMaximumSize(QSize(60, 40))
        self.contactButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.contactButton.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.contactButton)

        self.groupButton = QPushButton(self.frame_2)
        self.groupButton.setObjectName(u"groupButton")
        sizePolicy1.setHeightForWidth(self.groupButton.sizePolicy().hasHeightForWidth())
        self.groupButton.setSizePolicy(sizePolicy1)
        self.groupButton.setMinimumSize(QSize(50, 40))
        self.groupButton.setMaximumSize(QSize(60, 40))
        self.groupButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.groupButton.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.groupButton)

        self.channelButton = QPushButton(self.frame_2)
        self.channelButton.setObjectName(u"channelButton")
        sizePolicy1.setHeightForWidth(self.channelButton.sizePolicy().hasHeightForWidth())
        self.channelButton.setSizePolicy(sizePolicy1)
        self.channelButton.setMinimumSize(QSize(50, 40))
        self.channelButton.setMaximumSize(QSize(60, 40))
        self.channelButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.channelButton.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.channelButton)

        self.verticalSpacer_2 = QSpacerItem(20, 240, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.frame_2)

        self.splitter = QSplitter(PRMPChat)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setStyleSheet(u"background: rgb(41, 58, 76)")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(3)
        self.splitter.setChildrenCollapsible(False)
        self.frame_3 = QFrame(self.splitter)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(400, 450))
        self.frame_3.setMaximumSize(QSize(400, 16777215))
        self.frame_3.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: white}\n"
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
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 2, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.lineEdit = QLineEdit(self.frame_3)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy2)
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setStyleSheet(u"\n"
"color: white;\n"
"border-radius: 2px;")
        self.lineEdit.setCursorMoveStyle(Qt.VisualMoveStyle)
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.frame_3)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy3)
        self.pushButton.setMinimumSize(QSize(0, 30))
        self.pushButton.setMaximumSize(QSize(50, 30))
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.chatList = ChatList(self.frame_3)
        self.chatList.setObjectName(u"chatList")
        self.chatList.setMinimumSize(QSize(0, 400))
        self.chatList.setAutoFillBackground(False)
        self.chatList.setStyleSheet(u"border-radius: 4px")
        self.chatList.setLineWidth(0)
        self.chatList.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.chatList.setDragEnabled(True)
        self.chatList.setDragDropMode(QAbstractItemView.InternalMove)

        self.verticalLayout.addWidget(self.chatList)

        self.splitter.addWidget(self.frame_3)
        self.frame_4 = QFrame(self.splitter)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(400, 450))
        self.frame_4.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: white}\n"
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
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.roomName = QPushButton(self.frame_4)
        self.roomName.setObjectName(u"roomName")
        self.roomName.setMinimumSize(QSize(200, 40))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(14)
        font1.setBold(True)
        self.roomName.setFont(font1)
        self.roomName.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.roomName)

        self.pushButton_4 = QPushButton(self.frame_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy3.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy3)
        self.pushButton_4.setMaximumSize(QSize(50, 40))
        self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.pushButton_4)

        self.pushButton_2 = QPushButton(self.frame_4)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy3.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy3)
        self.pushButton_2.setMaximumSize(QSize(50, 40))
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setMouseTracking(True)
        self.pushButton_2.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.chatRoomList = ChatRoomList(self.frame_4)
        self.chatRoomList.setObjectName(u"chatRoomList")
        self.chatRoomList.setMinimumSize(QSize(0, 360))
        self.chatRoomList.setStyleSheet(u"border-radius: 4px")
        self.chatRoomList.setLineWidth(0)
        self.chatRoomList.setDragDropMode(QAbstractItemView.InternalMove)

        self.verticalLayout_2.addWidget(self.chatRoomList)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_9 = QPushButton(self.frame_4)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy3.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy3)
        self.pushButton_9.setMinimumSize(QSize(40, 40))
        self.pushButton_9.setMaximumSize(QSize(40, 40))
        self.pushButton_9.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.pushButton_9)

        self.textEdit = QTextEdit(self.frame_4)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        font2.setPointSize(12)
        self.textEdit.setFont(font2)
        self.textEdit.setStyleSheet(u"\n"
"color: white;\n"
"border-radius: 2px;")

        self.horizontalLayout_2.addWidget(self.textEdit)

        self.pushButton_10 = QPushButton(self.frame_4)
        self.pushButton_10.setObjectName(u"pushButton_10")
        sizePolicy3.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy3)
        self.pushButton_10.setMinimumSize(QSize(40, 40))
        self.pushButton_10.setMaximumSize(QSize(40, 40))
        self.pushButton_10.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_10.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.pushButton_10)

        self.audioSendButton = QPushButton(self.frame_4)
        self.audioSendButton.setObjectName(u"audioSendButton")
        sizePolicy3.setHeightForWidth(self.audioSendButton.sizePolicy().hasHeightForWidth())
        self.audioSendButton.setSizePolicy(sizePolicy3)
        self.audioSendButton.setMinimumSize(QSize(40, 40))
        self.audioSendButton.setMaximumSize(QSize(40, 40))
        self.audioSendButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.audioSendButton.setStyleSheet(u"n")

        self.horizontalLayout_2.addWidget(self.audioSendButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.frame_4)

        self.horizontalLayout.addWidget(self.splitter)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.retranslateUi(PRMPChat)

        QMetaObject.connectSlotsByName(PRMPChat)
    # setupUi

    def retranslateUi(self, PRMPChat):
        PRMPChat.setWindowTitle(QCoreApplication.translate("PRMPChat", u"Form", None))
        self.winflag.setText(QCoreApplication.translate("PRMPChat", u"____", None))
        self.label.setText(QCoreApplication.translate("PRMPChat", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">PRMP Chat</span></p></body></html>", None))
        self.minimizeButton.setText("")
        self.maximizeButton.setText("")
        self.exitButton.setText("")
        self.menuButton.setText(QCoreApplication.translate("PRMPChat", u"Menu", None))
        self.contactButton.setText(QCoreApplication.translate("PRMPChat", u"Contacts", None))
        self.groupButton.setText(QCoreApplication.translate("PRMPChat", u"Groups", None))
        self.channelButton.setText(QCoreApplication.translate("PRMPChat", u"Channels", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("PRMPChat", u"Search...", None))
        self.pushButton.setText(QCoreApplication.translate("PRMPChat", u"Search", None))
        self.roomName.setText(QCoreApplication.translate("PRMPChat", u"Chat Name", None))
        self.pushButton_4.setText(QCoreApplication.translate("PRMPChat", u"Search", None))
        self.pushButton_2.setText(QCoreApplication.translate("PRMPChat", u"Menu", None))
        self.pushButton_9.setText(QCoreApplication.translate("PRMPChat", u"Link", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("PRMPChat", u"Write a message ...", None))
        self.pushButton_10.setText(QCoreApplication.translate("PRMPChat", u"Emoji", None))
        self.audioSendButton.setText(QCoreApplication.translate("PRMPChat", u"Audio\n"
"Send", None))
    # retranslateUi

