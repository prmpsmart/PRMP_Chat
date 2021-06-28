from prmp_chat.ui.other_ui import *
from PySide6.QtGui import QFontMetrics
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File
# from prmp_chat.ui.prmp_chat_test import *
import os
d = r'C:\Users\Administrator\Coding_Projects\C_C++\Qt\from_designer'
os.chdir(d)




app = QApplication([])

import prmp_chat.ui.file




FILE_DIR = os.path.dirname(__file__)
FILE = os.path.join(FILE_DIR, 'CLIENT_DATA.pc')


def SAVE(user):
    _file = PRMP_File(FILE, perm='w')
    _file.saveObj(user)
    _file.save()

def LOAD():
    _file = PRMP_File(FILE)
    user = _file.loadObj()
    return user


class Home(Setups):
    UI = Ui_PRMPChat

    def __init__(self, socket=None, **kwargs):
        self.socket = socket

        super().__init__(user=self.socket.user, **kwargs)
        
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
        self.statusTimer = QTimer(self)
    
    def login(self):
        res = self.socket.login()
        Msg(parent=self, text=str(res))
    
    def logout(self):
        res = self.socket.logout()
        if isinstance(res, int): res = 'Logout successful.'
        Msg(parent=self, text=str(res))
    
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
        if not (w and self.user): return

        self.currentChatList = w

        self.ui.chatList.clear()

        if w == 1: pcs = self.user.chats.private_chats
        elif w == 2: pcs = self.user.groups
        elif w == 3: pcs = self.user.channels
        
        def key(a): return a.last_time
        vals = list(pcs.values())

        sorted_pcs = sorted(vals, key=key, reverse=1)

        for pc in sorted_pcs: self.ui.chatList.add(pc)
        
    def sendMessage(self):
        if not self.currentChatObject: return

        text = self.ui.textEdit.toPlainText()
        tag = Tag(sender=self.user.id, recipient=self.currentChatObject.id, data=text, date_time=DATETIME())

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
        sideDialog = SideDialog(parent=self, user=self.user)

        pos = self.pos()
        sideDialog.move(pos.x(), pos.y()+28)
        sideDialog.show()
    
    def closeEvent(self, event):
        self.socket.logout()
        SAVE(self.user)
        super().closeEvent(event=event)


class Start(Setups):
    UI = Ui_Start
    def __init__(self, app):
        # super().__init__(None, flag=Qt.FramelessWindowHint, app=app)
        super().__init__(None, flag=Qt.Widget | Qt.WindowStaysOnTopHint, app=app, user=LOAD())

        self.centerWindow()
        self.changeName = lambda name: self.setWindowTitle(f'PRMP Chat - {name}')
        self.setMaximumWidth(self.size().width())
        self.socket = Client(user=self.user)

        if not self.socket.user:
            self.signup = Signup(parent=self, socket=self.socket)
            self.login = Login(parent=self, socket=self.socket)
            self.ui.horizontalLayout.addWidget(self.login)
            self.ui.horizontalLayout.addWidget(self.signup)

            self.changeAction()

            self.ui.checkBox.stateChanged.connect(self.changeAction)
            self.show()
        
        else: self.launch()
    
    def signupResponse(self):
        self.user = self.socket.user
        
        self.login.ui.usernameLineEdit.setText(self.user.id)
        self.login.ui.passwordLineEdit.setText(self.user.key)
    
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
            THREAD(SAVE, self.socket.user)
            # SAVE(self.socket.user)
            self.launch()
    
    def launch(self): Home(app=self.app, socket=self.socket).show()
    
    def closeEvent(self, event=0): ...












window = Start(app=app)



app.exec_()

