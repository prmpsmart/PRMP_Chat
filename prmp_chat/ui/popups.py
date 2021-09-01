from prmp_chat.ui.chat_ui.chat_listing import IconButton
from .widgets import *




def _cancel_next(parent, first, next):
    horizontalLayout = QHBoxLayout()
    horizontalLayout.setContentsMargins(0, 0, 0, 0)

    cancel_button = MenuButton(parent, icon='home/x.svg', tip='Cancel', action=lambda: parent.close())

    next_button = MenuButton(parent, icon='home/player-play.svg', tip='Next', action=next)

    for button in [cancel_button, next_button]:
        button.setMinimumSize(QSize(50, 40))
        button.setMaximumSize(QSize(50, 40))
        horizontalLayout.addWidget(button)
    
    first.addLayout(horizontalLayout)




class Popups(ChatWindow):
    def __init__(self, **kwargs):
        ChatWindow.__init__(self, flag=Qt.Popup, **kwargs)



class NewContactDialog(Popups):

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.name = QLineEdit()
        layout.addWidget(self.name)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setPlaceholderText('Contact Name')
        self.name.setClearButtonEnabled(True)

        _cancel_next(self, layout, self.next)

    def next(self): ...


class NewGroupDialog(Popups):
    
    def setup_ui(self):
        self.resize(350, 200)
        self.setMinimumSize(QSize(350, 200))
        self.setMaximumSize(QSize(350, 200))
        
        self.icon = ImageButton(parent=self, icon='chat_list/user-circle.svg')
        self.icon.setGeometry(QRect(10, 10, 80, 80))

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

        widget, layout = SETUP_FRAME(re_obj=1, parent=self)
        widget.setGeometry(QRect(190, 150, 131, 42))

        _cancel_next(self, layout, self.next)
        widget.setStyleSheet('''
            QFrame {
                background: %s
                }'''
                %
                STYLE.LIGHT_SHADE
            )

    def next(self): ...


class NewChannelDialog(Popups):
    
    def setup_ui(self):
        self.resize(350, 200)
        self.setMinimumSize(QSize(350, 200))
        self.setMaximumSize(QSize(350, 200))
        
        self.icon = ImageButton(parent=self, icon='chat_list/user-circle.svg')
        self.icon.setGeometry(QRect(10, 10, 80, 80))

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

        widget, layout = SETUP_FRAME(re_obj=1, parent=self)
        widget.setGeometry(QRect(190, 150, 131, 42))

        _cancel_next(self, layout, self.next)
        widget.setStyleSheet('''
            QFrame {
                background: %s
                }'''
                %
                STYLE.LIGHT_SHADE
            )

    def next(self): ...


class ProfileDialog(Popups):
    
    def setup_ui(self):
        self.resize(350, 200)
        self.setMinimumSize(QSize(350, 200))
        self.setMaximumSize(QSize(350, 200))
        
        self.icon = IconButton(parent=self, icon=self.client.icon)
        self.icon.setGeometry(QRect(10, 10, 80, 80))

        self.name = QLineEdit(self)
        self.name.setGeometry(QRect(100, 20, 242, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setPlaceholderText('Name')
        self.name.setClearButtonEnabled(True)
        self.name.setText(self.client.name)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        self.username.setGeometry(QRect(100, 60, 242, 30))
        self.username.setClearButtonEnabled(True)
        self.username.setText(self.client.id)


        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setGeometry(QRect(100, 100, 242, 30))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setClearButtonEnabled(True)
        self.password.setText(self.client.key)

        widget, layout = SETUP_FRAME(re_obj=1)
        widget.setGeometry(QRect(190, 150, 131, 42))

        _cancel_next(self, layout, self.next)

    def next(self): ...


class SettingsDialog(Popups):
    
    def setup_ui(self):
        self.resize(176, 222)
        self.setMaximumSize(QSize(278, 411))
                
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


