# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_group.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_NewGroupDialog(object):
    def setupUi(self, NewGroupDialog):
        if not NewGroupDialog.objectName():
            NewGroupDialog.setObjectName(u"NewGroupDialog")
        NewGroupDialog.resize(350, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewGroupDialog.sizePolicy().hasHeightForWidth())
        NewGroupDialog.setSizePolicy(sizePolicy)
        NewGroupDialog.setMinimumSize(QSize(350, 150))
        NewGroupDialog.setMaximumSize(QSize(350, 150))
        NewGroupDialog.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: white}\n"
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
        self.pushButton_6 = QPushButton(NewGroupDialog)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(10, 10, 80, 80))
        self.pushButton_6.setStyleSheet(u"\n"
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
        self.pushButton_6.setAutoDefault(False)
        self.pushButton_6.setFlat(False)
        self.lineEdit = QLineEdit(NewGroupDialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(100, 40, 242, 30))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setCursor(QCursor(Qt.IBeamCursor))
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setStyleSheet(u"")
        self.lineEdit.setCursorMoveStyle(Qt.VisualMoveStyle)
        self.lineEdit.setClearButtonEnabled(True)
        self.cancelButton = QPushButton(NewGroupDialog)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setGeometry(QRect(210, 100, 50, 40))
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setMinimumSize(QSize(50, 40))
        self.cancelButton.setMaximumSize(QSize(50, 40))
        self.cancelButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancelButton.setStyleSheet(u"n")
        self.pushButton_8 = QPushButton(NewGroupDialog)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(270, 100, 50, 40))
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setMinimumSize(QSize(50, 40))
        self.pushButton_8.setMaximumSize(QSize(50, 40))
        self.pushButton_8.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet(u"n")

        self.retranslateUi(NewGroupDialog)

        self.pushButton_6.setDefault(True)


        QMetaObject.connectSlotsByName(NewGroupDialog)
    # setupUi

    def retranslateUi(self, NewGroupDialog):
        NewGroupDialog.setWindowTitle(QCoreApplication.translate("NewGroupDialog", u"Dialog", None))
        self.pushButton_6.setText(QCoreApplication.translate("NewGroupDialog", u"Image", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("NewGroupDialog", u"Group Name", None))
        self.cancelButton.setText(QCoreApplication.translate("NewGroupDialog", u"Cancel", None))
        self.pushButton_8.setText(QCoreApplication.translate("NewGroupDialog", u"Next", None))
    # retranslateUi

