from other_ui import *
from prmp_chat.backend.client import *



class Home(Popups, QWidget):

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        
        self.app = app
        self.user = USER
        self.currentChatObject = None
        
        self.ui = Ui_PRMPChat()
        self.ui.setupUi(self)

        self.ui.chatList.currentChanged = self.chatListCurrentChanged

        self._flagChanged = True
        self.ui.winflag.clicked.connect(self.changeFlag)
        self.setSignals()
        self.changeFlag()
        self.chatTest()

        self.loadChatObjects(1)
    
    def chatListCurrentChanged(self, index, prev_index):
        self.currentChatObject = self.ui.chatList._delegate.item(index).chatObject
        self.ui.chatRoomList.clear()
        
        self.ui.roomName.setText(self.currentChatObject.name)
        chats = self.currentChatObject.chats

        for chat in chats:
            self.ui.chatRoomList.add(type='chat', tag=chat, chatObject=self.currentChatObject)
    
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
    
    def loadChatObjects(self, w=0):
        if not w: return

        self.ui.chatList.clear()


        if w == 1:
            # contacts
            pcs = self.user.chats.private_chats
            vals = list(pcs.values())

            def key(a): return a.last_time

            sorted_pcs = sorted(vals, key=key)

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
        sideDialog = SideDialog(self)

        pos = self.pos()
        sideDialog.move(pos.x(), pos.y()+28)
        sideDialog.show()

    def chatTest(self):
        chatList = self.ui.chatList
        chatRoomList = self.ui.chatRoomList
        

app = QApplication([])

import os, file
from prmp_chat_test import *
d = r'C:\Users\Administrator\Coding_Projects\C_C++\Qt\from_designer'
os.chdir(d)




window = Home(app=app)



app.exec_()

