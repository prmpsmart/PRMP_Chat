from typing import Set
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow, QWidget
from designer.chat_menu_dialog import *
from designer.home import Ui_PRMPChat

from designer.new_contact import Ui_NewContactDialog
from designer.new_group import Ui_NewGroupDialog
from designer.new_channel import Ui_NewChannelDialog
from designer.settings import Ui_SettingsDialog
from designer.profile import Ui_Profile
from designer.side_dialog import Ui_SideDialog
from designer.signup import Ui_Signup
from designer.login import Ui_Login
from designer.start import Ui_Start

from prmp_chat.backend.client import *


class Setups(QWidget):
    UI = None

    def __init__(self, parent, flag=Qt.Widget, user=None):
        QWidget.__init__(self, parent, flag)

        self.user = user
        self.ui = self.UI()
        self.ui.setupUi(self)


class Popups(Setups):
    def __init__(self, parent=None, user=None):
        Setups.__init__(self, parent, Qt.Popup, user)

    def closeEvent(self, event=0):
        if not self.parent(): self.app.quit()


class ChatMenu(Popups):
    UI = Ui_ChatMenu


class News(Popups):
    def __init__(self, parent=None, user=None):
        Popups.__init__(self, parent, user)
        self.ui.cancelButton.clicked.connect(self.close)


class NewContact(News, QWidget):
    UI = Ui_NewContactDialog

    def __init__(self, parent=None, user=None):
        News.__init__(self, parent, user)


class NewGroup(News):
    UI = Ui_NewGroupDialog

    def __init__(self, parent=None, user=None):
        News.__init__(self, parent, user)


class NewChannel(News):
    UI = Ui_NewChannelDialog

    def __init__(self, parent=None, user=None):
        News.__init__(self, parent, user)



class Profile(News):
    UI = Ui_Profile

    def __init__(self, parent=None, user=None):
        News.__init__(self, parent, user)

        self.ui.iconButton.setText('')
        self.ui.iconButton.setIconSize(QSize(70, 70))
        self.ui.iconButton.setIcon(user.icon)

        self.ui.nameLineEdit.setText(user.name)
        self.ui.idLineEdit.setText(user.id)



class SettingsDialog(Popups):
    UI = Ui_SettingsDialog

    def __init__(self, parent=None, user=None):
        Popups.__init__(self, parent, user)
        
        self.ui.editProfileButton.clicked.connect(self.profileSettings)
    
    def profileSettings(self):
        profile = Profile(self, self.user)

        pos = self.pos()
        geo = self.ui.editProfileButton.geometry()

        profile.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        profile.show()


class SideDialog(Popups):
    UI = Ui_SideDialog

    def __init__(self, parent=None, user=None):
        Popups.__init__(self, parent, user)
        
        self.ui.iconButton.setText('')
        self.ui.iconButton.setIconSize(QSize(70, 70))
        self.ui.iconButton.setIcon(user.icon)
        
        self.ui.newContactButton.clicked.connect(self.openNewContact)
        self.ui.newGroupButton.clicked.connect(self.openNewGroup)
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        self.ui.editButton.clicked.connect(self.openSettings)
    
    def openNewContact(self):
        newContact = NewContact(self, self.user)

        pos = self.pos()
        geo = self.ui.newContactButton.geometry()

        newContact.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newContact.show()
    
    def openNewGroup(self):
        newGroup = NewGroup(self, self.user)

        pos = self.pos()
        geo = self.ui.newGroupButton.geometry()

        newGroup.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newGroup.show()
    
    def openNewChannel(self):
        newChannel = NewChannel(self, self.user)

        pos = self.pos()
        geo = self.ui.newChannelButton.geometry()

        newChannel.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newChannel.show()
    
    def openSettings(self):
        settings = SettingsDialog(self, self.user)

        pos = self.pos()
        geo = self.geometry()

        settings.move(pos.x()+geo.width()+10, pos.y())
        settings.show()




class Login(Popups):
    UI = Ui_Login

    def __init__(self, parent=None, socket=None):
        Popups.__init__(self, parent, None)

        self.ui.loginButton.clicked.connect(self.login)
        self.socket = socket

    def login(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if username and password:
            if not self.socket.connected: self.socket._connect()
            response = self.socket.login(username, password)
            print(response, 'hjhj')



class Signup(Popups):
    UI = Ui_Signup

    def __init__(self, parent=None, socket=None):
        Popups.__init__(self, parent, None)
        self._par = parent

        self.ui.signupButton.clicked.connect(self.signup)
        self.socket = socket

    
    def signup(self):
        username = self.ui.usernameLineEdit.text()
        name = self.ui.nameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if username and password:
            if not self.socket.connected: self.socket._connect()
            response = self.socket.signup(username, name, password)
            self._par.loginResponse(response)




