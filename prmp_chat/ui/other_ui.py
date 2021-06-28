from PySide6.QtCore import QDateTime
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QMainWindow, QWidget
from .designer.chat_menu_dialog import *
from .designer.home import Ui_PRMPChat

from .designer.new_contact import Ui_NewContactDialog
from .designer.new_group import Ui_NewGroupDialog
from .designer.new_channel import Ui_NewChannelDialog
from .designer.settings import Ui_SettingsDialog
from .designer.profile import Ui_Profile
from .designer.side_dialog import Ui_SideDialog
from .designer.signup import Ui_Signup
from .designer.login import Ui_Login
from .designer.start import Ui_Start
from .designer.msg import Ui_Msg

from ..backend.client import *


class Setups(QWidget):
    UI = None

    def __init__(self, parent=None, flag=Qt.Widget, user=None, app=None):
        QWidget.__init__(self, parent, flag)

        self._par = parent
        self.user = user
        self.app = app or parent.app
        self.ui = self.UI()
        self.ui.setupUi(self)
    
    def centerWindow(self):
        size = self.size()
        a, b = size.width(), size.height()
        rect = self.app.screens()[0].availableGeometry()
        geo = QRect(int(rect.width()/2-a/2), int(rect.height()/2-b/2), a, b)
        self.setGeometry(geo)

    def closeEvent(self, event=0):
        if not self.parent(): self.app.quit()


class Popups(Setups):
    def __init__(self, **kwargs):
        Setups.__init__(self, flag=Qt.Popup, **kwargs)


class ChatMenu(Popups):
    UI = Ui_ChatMenu


class News(Popups):
    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
        self.ui.cancelButton.clicked.connect(self.close)


class NewContact(News, QWidget):
    UI = Ui_NewContactDialog

    def __init__(self, **kwargs):
        News.__init__(self, **kwargs)


class NewGroup(News):
    UI = Ui_NewGroupDialog

    def __init__(self, **kwargs):
        News.__init__(self, **kwargs)


class NewChannel(News):
    UI = Ui_NewChannelDialog

    def __init__(self, **kwargs):
        News.__init__(self, **kwargs)



class Profile(News):
    UI = Ui_Profile

    def __init__(self, **kwargs):
        News.__init__(self, **kwargs)

        self.ui.iconButton.setText('')
        self.ui.iconButton.setIconSize(QSize(70, 70))
        
        if self.user:
            self.ui.iconButton.setIcon(self.user.icon)
            self.ui.nameLineEdit.setText(self.user.name)
            self.ui.idLineEdit.setText(self.user.id)



class SettingsDialog(Popups):
    UI = Ui_SettingsDialog

    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
        
        self.ui.editProfileButton.clicked.connect(self.profileSettings)
    
    def profileSettings(self):
        profile = Profile(parent=self, user=self.user)

        pos = self.pos()
        geo = self.ui.editProfileButton.geometry()

        profile.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        profile.show()


class SideDialog(Popups):
    UI = Ui_SideDialog

    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
        
        self.ui.iconButton.setText('')
        self.ui.iconButton.setIconSize(QSize(70, 70))
        if self.user:
            if self.user.icon: self.ui.iconButton.setIcon(self.user.icon)

            self.ui.nameLabel.setText(self.user.name)
            self.ui.usernameLabel.setText(self.user.id)
            if self.user.status == STATUS.ONLINE: text = self.user.status
            else:
                datetime = DATETIME(self.user.last_seen)
                text = f"last login {datetime.toString('yyyy:MM:dd')} at {datetime.toString('HH:mm:ss')}"
            self.ui.lastLoginLabel.setText(text)
        
        self.ui.newContactButton.clicked.connect(self.openNewContact)
        self.ui.newGroupButton.clicked.connect(self.openNewGroup)
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        self.ui.editButton.clicked.connect(self.openSettings)
    
    def openNewContact(self):
        newContact = NewContact(parent=self, user=self.user)

        pos = self.pos()
        geo = self.ui.newContactButton.geometry()

        newContact.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newContact.show()
    
    def openNewGroup(self):
        newGroup = NewGroup(parent=self, user=self.user)

        pos = self.pos()
        geo = self.ui.newGroupButton.geometry()

        newGroup.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newGroup.show()
    
    def openNewChannel(self):
        newChannel = NewChannel(parent=self, user=self.user)

        pos = self.pos()
        geo = self.ui.newChannelButton.geometry()

        newChannel.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newChannel.show()
    
    def openSettings(self):
        settings = SettingsDialog(parent=self, user=self.user)

        pos = self.pos()
        geo = self.geometry()

        settings.move(pos.x()+geo.width()+10, pos.y())
        settings.show()




class Msg(News):
    UI = Ui_Msg

    def __init__(self, text='', **kwargs):
        News.__init__(self, **kwargs)
        self.ui.label.setText(text)
        rect = QFontMetrics(self.ui.label.font()).boundingRect(text)
        self.ui.label.setMaximumSize(QSize(rect.width(), rect.height()))
        self.centerWindow()
        self.show()


class Signup(Popups):
    UI = Ui_Signup

    def __init__(self, socket=None, **kwargs):
        Popups.__init__(self, **kwargs)
        self.ui.signupButton.clicked.connect(self.signup)
        self.socket = socket
    
    def signup(self):
        username = self.ui.usernameLineEdit.text()
        name = self.ui.nameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if username and password and name:
            if self.socket._connect():
                response = self.socket.signup(username, name, password)
                if response == RESPONSE.SUCCESSFUL:
                    msg = 'Signup Successful, proceed to Login.'
                    self._par.signupResponse()
                else: msg = str(response)
            else: msg = 'Connection Problem.'
        else: msg = 'All fields are required.'

        Msg(parent=self, text=msg)

    def showEvent(self, event=0): self._par.changeName('Signup')



class Login(Popups):
    UI = Ui_Login

    def __init__(self, socket=None, **kwargs):
        Popups.__init__(self, **kwargs)
        self.ui.loginButton.clicked.connect(self.login)
        self.socket = socket

    def login(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        response = ''

        username = password = 'ade0'

        # return self._par.loginResponse(RESPONSE.SUCCESSFUL)

        if username and password:
            if self.socket._connect():
                response = self.socket.login(username, password)
                msg = str(response)
            else: msg = 'Connection Problem.'
        else: msg = 'All fields are required.'

        Msg(parent=self, text=msg)
        if response == RESPONSE.SUCCESSFUL: self._par.loginResponse(response)
    
    def showEvent(self, event=0): self._par.changeName('Login')





