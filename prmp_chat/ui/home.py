
from prmp_chat.new_ui.widgets import *

APP = QApplication([])


class Home(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app

        self.setWindowTitle('PRMP Chat')
        self.resize(881, 602)
        # self.setStyleSheet('background-color: red')

        self._layout = SETUP_FRAME(obj=self)

    # header
        header = QFrame()
        header.setStyleSheet('background-color: red')
        header.setMinimumHeight(25)
        header.setMaximumHeight(25)
        self._layout.addWidget(header)

    # body
        body_layout = SETUP_FRAME(mother_layout=self._layout, v=0)
    
     # left side
        left_side, left_side_layout = SETUP_FRAME(mother_layout=body_layout, re_obj=1)
        left_side.setMaximumWidth(380)

        self.user_name = QPushButton()
        self.user_name.setText('PRMP Smart')
        left_side_layout.addWidget(self.user_name)

      # inside left
        inside_left_layout = SETUP_FRAME(mother_layout=left_side_layout, v=0)
        

      # left_bar
        left_bar, left_bar_layout = SETUP_FRAME(mother_layout=inside_left_layout, re_obj=1)
        left_bar.setMaximumWidth(60)

        menu_button = QPushButton(left_bar)
        menu_button.setText('Menu')
        left_bar_layout.addWidget(menu_button)

        contacts_button = QPushButton(left_bar)
        contacts_button.setText('New C')
        left_bar_layout.addWidget(contacts_button)

        groups_button = QPushButton(left_bar)
        groups_button.setText('New G')
        left_bar_layout.addWidget(groups_button)

        channels_button = QPushButton(left_bar)
        channels_button.setText('New Ch')
        left_bar_layout.addWidget(channels_button)

        left_bar_layout.addSpacerItem(QSpacerItem(1, self.height()/2))

        setting_button = QPushButton(left_bar)
        setting_button.setText('Setting')
        left_bar_layout.addWidget(setting_button)
      
      # left view
        left_view, left_view_layout = SETUP_FRAME(mother_layout=inside_left_layout, re_obj=1)
        self.search_edit = QLineEdit(left_view)
        self.search_edit.setPlaceholderText('Search People or Message')
        left_view_layout.addWidget(self.search_edit)

        self.left_tab = QTabWidget(left_view)
        left_view_layout.addWidget(self.left_tab)

        self.all_frame = CREATE_TAB(self.left_tab, 'All')
        self.contact_frame = CREATE_TAB(self.left_tab, 'Contacts')
        self.group_frame = CREATE_TAB(self.left_tab, 'Groups')
        self.channel_frame = CREATE_TAB(self.left_tab, 'Channels')
     
     # right side
        right_side, right_side_layout = SETUP_FRAME(mother_layout=body_layout, re_obj=1)
        
        self.right_tab = ChatRoomsTab(right_side)
     
        self.show()
        return

# chat_list
        chat_list_frame = QFrame()
        chat_list_frame.setStyleSheet('background-color: orange')
        chat_list_frame.setMinimumWidth(280)
        chat_list_frame.setMaximumWidth(280)
        body_layout.addWidget(chat_list_frame)

        chat_list_frame_layout = QVBoxLayout(chat_list_frame)
        chat_list_frame_layout.setContentsMargins(2, 2, 2, 2)
        chat_list_frame_layout.setSpacing(2)

        search_frame = QFrame()
        search_frame.setStyleSheet('background-color: green')
        search_frame.setMaximumHeight(40)
        chat_list_frame_layout.addWidget(search_frame)

        chat_list_label = QLabel()
        chat_list_label.setText('Chat List')
        chat_list_label.setStyleSheet('background-color: grey')
        chat_list_label.setAlignment(Qt.AlignCenter)
        chat_list_frame_layout.addWidget(chat_list_label)
    
     # chatting
        self._cht = chatting_frame = QFrame()
        chatting_frame_layout = QVBoxLayout(chatting_frame)
        chatting_frame_layout.setSpacing(0)
        chatting_frame_layout.setContentsMargins(0, 0, 0, 0)
        chatting_frame.setStyleSheet('background-color: pink')
        body_layout.addWidget(chatting_frame)

        chats_tab = QTabWidget()
        # chats_tab.setMaximumSize(200, 200)
        chatting_frame_layout.addWidget(chats_tab)

        for a in range(1, 5): chats_tab.addTab(QFrame(), f'Test {a}')

        self._cht_menu = QPushButton(chats_tab)
        self._cht_menu.setText('M')


    # footer
        footer = QFrame()
        footer.setStyleSheet('background-color: red')
        footer.setMinimumHeight(25)
        footer.setMaximumHeight(25)
        self._layout.addWidget(footer)

        status_widget = QFrame(footer)
        

        self.show()
    
    def centerWindow(self):
        size = self.size()
        a, b = size.width(), size.height()
        rect = self.app.screens()[0].availableGeometry()
        geo = QRect(int(rect.width()/2-a/2), int(rect.height()/2-b/2), a, b)
        self.setGeometry(geo)
    
    def showEvent(self, event):
        return
        w = self._cht.width()
        self._cht_menu.setGeometry(w-30, 0, 30, 25)
    
    def resizeEvent(self, event):
        self.showEvent(event)
    
    def closeEvent(self, event=0): self.app.quit()








window = Home(app=APP)



APP.exec_()

