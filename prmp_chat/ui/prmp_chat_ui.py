from prmp_chat.backend.core import RESPONSE
from prmp_chat.ui.other_ui import Login
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QFrame, QWidget
from other_ui import *



class Home(Popups, QWidget):
    UI = Ui_PRMPChat

    def __init__(self, parent=None, app=None):
        super().__init__(parent, USER)
        
        self.app = app
        self.currentChatObject = None
        self.currentChatList = 1
        
        self.ui.chatList.currentChanged = self.chatListCurrentChanged

        self._flagChanged = True
        self.ui.winflag.clicked.connect(self.changeFlag)
        self.setSignals()
        self.changeFlag()

        self.loadChatObjects(self.currentChatList)
    
    def chatListCurrentChanged(self, index, prev_index):
        current = self.ui.chatList._delegate.item(index)
        self.currentChatObject = current.chatObject
        self.ui.chatRoomList.clear()

        self.ui.roomName.setIconSize(QSize(45, 35))
        self.ui.roomName.setIcon(current.icon)
        
        self.ui.roomName.setText(current.name)
        chats = self.currentChatObject.chats

        for chat in chats:
            self.ui.chatRoomList.add(type='chat', tag=chat, chatObject=self.currentChatObject)
        
        self.currentChatObject.read()
    
    def loadUser(self):
        ...
    
    def setSignals(self):
        self.ui.menuButton.clicked.connect(self.openSideDialog)
        self.ui.minimizeButton.clicked.connect(self.showMinimized)
        self.ui.maximizeButton.clicked.connect(self.maximizeWindow)
        self.ui.exitButton.clicked.connect(self.closeEvent)

        self.ui.audioSendButton.clicked.connect(self.sendMessage)

        self.ui.contactButton.clicked.connect(lambda: self.loadChatObjects(1))
        self.ui.groupButton.clicked.connect(lambda: self.loadChatObjects(2))
        self.ui.channelButton.clicked.connect(lambda: self.loadChatObjects(3))

        self.ui.textEdit.textChanged.connect(self.resizeTextEdit)
    
    def resizeTextEdit(self):
        textEdit  =self.ui.textEdit
        fontMetrics = QFontMetrics(textEdit.currentFont())
        rect = textEdit.rect()
        needed = fontMetrics.boundingRect(0, 0, rect.width(), 0, Qt.AlignLeft | Qt.AlignTop | Qt.TextWrapAnywhere, textEdit.toPlainText())

        mx = 200
        mn = 40

        n = needed.height()
        r = rect.height()

        if mn < n < mx: h = n
        elif n > mx: h = mx
        else: h = mn
        
        textEdit.setMinimumHeight(h)
        textEdit.setMaximumHeight(h)
    
    def loadChatObjects(self, w=0):
        if not w: return
        self.currentChatList = w

        self.ui.chatList.clear()

        if w == 1:
            # contacts
            pcs = self.user.chats.private_chats
            vals = list(pcs.values())

            def key(a): return a.last_time

            sorted_pcs = sorted(vals, key=key, reverse=1)

            for pc in sorted_pcs: self.ui.chatList.add(pc)

        elif w == 2:
            # groups
            ...
        elif w == 3:
            # channels
            ...
        
    def sendMessage(self):
        if not self.currentChatObject: return

        text = self.ui.textEdit.toPlainText()
        tag = Tag(sender=self.user.id, recipient=self.currentChatObject.id, data=text, date_time=DATE_TIME())

        if text:
            self.ui.chatRoomList.add(type='chat', tag=tag, chatObject=self.currentChatObject)

            self.currentChatObject.add_chat(tag)

            self.ui.textEdit.setPlainText('')

            self.loadChatObjects(self.currentChatList)
            self.ui.chatList.setSelection(QRect(0, 0, 2, 2), QItemSelectionModel.Clear)
            self.ui.chatList.setSelection(QRect(0, 0, 2, 2), QItemSelectionModel.Select)
    
    def receiveMessage(self): ...
    
    def changeFlag(self):
        if self._flagChanged:
            flag = Qt.Window | Qt.FramelessWindowHint
            self._flagChanged = False
        else:
            flag = Qt.Window | Qt.WindowSystemMenuHint
            self._flagChanged = True

        self.setWindowFlags(flag)
        self.show()

    def maximizeWindow(self):
        geo = self.geometry()
        if geo.width() == 1013: self.setGeometry(geo.x(), geo.y(), 881, 510)
        else: self.setGeometry(geo.x(), geo.y(), 1013, 510)
    
    def openSideDialog(self):
        sideDialog = SideDialog(self, self.user)

        pos = self.pos()
        sideDialog.move(pos.x(), pos.y()+28)
        sideDialog.show()

        


class Start(Setups):
    UI = Ui_Start
    def __init__(self, app):
        self.app = app
        super().__init__(None, flag=Qt.FramelessWindowHint)

        size = self.size()
        a, b = size.width(), size.height()
        rect = app.screens()[0].availableGeometry()
        geo = QRect(int(rect.width()/2-a/2), int(rect.height()/2-b/2), 400, 300)
        self.setGeometry(geo)
        
        USER = None
        self.socket = Client()

        self.socket.signup('p', 'PRMP', 'p')

        if not USER:
            self.signup = Signup(self, self.socket)
            self.login = Login(self, self.socket)
            self.ui.horizontalLayout.addWidget(self.login)
            self.ui.horizontalLayout.addWidget(self.signup)

            self.changeAction()

            self.ui.checkBox.stateChanged.connect(self.changeAction)
            self.show()
        
        else: exit()
    
    def changeAction(self, event=0):
        if event == Qt.Checked:
            self.signup.show()
            self.login.close()
        else:
            self.signup.close()
            self.login.show()
    
    def loginResponse(self, response):
        if response == RESPONSE.SUCCESSFUL:
            app = self.app
            self.app = None
            self.close()
            Home(app).show()











app = QApplication([])

import os, file
from prmp_chat_test import *
d = r'C:\Users\Administrator\Coding_Projects\C_C++\Qt\from_designer'
os.chdir(d)




window = Start(app=app)



app.exec_()

