# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(176, 222)
        SettingsDialog.setMaximumSize(QSize(278, 411))
        SettingsDialog.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: rgb(234, 183, 78)}\n"
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
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.editProfileButton = QPushButton(SettingsDialog)
        self.editProfileButton.setObjectName(u"editProfileButton")
        self.editProfileButton.setMinimumSize(QSize(0, 40))
        self.editProfileButton.setLayoutDirection(Qt.LeftToRight)
        self.editProfileButton.setFlat(True)

        self.verticalLayout.addWidget(self.editProfileButton)

        self.pushButton_2 = QPushButton(SettingsDialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QSize(0, 40))
        self.pushButton_2.setMaximumSize(QSize(16777215, 40))
        self.pushButton_2.setFlat(True)

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(SettingsDialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 40))
        self.pushButton_3.setFlat(True)

        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(SettingsDialog)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(0, 40))
        self.pushButton_4.setStyleSheet(u"")
        self.pushButton_4.setFlat(True)

        self.verticalLayout.addWidget(self.pushButton_4)


        self.retranslateUi(SettingsDialog)

        self.editProfileButton.setDefault(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_3.setDefault(False)
        self.pushButton_4.setDefault(False)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Dialog", None))
        self.editProfileButton.setText(QCoreApplication.translate("SettingsDialog", u"Edit Profile", None))
        self.pushButton_2.setText(QCoreApplication.translate("SettingsDialog", u"Download Path", None))
        self.pushButton_3.setText(QCoreApplication.translate("SettingsDialog", u"Chat Settings", None))
        self.pushButton_4.setText(QCoreApplication.translate("SettingsDialog", u"Advance Settings", None))
    # retranslateUi

