# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(229, 172)
        Login.setStyleSheet(u"QWidget {background: rgb(41, 58, 76); color: rgb(41, 58, 76)}\n"
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
        self.verticalLayout = QVBoxLayout(Login)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.usernameLineEdit = QLineEdit(Login)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameLineEdit.sizePolicy().hasHeightForWidth())
        self.usernameLineEdit.setSizePolicy(sizePolicy)
        self.usernameLineEdit.setMinimumSize(QSize(0, 30))
        self.usernameLineEdit.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.usernameLineEdit.setFont(font)
        self.usernameLineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.usernameLineEdit.setMouseTracking(False)
        self.usernameLineEdit.setStyleSheet(u"\n"
"color: white;\n"
"border-radius: 2px;")
        self.usernameLineEdit.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.usernameLineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit(Login)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        sizePolicy.setHeightForWidth(self.passwordLineEdit.sizePolicy().hasHeightForWidth())
        self.passwordLineEdit.setSizePolicy(sizePolicy)
        self.passwordLineEdit.setMinimumSize(QSize(0, 30))
        self.passwordLineEdit.setMaximumSize(QSize(16777215, 30))
        self.passwordLineEdit.setFont(font)
        self.passwordLineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.passwordLineEdit.setMouseTracking(False)
        self.passwordLineEdit.setStyleSheet(u"\n"
"color: white;\n"
"border-radius: 2px;")
        self.passwordLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.passwordLineEdit.setCursorMoveStyle(Qt.VisualMoveStyle)
        self.passwordLineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.passwordLineEdit)

        self.loginButton = QPushButton(Login)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMinimumSize(QSize(50, 40))

        self.verticalLayout.addWidget(self.loginButton)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Form", None))
        self.usernameLineEdit.setPlaceholderText(QCoreApplication.translate("Login", u"Username", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("Login", u"Password", None))
        self.loginButton.setText(QCoreApplication.translate("Login", u"Login", None))
    # retranslateUi

