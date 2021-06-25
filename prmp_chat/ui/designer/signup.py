# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'signup.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Signup(object):
    def setupUi(self, Signup):
        if not Signup.objectName():
            Signup.setObjectName(u"Signup")
        Signup.resize(350, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Signup.sizePolicy().hasHeightForWidth())
        Signup.setSizePolicy(sizePolicy)
        Signup.setMinimumSize(QSize(350, 250))
        Signup.setMaximumSize(QSize(350, 250))
        Signup.setLayoutDirection(Qt.RightToLeft)
        Signup.setStyleSheet(u"QWidget {background: rgb(41, 58, 76); color: rgb(41, 58, 76)}\n"
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
        self.horizontalLayout = QHBoxLayout(Signup)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 9, 2, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.iconButton = QPushButton(Signup)
        self.iconButton.setObjectName(u"iconButton")
        self.iconButton.setMinimumSize(QSize(80, 80))
        self.iconButton.setMaximumSize(QSize(100, 100))
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

        self.verticalLayout_2.addWidget(self.iconButton)

        self.verticalSpacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nameLineEdit = QLineEdit(Signup)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.nameLineEdit.sizePolicy().hasHeightForWidth())
        self.nameLineEdit.setSizePolicy(sizePolicy1)
        self.nameLineEdit.setMinimumSize(QSize(220, 30))
        self.nameLineEdit.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.nameLineEdit.setFont(font)
        self.nameLineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.nameLineEdit.setMouseTracking(False)
        self.nameLineEdit.setStyleSheet(u"\n"
"color: white;\n"
"border-radius: 2px;")
        self.nameLineEdit.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.nameLineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.nameLineEdit)

        self.usernameLineEdit = QLineEdit(Signup)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        sizePolicy1.setHeightForWidth(self.usernameLineEdit.sizePolicy().hasHeightForWidth())
        self.usernameLineEdit.setSizePolicy(sizePolicy1)
        self.usernameLineEdit.setMinimumSize(QSize(0, 30))
        self.usernameLineEdit.setMaximumSize(QSize(16777215, 30))
        self.usernameLineEdit.setFont(font)
        self.usernameLineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.usernameLineEdit.setMouseTracking(False)
        self.usernameLineEdit.setStyleSheet(u"\n"
"color: white;\n"
"border-radius: 2px;")
        self.usernameLineEdit.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.usernameLineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit(Signup)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        sizePolicy1.setHeightForWidth(self.passwordLineEdit.sizePolicy().hasHeightForWidth())
        self.passwordLineEdit.setSizePolicy(sizePolicy1)
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

        self.signupButton = QPushButton(Signup)
        self.signupButton.setObjectName(u"signupButton")
        self.signupButton.setMinimumSize(QSize(50, 40))

        self.verticalLayout.addWidget(self.signupButton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Signup)

        self.iconButton.setDefault(True)


        QMetaObject.connectSlotsByName(Signup)
    # setupUi

    def retranslateUi(self, Signup):
        Signup.setWindowTitle(QCoreApplication.translate("Signup", u"Form", None))
        self.iconButton.setText(QCoreApplication.translate("Signup", u"Image", None))
        self.nameLineEdit.setPlaceholderText(QCoreApplication.translate("Signup", u"Name", None))
        self.usernameLineEdit.setPlaceholderText(QCoreApplication.translate("Signup", u"Username", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("Signup", u"Password", None))
        self.signupButton.setText(QCoreApplication.translate("Signup", u"Signup", None))
    # retranslateUi

