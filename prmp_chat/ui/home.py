
from .chat_ui import *
from .popups import *


MASK = 1


class Label(QLabel):

    def __init__(self, ps=0, bold=0, underline=0, layout=None):
        super().__init__()

        font = QFont()
        font.setFamily('Times New Roman')
        if ps:  font.setPointSize(ps)
        if underline: font.setUnderline(True)
        if bold: font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)
        if layout: layout.addWidget(self, Qt.AlignCenter)


class Profile(QFrame):

    def __init__(self, user: User):
        super().__init__()
        
        self.user = user
        self.setStyleSheet('background: %s'%STYLE.LIGHT_SHADE)
        self.setMaximumHeight(250)

        layout = SETUP_FRAME(obj=self)

        self.icon_button = IconButton()
        self.icon_button.setMaximumHeight(200)
        layout.addWidget(self.icon_button)

        self.name = Label(ps=14, underline=1, layout=layout)

        self.username = Label(ps=11, bold=1, layout=layout)

        self.last_login = Label(ps=10, layout=layout)
        layout.addWidget(self.last_login)

    def showEvent(self, e):
        icon = self.user.icon
        if icon:
            if MASK: icon = GET_ICON(self.user.icon, size=200)
            else: icon = QIcon(QPixmap(QImage().fromData(b64decode(self.user.icon))))
            self.icon_button.setIcon(icon)
        self.update_details()
    
    def update_details(self):
        self.name.setText(self.user.name)
        self.username.setText(self.user.id)
        if self.user.status == STATUS.ONLINE: text = str(STATUS.ONLINE)
        else: text = self.user.last_seen.toString(OFFLINE_FORMAT)
        self.last_login.setText(text)
    
    # def resizeEvent(self, event):


class SideBar(QFrame):

    def __init__(self, user, parent):
        super().__init__(parent)
        self.user = user

        self.minw = 45
        self.maxw = 260
        
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

        self._layout = SETUP_FRAME(obj=self, space=2, margins=[5, 5, 5, 5])

        # setup profile
        
        self.profile = Profile(user)
        self._layout.addWidget(self.profile)

        self.menu_button = MenuButton(self.parent(), icon='home/menu-2.svg', tip='Menu', user=self.user, action=self.action)
        self._layout.addWidget(self.menu_button)

        self.contacts_button = MenuButton(self.parent(), icon='home/user-plus.svg', tip='New Contact', user=self.user, window=NewContactDialog)
        self._layout.addWidget(self.contacts_button)

        self.groups_button = MenuButton(self.parent(), icon='home/users.svg', tip='New Group', user=self.user, window=NewGroupDialog)
        self._layout.addWidget(self.groups_button)

        self.channels_button = MenuButton(self.parent(), icon='home/video-plus.svg', tip='New Channel', user=self.user, window=NewChannelDialog)
        self._layout.addWidget(self.channels_button)

        self.setting_button = MenuButton(self.parent(), icon='home/settings.svg', tip='Setting', user=self.user, window=SettingsDialog)
        self._layout.addWidget(self.setting_button)

        self.spacer = QSpacerItem(1, 300, QSizePolicy.MinimumExpanding)
        self._layout.addItem(self.spacer)

        self._menus = [self.menu_button, self.contacts_button, self.groups_button, self.channels_button, self.setting_button]

        self.enlarged = 1
        self.action()

    def action(self):
        if self.enlarged: self._hide()
        else: self._show()
    
    def _hide(self):
        self.profile.hide()
        self.spacer.changeSize(1, 300)
        self.enlarged = 0
        self.setMinimumWidth(self.minw)
        self.setMaximumWidth(self.minw)

        for a in self._menus: a._hide()
        self.resizeParent(0)

    def _show(self):
        self.enlarged = 1
        self.spacer.changeSize(1, 200)
        self.setMinimumWidth(self.maxw)
        self.setMaximumWidth(self.maxw)
        self.profile.show()

        for a in self._menus: a._show()
        self.resizeParent(1)

    def resizeParent(self, s):
        par = self.parent()

        if par._size:

            geo = par.size()
            geo1 = self.size()
            
            x, y = par._size.toTuple()
            if s: x += self.maxw - self.minw
            
            gg = par.geometry()
            g = [getattr(gg, a)() for a in ['x', 'y', 'width', 'height']]
            g[2] = x

            par.setGeometry(*g)
            par.centerWindow()


class Header(QFrame):

    def __init__(self, parent, h=30):
        super().__init__(parent)
        hlay = SETUP_FRAME(obj=self, orient='h', margins=[2, 2, 2, 2])
        
        hlay.addItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        
        self.title = QLabel()
        self.title.setText('Mimi Peach')
        font = QFont()
        font.setFamilies(['Times New Roman'])
        font.setPointSize(23)
        font.setBold(True)
        font.setItalic(False)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        hlay.addWidget(self.title)

        hlay.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.status = QLabel()
        self.status.setMinimumWidth(100)
        self.status.setMaximumWidth(100)
        font = QFont()
        font.setFamilies(['Hobo Std'])
        font.setPointSize(16)
        font.setBold(True)
        self.status.setFont(font)
        self.status.setAlignment(Qt.AlignCenter)
        self.set_offline()
        hlay.addWidget(self.status)
        
        hlay.addItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        _min = MenuButton(icon='home/minus.svg', tip='Minimize')
        hlay.addWidget(_min)
        _max = MenuButton(icon='home/rectangle.svg', tip='Maximize')
        hlay.addWidget(_max)
        _exit = MenuButton(icon='home/x.svg', tip='Exit')
        hlay.addWidget(_exit)

        self.setStyleSheet('''
            QFrame {
                border: 5px; 
                background-color: white;
                }
            MenuButton {
                border: 0px;
                background-color: %s;
                text-align: center
                }
            MenuButton::hover {
                background-color: %s
                }
            MenuButton::pressed {
                background-color: %s
                }

            '''
            %
            (STYLE.LIGHT, STYLE.LIGHT_SHADE, STYLE.DARK)
            )
        
        self.setMinimumHeight(h+5)
        self.setMaximumHeight(h+5)

    def set_online(self):
        self.status.setText('ONLINE')
        self.status.setStyleSheet('background: qlineargradient(spread:pad, x1:0.683616, y1:0.477, x2:1, y2:1, stop:0.587571 rgba(3, 146, 52, 255), stop:0.847458 rgba(255, 255, 255, 255));\ncolor: white;')

    def set_offline(self):
        self.status.setText('OFFLINE')
        self.status.setStyleSheet('background: qlineargradient(spread:pad, x1:0.585, y1:0.818136, x2:0.614, y2:1, stop:0.147727 red, stop:0.431818 rgba(146, 100, 136, 255), stop:0.880682 rgba(246, 184, 233, 255));\ncolor: white;')


class Thread(QThread):

    def __init__(self, parent, function):
        super().__init__(parent)
        self.function = function

    def run(self): self.function()


class Backend_Hook:

    def __init__(self, user=None):
        self.user: User = user or LOAD()
        self.client = Client(user=self.user, relogin=1, LOG=self.logit)

        self._recv_status = None
        self._change_status = None

        self.user_hooks()
        self.client_hooks()
    
        self.login_thread = Thread(self, self.login)

    def login(self):
        if self.user: self.client.re_login(start=1)

    def logit(self, *args, **kwargs):
        # print(*args, **kwargs)
        ...

    def user_hooks(self):
       # status
        self._change_status = self.user.change_status
        self.user.change_status = self.change_status

    def client_hooks(self):
        self._recv_status = self.client.recv_status
        self.client.recv_status = self.recv_status

    def recv_status(self, tag):
        self._recv_status(tag)
        print(tag)
        self.update_chatlists()

    def change_status(self, status):
        self._change_status(status)
        if status == STATUS.ONLINE: self.header.set_online()
        else: self.header.set_offline()
        self.side_bar.profile.update_details()

    def remove_user_hooks(self):
        self.user.change_status = self._change_status

    def remove_client_hooks(self):
        ...

    def remove_hooks(self):
        self.remove_user_hooks()
        self.remove_client_hooks()

    def close(self):
        self.login_thread.quit()
        self.client.stop()
        self.remove_hooks()
        SAVE(self.user)


class Home(QFrame, Backend_Hook):

    def set_style(self):
        self.setStyleSheet(GET_STYLE())
    
    def __init__(self, app, user=None):
        QFrame.__init__(self)
        Backend_Hook.__init__(self, user)

        self.app = app
        self._size = None
        self.setup()
        self.setWindowTitle('Mimi Peach')
        self.set_style()
        self.setMinimumSize(QSize(1213, 717))
        self.centerWindow()

        self.login_thread.start()

        self.show()
    
    def setup(self):
        
        vlayout = SETUP_FRAME(obj=self)

     #  header
        self.header = Header(self)
        vlayout.addWidget(self.header)

        hlayout = SETUP_FRAME(klass=None, margins=[0, 2, 0, 2], orient='h', space=5)
        vlayout.addLayout(hlayout)

     # left
        self.side_bar = SideBar(user=self.user, parent=self)
        hlayout.addWidget(self.side_bar)
      
     # center
        center, center_layout = SETUP_FRAME(mother_layout=hlayout, re_obj=1, space=5, margins=[5, 5, 5, 5], orient='h')
        center.setStyleSheet('QFrame{background: white; border-radius: 10px}')

      # center view
        center_view, center_view_layout = SETUP_FRAME(mother_layout=center_layout, re_obj=1, space=10)
        
        center_view.setMinimumWidth(300)
        center_view.setMaximumWidth(350)

        self.search_edit = ChatLineEdit(parent=center_view, icon='chat_list/search.svg')
        self.search_edit.keyReleaseEvent = self._keyReleaseEvent
        self.search_edit.setPlaceholderText('Search People or Message')
        center_view_layout.addWidget(self.search_edit)

        self.center_tab = QTabWidget(center_view)
        center_view_layout.addWidget(self.center_tab)

        self.contact_frame = CREATE_TAB(self.center_tab, 'chat_list/user.svg', 'Contacts', ChatsList, kwargs=dict(user=self.user, callback=self.chat_picked))
        self.group_frame = CREATE_TAB(self.center_tab, 'chat_list/users.svg', 'Groups', ChatsList, kwargs=dict(user=self.user, attr='groups', callback=self.chat_picked))
        self.channel_frame = CREATE_TAB(self.center_tab, 'chat_list/user-group.svg', 'Channels', ChatsList, kwargs=dict(user=self.user, attr='channels', callback=self.chat_picked))
        self.search_frame = CREATE_TAB(self.center_tab, 'chat_list/list-search.svg', 'Searched', SearchList, kwargs=dict(user=self.user, attr='', callback=self.chat_picked))

     # profile
        profile = ChatProfile(self)
        hlayout.addWidget(profile)
     
     # chat
        self.chat_tab = ChatTab(self.client, profile, self.send_back)
        center_layout.addWidget(self.chat_tab)

        self.chat_tab.setMinimumWidth(450)
    
     # footer
        # self.footer = QFrame()
        # self.footer.setStyleSheet('background-color: red')
        # self.footer.setMinimumHeight(25)
        # self.footer.setMaximumHeight(25)
        # vlayout.addWidget(self.footer)

    def _keyReleaseEvent(self, event):
        self.center_tab.setCurrentIndex(3)

        typed = self.search_edit.text().lower()
        self.search_frame.search(typed)

    def centerWindow(self): self.move(QApplication.primaryScreen().availableGeometry().center()-self.rect().center())
    
    def showEvent(self, event):
        if not self._size: self._size = self.size()
    
    resizeEvent = showEvent
    
    def closeEvent(self, event=0):
        Backend_Hook.close(self)
        self.app.quit()

    def chat_picked(self, chat):
        self.chat_tab.add_chat_room(chat)

    def send_back(self, user):
        widget = None
        index = 0
        if isinstance(user, Contact): widget, index = self.contact_frame, 0
        elif isinstance(user, Group): widget, index = self.group_frame, 1
        elif isinstance(user, Channel): widget, index = self.channel_frame, 2
        else: return

        widget.set_current_object(user)
        self.center_tab.setCurrentIndex(index)

    def update_chatlists(self):
        self.center_tab.currentWidget().update_statuses()
        self.chat_tab.currentWidget().header.update_()


