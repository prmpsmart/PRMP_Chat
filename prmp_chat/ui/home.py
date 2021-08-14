
from .chat_ui import *

class MenuButton(QPushButton):
    def __init__(self, icon, tip):
        QPushButton.__init__(self)
        self.setIcon(QIcon(f':{icon}'))
        self.setToolTip(tip)


class Home(QFrame):

    def set_style(self):
        self.setStyleSheet(GET_STYLE())
        ...

    def __init__(self, app):
        QFrame.__init__(self)
        self.app = app
        self.client = LOAD()

        self.setWindowTitle('Mimi Peach')
        self.resize(1081, 602)

        self._layout = SETUP_FRAME(obj=self, margins=[5, 5, 5, 5], orient='h', space=5)

    # header
        header = QFrame()
        header.setStyleSheet('QFrame{background-color: red}')
        header.setMinimumHeight(25)
        header.setMaximumHeight(25)
        # self._layout.addWidget(header)

    # left
        left, left_layout = SETUP_FRAME(mother_layout=self._layout, re_obj=1)
        left.setMaximumWidth(35)
        
        menu_button = MenuButton(icon='home/menu.svg', tip='Menu')
        left_layout.addWidget(menu_button)

        contacts_button = MenuButton(icon='chat_list/user.svg', tip='New Contact')
        left_layout.addWidget(contacts_button)

        groups_button = MenuButton(icon='chat_list/users.svg', tip='New Group')
        left_layout.addWidget(groups_button)

        channels_button = MenuButton(icon='chat_list/user-group.svg', tip='New Channel')
        left_layout.addWidget(channels_button)

        left_layout.addSpacerItem(QSpacerItem(1, self.height()/2))

        setting_button = MenuButton(icon='home/settings.svg', tip='Setting')
        left_layout.addWidget(setting_button)
      
    # center
        center, center_layout = SETUP_FRAME(mother_layout=self._layout, re_obj=1, space=5, margins=[5, 5, 5, 5], orient='h')
        center.setStyleSheet('QFrame{background: white; border-radius: 10px}')

     # center view
        center_view, center_view_layout = SETUP_FRAME(mother_layout=center_layout, re_obj=1, space=10)
        
        center_view.setMinimumWidth(300)
        center_view.setMaximumWidth(350)

        self.search_edit = ChatLineEdit(parent=center_view, icon='chat_list/search.svg')
        self.search_edit.setPlaceholderText('Search People or Message')
        center_view_layout.addWidget(self.search_edit)

        self.center_tab = QTabWidget(center_view)
        center_view_layout.addWidget(self.center_tab)

        # self.all_frame = CREATE_TAB(self.center_tab, 'chat_list/globe-alt.svg', 'All')
        self.contact_frame = CREATE_TAB(self.center_tab, 'chat_list/user.svg', 'Contacts', ChatsList, kwargs=dict(client=self.client, callback=self.chat_picked))
        self.group_frame = CREATE_TAB(self.center_tab, 'chat_list/users.svg', 'Groups', ChatsList, kwargs=dict(client=self.client, attr='groups', callback=self.chat_picked))
        self.channel_frame = CREATE_TAB(self.center_tab, 'chat_list/user-group.svg', 'Channels', ChatsList, kwargs=dict(client=self.client, attr='channels', callback=self.chat_picked))

    # profile
        profile = ChatProfile(self)
        self._layout.addWidget(profile)

        self.chat_tab = ChatTab(self.client, profile, self.send_back)
        center_layout.addWidget(self.chat_tab)

        self.chat_tab.setMinimumWidth(450)
        self.chat_tab.setMaximumWidth(500)

        # self._cht_menu = IconButton(icon='chat_room/dots-vertical.svg', parent=self.chat_tab, icon_size=20)
        # self._cht_menu.setMaximumHeight(25)
    
    # footer
        footer = QFrame()
        footer.setStyleSheet('background-color: red')
        footer.setMinimumHeight(25)
        footer.setMaximumHeight(25)
        # self._layout.addWidget(footer)

        status_widget = QFrame(footer)
        
        
        self.set_style()
        self.setFixedSize(QSize(1213, 667))

        self.show()
        
    def centerWindow(self):
        size = self.size()
        a, b = size.width(), size.height()
        rect = self.app.screens()[0].availableGeometry()
        geo = QRect(int(rect.width()/2-a/2), int(rect.height()/2-b/2), a, b)
        self.setGeometry(geo)
    
    def showEvent(self, event):
        return
        w = self.chat_tab.width()
        self._cht_menu.setGeometry(w-30, 0, 30, 25)
    
    resizeEvent = showEvent
    
    def closeEvent(self, event=0): self.app.quit()

    def chat_picked(self, chat): self.chat_tab.add_chat_room(chat)

    def send_back(self, user):
        widget = None
        index = 0
        if isinstance(user, Contact): widget, index = self.contact_frame, 0
        elif isinstance(user, Group): widget, index = self.group_frame, 1
        elif isinstance(user, Channel): widget, index = self.channel_frame, 2
        else: return

        widget.set_current_object(user)
        self.center_tab.setCurrentIndex(index)


