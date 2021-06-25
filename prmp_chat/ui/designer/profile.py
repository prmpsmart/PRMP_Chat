# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Profile(object):
    def setupUi(self, Profile):
        if not Profile.objectName():
            Profile.setObjectName(u"Profile")
        Profile.resize(316, 150)
        Profile.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: white}\n"
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
        self.iconButton = QPushButton(Profile)
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
        self.layoutWidget = QWidget(Profile)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(180, 100, 131, 42))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.cancelButton = QPushButton(self.layoutWidget)
        self.cancelButton.setObjectName(u"cancelButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setMinimumSize(QSize(50, 40))
        self.cancelButton.setMaximumSize(QSize(50, 40))
        self.cancelButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelButton.setStyleSheet(u"n")

        self.horizontalLayout.addWidget(self.cancelButton)

        self.pushButton_8 = QPushButton(self.layoutWidget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setMinimumSize(QSize(50, 40))
        self.pushButton_8.setMaximumSize(QSize(50, 40))
        self.pushButton_8.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet(u"n")

        self.horizontalLayout.addWidget(self.pushButton_8)

        self.widget = QWidget(Profile)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(100, 20, 211, 68))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.nameLineEdit = QLineEdit(self.widget)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.nameLineEdit.sizePolicy().hasHeightForWidth())
        self.nameLineEdit.setSizePolicy(sizePolicy1)
        self.nameLineEdit.setMinimumSize(QSize(0, 30))
        self.nameLineEdit.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.nameLineEdit.setFont(font)
        self.nameLineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.nameLineEdit.setMouseTracking(False)
        self.nameLineEdit.setStyleSheet(u"")
        self.nameLineEdit.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.nameLineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.nameLineEdit)

        self.idLineEdit = QLineEdit(self.widget)
        self.idLineEdit.setObjectName(u"idLineEdit")
        sizePolicy1.setHeightForWidth(self.idLineEdit.sizePolicy().hasHeightForWidth())
        self.idLineEdit.setSizePolicy(sizePolicy1)
        self.idLineEdit.setMinimumSize(QSize(0, 30))
        self.idLineEdit.setMaximumSize(QSize(16777215, 30))
        self.idLineEdit.setFont(font)
        self.idLineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.idLineEdit.setMouseTracking(False)
        self.idLineEdit.setStyleSheet(u"")
        self.idLineEdit.setCursorMoveStyle(Qt.LogicalMoveStyle)
        self.idLineEdit.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.idLineEdit)

        self.iconButton.raise_()
        self.idLineEdit.raise_()
        self.nameLineEdit.raise_()
        self.layoutWidget.raise_()

        self.retranslateUi(Profile)

        self.iconButton.setDefault(True)


        QMetaObject.connectSlotsByName(Profile)
    # setupUi

    def retranslateUi(self, Profile):
        Profile.setWindowTitle(QCoreApplication.translate("Profile", u"Form", None))
        self.iconButton.setText(QCoreApplication.translate("Profile", u"Image", None))
        self.cancelButton.setText(QCoreApplication.translate("Profile", u"Cancel", None))
        self.pushButton_8.setText(QCoreApplication.translate("Profile", u"Next", None))
        self.nameLineEdit.setPlaceholderText(QCoreApplication.translate("Profile", u"Name", None))
        self.idLineEdit.setPlaceholderText(QCoreApplication.translate("Profile", u"ID", None))
    # retranslateUi

