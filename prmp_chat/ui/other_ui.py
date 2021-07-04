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

    def __init__(self, parent=None, flag=Qt.Widget, client=None, app=None):
        QWidget.__init__(self, parent, flag)

        self._par = parent
        self.client = client
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
        user = self.client.user
        
        if user:
            self.ui.iconButton.setIcon(user.icon)
            self.ui.nameLineEdit.setText(user.name)
            self.ui.idLineEdit.setText(user.id)


class SettingsDialog(Popups):
    UI = Ui_SettingsDialog

    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
        
        self.ui.editProfileButton.clicked.connect(self.profileSettings)
    
    def profileSettings(self):
        profile = Profile(parent=self, client=self.client)

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
        user = self.client.user

        if user:
            if user.icon: self.ui.iconButton.setIcon(user.icon)
            self.ui.nameLabel.setText(user.name)
            self.ui.usernameLabel.setText(user.id)
            if user.status == STATUS.ONLINE: text = user.status
            else: text = f"last login {user.str_last_seen}"
            self.ui.lastLoginLabel.setText(text)
        else:
            self.ui.nameLabel.setText('')
            self.ui.usernameLabel.setText('')
            self.ui.lastLoginLabel.setText('')
        
        self.ui.newContactButton.clicked.connect(self.openNewContact)
        self.ui.newGroupButton.clicked.connect(self.openNewGroup)
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        self.ui.editButton.clicked.connect(self.openSettings)
    
    def openNewContact(self):
        newContact = NewContact(parent=self, client=self.client)

        pos = self.pos()
        geo = self.ui.newContactButton.geometry()

        newContact.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newContact.show()
    
    def openNewGroup(self):
        newGroup = NewGroup(parent=self, client=self.client)

        pos = self.pos()
        geo = self.ui.newGroupButton.geometry()

        newGroup.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newGroup.show()
    
    def openNewChannel(self):
        newChannel = NewChannel(parent=self, client=self.client)

        pos = self.pos()
        geo = self.ui.newChannelButton.geometry()

        newChannel.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newChannel.show()
    
    def openSettings(self):
        settings = SettingsDialog(parent=self, client=self.client)

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

    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
        self.ui.signupButton.clicked.connect(self.signup)
    
    def signup(self):
        username = self.ui.usernameLineEdit.text()
        name = self.ui.nameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if username and password and name:
            if self.client._connect():
                response = self.client.signup(username, name, password)
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

    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
        self.ui.loginButton.clicked.connect(self.login)

    def login(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        response = ''

        username = password = 'ade1'

        if username and password:
            response = self.client.login(username, password)
            msg = str(response)
        else: msg = 'All fields are required.'

        Msg(parent=self, text=msg)
        if response == RESPONSE.SUCCESSFUL: self._par.loginResponse(response)
    
    def showEvent(self, event=0): self._par.changeName('Login')

