from .chat_listing import *
from .chat_room import *


class ChatProfile(QFrame):

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.setMinimumWidth(300)
        self.setMaximumWidth(300)
        self.setStyleSheet('''
            QFrame {
                background: %s;
                border-radius: 15px
                }
            QLabel {
                color: %s
                }
            '''
            %
            (STYLE.LIGHT, STYLE.DARK)
            )

        layout = SETUP_FRAME(obj=self, margins=[5, 0, 5, 5], space=5)

        details_layout = SETUP_FRAME(layout)

        icon_frame, icon_layout = SETUP_FRAME(details_layout, re_obj=1, margins=[10, 5, 10, 0])
        icon_layout.setAlignment(Qt.AlignHCenter)
        r = 120

        self.icon = IconButton(icon='chat_list/user-circle.svg', size=r)
        icon_layout.addWidget(self.icon)

        icon_frame.setMinimumHeight(r)
        
        self.name = QLabel()
        font = QFont()
        font.setFamily('Times New Roman')
        font.setBold(1)
        font.setPointSizeF(14)
        self.name.setFont(font)
        self.n_fm = QFontMetrics(font)
        details_layout.addWidget(self.name)

        self.username = QLabel()
        font = QFont()
        font.setPointSizeF(9)
        self.username.setFont(font)
        self.u_fm = QFontMetrics(font)
        details_layout.addWidget(self.username)

        media = QFrame()
        media.setStyleSheet('background: %s'%STYLE.LIGHT_SHADE)
        media.setMinimumHeight(400)
        media.setStyleSheet('background: url(:chat_room/wallpaper14.png) center')

        layout.addWidget(media)

        self.block = Icon2Button('profile/message-circle-off.svg', '')
        layout.addWidget(self.block)

        self.report = Icon2Button('profile/thumb-down.svg', '')
        layout.addWidget(self.report)

    def update_user(self, user: Base):
        icon = user.icon
        name = user.name
        username = user.id

        if icon: self.icon.set_icon(icon)
        else: self.icon.set_icon('chat_list/user-circle.svg')

        self.name.setText(name)
        
        br = self.n_fm.boundingRect(name)
        self.name.setText(name)
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setMinimumHeight(br.height()+5)
        self.name.setMaximumHeight(br.height()+5)

        br = self.u_fm.boundingRect(username)
        self.username.setText(username)
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setMinimumHeight(br.height()+5)
        self.username.setMaximumHeight(br.height()+5)

        _type = 'Report ' + user.className

        self.block.setText(_type)
        self.report.setText(_type)

