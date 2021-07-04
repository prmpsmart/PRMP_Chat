from prmp_chat.ui.other_ui import *
from PySide6.QtGui import QFontMetrics
# from prmp_chat.ui.prmp_chat_test import *
import os
d = r'C:\Users\Administrator\Coding_Projects\C_C++\Qt\from_designer'
os.chdir(d)




app = QApplication([])

import prmp_chat.ui.file


class Home(Setups):
    UI = Ui_PRMPChat

    def __init__(self, **kwargs):
        super().__init__(flag=Qt.Widget | Qt.WindowStaysOnTopHint, **kwargs)

        self.currentChatObject = None
        self.currentChatList = 1
        self.setWindowTitle('PRMP Chat')

        self.ui.chatList.currentChanged = self.chatListCurrentChanged

        self._flagChanged = True

        self.ui.winflag.clicked.connect(self.changeFlag)
        self.ui.loginButton.clicked.connect(self.login)
        self.ui.logoutButton.clicked.connect(self.logout)

        self.setSignals()
        self.changeFlag()

        self.loadChatObjects(self.currentChatList)
        # self.statusTimer = QTimer(self)

# start of chat functions
    def chatListLoop(self): ...
    def chatRoomLoop(self): ...

    def loadChatObjects(self, w=0):
        if not (w and self.client.user): return
        self.currentChatList = w
        self.ui.chatList.clear()
        if w == 1: pcs = self.client.user.users
        elif w == 2: pcs = self.client.user.groups
        elif w == 3: pcs = self.client.user.channels
        
        def key(a): return a.last_time
        sorted_pcs = sorted(pcs.objects, key=key, reverse=1)
        for pc in sorted_pcs: self.ui.chatList.add(pc)

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
    
    def sendMessage(self):
        if not self.currentChatObject: return

        text = self.ui.textEdit.toPlainText()
        tag = Tag(sender=self.client.user.id, recipient=self.currentChatObject.id, data=text, date_time=DATETIME())

        if text:
            self.ui.chatRoomList.add(type='chat', tag=tag, chatObject=self.currentChatObject)

            self.currentChatObject.add_chat(tag)

            self.ui.textEdit.setPlainText('')

            self.loadChatObjects(self.currentChatList)
            self.ui.chatList.setSelection(QRect(0, 0, 2, 2), QItemSelectionModel.Clear)
            self.ui.chatList.setSelection(QRect(0, 0, 2, 2), QItemSelectionModel.Select)

# misc functions
    def login(self):
        self.client.relogin = True
        res = self.client.login()
        if res == RESPONSE.SUCCESSFUL: self.client.start_session()
        Msg(parent=self, text=str(res))

    def logout(self):
        self.client.relogin = False
        res = self.client.logout()
        Msg(parent=self, text=str(res))
    
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
    
    def receiveMessage(self): ...
    
    def changeFlag(self):
        if self._flagChanged:
            flag = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
            self._flagChanged = False
        else:
            flag = Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowStaysOnTopHint
            self._flagChanged = True

        self.setWindowFlags(flag)
        self.show()

    def maximizeWindow(self):
        geo = self.geometry()
        if geo.width() == 1013: self.setGeometry(geo.x(), geo.y(), 881, 510)
        else: self.setGeometry(geo.x(), geo.y(), 1013, 510)
    
    def openSideDialog(self):
        sideDialog = SideDialog(parent=self, client=self.client)

        pos = self.pos()
        sideDialog.move(pos.x(), pos.y()+28)
        sideDialog.show()

    def closeEvent(self, event):
        self.client.stop()
        SAVE(self.client.user)
        super().closeEvent(event=event)

class Start(Setups):
    UI = Ui_Start
    def __init__(self, app):
        super().__init__(None, flag=Qt.Widget | Qt.WindowStaysOnTopHint, app=app, client=Client(user=LOAD(), relogin=1))

        self.centerWindow()
        self.changeName = lambda name: self.setWindowTitle(f'PRMP Chat - {name}')
        self.setMaximumWidth(self.size().width())

        if not self.client.user:
            self.signup = Signup(parent=self, client=self.client)
            self.login = Login(parent=self, client=self.client)
            self.ui.horizontalLayout.addWidget(self.login)
            self.ui.horizontalLayout.addWidget(self.signup)

            self.changeAction()
            self.ui.checkBox.stateChanged.connect(self.changeAction)
            self.show()
        
        else: self.launch()
    
    def signupResponse(self):
        self.client.user = self.client.user
        
        self.login.ui.usernameLineEdit.setText(self.client.user.id)
        self.login.ui.passwordLineEdit.setText(self.client.user.key)
    
    def changeAction(self, event=0):
        if event == Qt.Checked:
            self.signup.show()
            self.login.close()
        else:
            self.signup.close()
            self.login.show()

    def loginResponse(self, response):
        if response == RESPONSE.SUCCESSFUL:
            self.close()
            THREAD(SAVE, self.client.user)
            # SAVE(self.client.user)
            self.launch()
    
    def launch(self):
        THREAD(self.client.start_session)
        
        Home(app=self.app, client=self.client).show()
    
    def closeEvent(self, event=0): ...












window = Start(app=app)



app.exec_()

