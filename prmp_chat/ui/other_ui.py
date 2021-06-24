from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow, QWidget
from designer.chat_menu_dialog import *
from designer.home import Ui_PRMPChat

from designer.new_contact import Ui_NewContactDialog
from designer.new_group import Ui_NewGroupDialog
from designer.new_channel import Ui_NewChannelDialog
from designer.settings import Ui_SettingsDialog
from designer.side_dialog import Ui_SideDialog


class Popups:
    
    def closeEvent(self, event=0):
        if not self.parent(): self.app.quit()


class ChatMenu(Popups, QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent, f=Qt.Popup)

        self.ui = Ui_ChatMenu()
        self.ui.setupUi(self)

        # flags = Qt.Popup# | Qt.FramelessWindowHint


class News(Popups):
    def __init__(self):
        self.ui.cancelButton.clicked.connect(self.close)


class NewContact(News, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, Qt.Popup)
        
        self.ui = Ui_NewContactDialog()
        self.ui.setupUi(self)
        
        News.__init__(self)


class NewGroup(News, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, Qt.Popup)
        
        self.ui = Ui_NewGroupDialog()
        self.ui.setupUi(self)
        
        News.__init__(self)


class NewChannel(News, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, Qt.Popup)
        
        self.ui = Ui_NewChannelDialog()
        self.ui.setupUi(self)
        
        News.__init__(self)


class SettingsDialog(Popups, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, Qt.Popup)
        
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)


class SideDialog(Popups, QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, Qt.Popup)
        
        self.ui = Ui_SideDialog()
        self.ui.setupUi(self)
        
        self.ui.newContactButton.clicked.connect(self.openNewContact)
        self.ui.newGroupButton.clicked.connect(self.openNewGroup)
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        
        self.ui.newChannelButton.clicked.connect(self.openNewChannel)
        self.ui.settingsButton.clicked.connect(self.openSettings)

    
    def openNewContact(self):
        newContact = NewContact(self)

        pos = self.pos()
        geo = self.ui.newContactButton.geometry()

        newContact.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newContact.show()
    
    def openNewGroup(self):
        newGroup = NewGroup(self)

        pos = self.pos()
        geo = self.ui.newGroupButton.geometry()

        newGroup.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newGroup.show()
    
    def openNewChannel(self):
        newChannel = NewChannel(self)

        pos = self.pos()
        geo = self.ui.newChannelButton.geometry()

        newChannel.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newChannel.show()
    
    def openSettings(self):
        settings = SettingsDialog(self)

        pos = self.pos()
        geo = self.geometry()

        settings.move(pos.x()+geo.width()+10, pos.y())
        settings.show()

