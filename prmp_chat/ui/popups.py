from .widgets import *


def _cancel_next(parent, first, next):
    horizontalLayout = QHBoxLayout(first)
    horizontalLayout.setContentsMargins(0, 0, 0, 0)

    cancel_button = QPushButton()
    cancel_button.setText('Cancel')
    cancel_button.clicked.connect(lambda: parent.close())
    cancel_button.clicked.connect(lambda: parent.close())

    next_button = QPushButton()
    next_button.setText('Next')
    next_button.clicked.connect(next)

    for button in [cancel_button, next_button]:
        button.setMinimumSize(QSize(50, 40))
        button.setMaximumSize(QSize(50, 40))
        horizontalLayout.addWidget(button)





class NewContactDialog(Popups):
    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)

    def setup_ui(self):
        self.setStyleSheet(NORMAL_STYLE)

        layout = QVBoxLayout(self)


        self.name = QLineEdit()
        layout.addWidget(self.name)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setPlaceholderText('Contact Name')
        self.name.setClearButtonEnabled(True)

        layoutWidget = QFrame()

        _cancel_next(self, layoutWidget, self.next)

        layout.addWidget(layoutWidget)

    def next(self): ...


class NewGroupDialog(Popups):
    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
    
    def setup_ui(self):
        self.resize(350, 200)
        self.setMinimumSize(QSize(350, 200))
        self.setMaximumSize(QSize(350, 200))
        self.setStyleSheet(NORMAL_STYLE)

        self.icon = QPushButton(self)
        self.icon.setText('Image')
        self.icon.setGeometry(QRect(10, 10, 80, 80))
        self.icon.setStyleSheet(BUTTON_ICON)

        self.icon.setAutoDefault(False)
        self.icon.setFlat(False)

        self.name = QLineEdit(self)
        self.name.setGeometry(QRect(100, 20, 242, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setPlaceholderText('Group Name')
        self.name.setClearButtonEnabled(True)

        self.description = QTextEdit(self)
        self.description.setPlaceholderText('Group discription')
        self.description.setGeometry(QRect(100, 60, 241, 81))

        layoutWidget = QWidget(self)
        layoutWidget.setGeometry(QRect(190, 150, 131, 42))

        _cancel_next(self, layoutWidget, self.next)

    def next(self): ...


class NewChannelDialog(Popups):
    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
    
    def setup_ui(self):
        self.resize(350, 200)
        self.setMinimumSize(QSize(350, 200))
        self.setMaximumSize(QSize(350, 200))
        self.setStyleSheet(NORMAL_STYLE)

        self.icon = QPushButton(self)
        self.icon.setText('Image')
        self.icon.setGeometry(QRect(10, 10, 80, 80))
        self.icon.setStyleSheet(BUTTON_ICON)

        self.icon.setAutoDefault(False)
        self.icon.setFlat(False)

        self.name = QLineEdit(self)
        self.name.setGeometry(QRect(100, 20, 242, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setPlaceholderText('Channel Name')
        self.name.setClearButtonEnabled(True)

        self.description = QTextEdit(self)
        self.description.setPlaceholderText('Channel discription')
        self.description.setGeometry(QRect(100, 60, 241, 81))

        layoutWidget = QWidget(self)
        layoutWidget.setGeometry(QRect(190, 150, 131, 42))

        _cancel_next(self, layoutWidget, self.next)

    def next(self): ...


class ProfileDialog(Popups):
    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
    
    def setup_ui(self):
        self.resize(350, 200)
        self.setMinimumSize(QSize(350, 200))
        self.setMaximumSize(QSize(350, 200))
        self.setStyleSheet(NORMAL_STYLE)

        self.icon = QPushButton(self)
        self.icon.setText('Image')
        self.icon.setGeometry(QRect(10, 10, 80, 80))
        self.icon.setStyleSheet(BUTTON_ICON)

        self.icon.setAutoDefault(False)
        self.icon.setFlat(False)

        self.name = QLineEdit(self)
        self.name.setGeometry(QRect(100, 20, 242, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setPlaceholderText('Name')
        self.name.setClearButtonEnabled(True)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        self.username.setGeometry(QRect(100, 60, 242, 30))
        self.username.setClearButtonEnabled(True)
        self.username.setClearButtonEnabled(True)


        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setGeometry(QRect(100, 100, 242, 30))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setClearButtonEnabled(True)

        layoutWidget = QWidget(self)
        layoutWidget.setGeometry(QRect(190, 150, 131, 42))

        _cancel_next(self, layoutWidget, self.next)

    def next(self): ...


class SettingsDialog(Popups):
    def __init__(self, **kwargs):
        Popups.__init__(self, **kwargs)
    
    def setup_ui(self):
        self.resize(176, 222)
        self.setMaximumSize(QSize(278, 411))
        self.setStyleSheet(NORMAL_STYLE)
        
        layout = QVBoxLayout(self)

        self.edit_button = QPushButton(self)
        self.edit_button.setText('Edit Profile')
        self.edit_button.setMinimumSize(QSize(0, 40))
        self.edit_button.setLayoutDirection(Qt.LeftToRight)
        self.edit_button.clicked.connect(self.open_profile)

        layout.addWidget(self.edit_button)

        download_path = QPushButton(self)
        download_path.setText('Download Path')
        download_path.setMinimumSize(QSize(0, 40))
        download_path.setMaximumSize(QSize(16777215, 40))

        layout.addWidget(download_path)

        chat_settings = QPushButton(self)
        chat_settings.setText('Chat Settings')
        chat_settings.setMinimumSize(QSize(0, 40))

        layout.addWidget(chat_settings)

        advance_settings = QPushButton(self)
        advance_settings.setText('Advance Settings')
        advance_settings.setMinimumSize(QSize(0, 40))

        layout.addWidget(advance_settings)

    def open_profile(self):
        profile = ProfileDialog(parent=self, client=self.client)

        pos = self.pos()
        geo = self.edit_button.geometry()

        profile.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        profile.show()


class SideDialog(Chat_Ui):
    def __init__(self, client=None):
        Chat_Ui.__init__(self, client=client)

    def setup_ui(self):
        self.resize(303, 334)
        self.setMinimumSize(QSize(200, 0))
        self.setMaximumSize(QSize(350, 384))
        self.setStyleSheet(NORMAL_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame(self)
        frame.setMinimumSize(QSize(260, 130))
        frame.setMaximumSize(QSize(16777215, 150))
        
        edit_button = QPushButton(frame)
        edit_button.setGeometry(QRect(240, 90, 40, 30))
        edit_button.setText("Edit")
        edit_button.clicked.connect(self.open_settings)


        self.icon_button = QPushButton(frame)
        self.icon_button.setGeometry(QRect(10, 10, 80, 80))
        self.icon_button.setText("Image")
        self.icon_button.setStyleSheet(BUTTON_ICON)

        self.last_login = QLabel(frame)
        self.last_login.setGeometry(QRect(100, 60, 181, 21))
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(10)
        self.last_login.setFont(font)
        self.last_login.setText("last login 2021/06/25 at 06:11 PM")

        self.name = QLabel(frame)
        self.name.setGeometry(QRect(100, 10, 171, 31))
        font1 = QFont()
        font1.setFamily(u"Times New Roman")
        font1.setPointSize(14)
        font1.setUnderline(True)
        self.name.setFont(font1)
        self.name.setText("Apata Miracle Peter")

        self.username = QLabel(frame)
        self.username.setGeometry(QRect(100, 40, 141, 21))
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        font2.setPointSize(11)
        font2.setBold(True)
        self.username.setFont(font2)
        self.username.setText("prmpsmart")

        layout.addWidget(frame)

        layout_2 = QVBoxLayout()
        layout_2.setSpacing(5)
        layout_2.setContentsMargins(20, 4, 20, 4)
        self.contact_button = QPushButton(self)
        self.contact_button.setMinimumSize(QSize(0, 40))
        self.contact_button.setLayoutDirection(Qt.LeftToRight)
        self.contact_button.setFlat(True)
        self.contact_button.setText("New Contact")
        self.contact_button.clicked.connect(self.show_new_contact)

        layout_2.addWidget(self.contact_button)

        self.group_button = QPushButton(self)
        self.group_button.setMinimumSize(QSize(0, 40))
        self.group_button.setFlat(True)
        self.group_button.setText("New Group")
        self.group_button.clicked.connect(self.show_new_group)

        layout_2.addWidget(self.group_button)

        self.channel_button = QPushButton(self)
        self.channel_button.setMinimumSize(QSize(0, 40))
        self.channel_button.setFlat(True)
        self.channel_button.setText("New Channel")
        self.channel_button.clicked.connect(self.show_new_channel)

        layout_2.addWidget(self.channel_button)


        layout.addLayout(layout_2)

        copyright = QPlainTextEdit(self)
        copyright.setMinimumSize(QSize(0, 40))
        copyright.setMaximumSize(QSize(16777215, 40))
        font3 = QFont()
        font3.setFamily(u"Times New Roman")
        font3.setPointSize(16)
        font3.setBold(True)
        font3.setUnderline(True)
        copyright.setFont(font3)
        copyright.setFrameShape(QFrame.NoFrame)
        copyright.setPlainText("   PRMP Chat by PRMPSmart   ")

        layout.addWidget(copyright)
    
    def show_new_contact(self):
        newContact = NewContactDialog(client=self.client, parent=self)

        pos = self.pos()
        geo = self.contact_button.geometry()

        newContact.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newContact.show()
    
    def show_new_group(self):
        newGroup = NewGroupDialog(client=self.client, parent=self)

        pos = self.pos()
        geo = self.group_button.geometry()

        newGroup.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newGroup.show()
    
    def show_new_channel(self):
        newChannel = NewChannelDialog(parent=self, client=self.client)

        pos = self.pos()
        geo = self.channel_button.geometry()

        newChannel.move(pos.x()+geo.width()+10, pos.y()+geo.y())
        newChannel.show()
    
    def open_settings(self):
        settings = SettingsDialog(client=self.client, parent=self)

        pos = self.pos()
        geo = self.geometry()

        settings.move(pos.x()+geo.width()+10, pos.y())
        settings.show()
        settings.show()





APP = QApplication([])
window = SideDialog()
window.show()
APP.exec_()
