

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class LineEditWithButton(QLineEdit):
    buttonClicked = Signal()

    def __init__(self, icon_file, parent=None, completer=False, default_values=[], completer_sense=Qt.CaseInsensitive, callback=None):
        QLineEdit.__init__(self, parent)

        self.default_values = default_values
        self.completer_sense = completer_sense
        self.callback = callback
        
        if completer or default_values: self.set_completer(default_values, completer_sense)

        self.button = QToolButton(self)
        self.button.setIcon(QIcon(icon_file))
        self.button.setToolTip('Go')
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(Qt.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)
        self.returnPressed.connect(self.button.click)
        self.buttonClicked.connect(self.call_callback)


        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('.QLineEdit {padding-right: %dpx;}' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2), max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))
    
    def call_callback(self):
        if self.callback: self.callback(self.text())
    
    def set_completer(self, default_values=[], completer_sense=Qt.CaseInsensitive):
        self.default_values = default_values or self.default_values
        self.completer_sense = completer_sense

        completer = QCompleter(self.default_values)
        completer.setCaseSensitivity(self.completer_sense)
        self.setCompleter(completer)

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)

        self.button.move(self.rect().right() - frameWidth - buttonSize.width(), (self.rect().bottom() - buttonSize.height() + 1)/2)
        QLineEdit.resizeEvent(self, event)
    
    def clear_default_values(self): self.default_values = []

    def add_default_value(self, value): self.default_values.append(value)


class ChatObjectWidget(QFrame):
    def __init__(self, name_hook, alias, lastseen, access):
        QFrame.__init__(self)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setFixedSize(233, 90)
        self._style_me()
        self.setLayout(self.layout)
        self.name_hook = name_hook
        self.render(alias, lastseen, access)

    def mouseReleaseEvent(self, event):
        self.name_hook(self.alias)

    def _style_me(self): self.setStyleSheet('ChatObjectWidget{border-radius: 10px; background-color: #dadada;}ChatObjectWidget::hover{background-color: #a0a0a0;}')

    def blink(self):
        self.setStyleSheet('ChatObjectWidget{border-radius: 10px; background-color: #a0a0a0;}')
        QTimer.singleShot(150, self._style_me)

    def render(self, alias, lastseen, access):
        self.alias = alias
        self.setToolTip('{0} >> {1}'.format(alias, access))
        layout2 = QHBoxLayout()
        layout2.setContentsMargins(10, 10, 0, 0)
        layout2.setSpacing(0)
        layout3 = QHBoxLayout()
        layout3.setContentsMargins(0, 0, 10, 10)
        layout3.setSpacing(0)
        frame1 = QFrame()
        frame1.setLayout(layout2)
        self.layout.addWidget(frame1)
        frame2 = QFrame()
        frame2.setLayout(layout3)
        self.layout.addWidget(frame2, alignment = Qt.AlignRight)
        self.piclabel = QLabel()
        self.piclabel.setText(alias[0])
        self.piclabel.setAlignment(Qt.AlignCenter)
        self.piclabel.setFixedSize(50, 50)
        self.piclabel.setStyleSheet('border-radius: 25px; background-color: #f092de; font-size: 20px;')
        layout2.addWidget(self.piclabel)
        self.namelabel = QLabel(alias)
        if access == 1:
            self.namelabel.setStyleSheet('font-size: 20px; margin-left: 3px; color: #0f9000;')
        elif access == 2:
            self.namelabel.setStyleSheet('font-size: 20px; margin-left: 3px; color: #0020ff;')
        else:
            self.namelabel.setStyleSheet('font-size: 20px; margin-left: 3px;')
        layout2.addWidget(self.namelabel)
        self.seenlabel = QLabel()
        self.seenlabel.setFixedSize(16, 16)
        if lastseen == 'Online':
            self.seenlabel.setStyleSheet('border-radius: 8px; background-color: #00f700;')
        else:
            self.seenlabel.setStyleSheet('border-radius: 8px; background-color: #fd0000;')
        layout3.addWidget(self.seenlabel)
        self.timelabel = QLabel(lastseen)
        self.timelabel.setStyleSheet('font-size: 15px; margin-left: 1px;')
        layout3.addWidget(self.timelabel)


class ChatRoomObjectWidget(QFrame):
    def __init__(self, **kwargs):
        QFrame.__init__(self)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.define_styles()
        self._setup(**kwargs)

    def define_styles(self):
        self.sent = '''
        ChatRoomObjectWidget{
            border: 2px solid #08b7ff;
            border-top-right-radius: 10px;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            background-color: %s
        }
        '''
        self.received = '''
        ChatRoomObjectWidget{
            border: 2px solid #02dfa5;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            border-bottom-left-radius: 10px;
            background-color: %s
        }
        '''
        self.status = '''
        ChatRoomObjectWidget{
            border: 2px solid #91b7b0;
            border-top-right-radius: 10px;
            border-top-left-radius: 10px;
            border-bottom-right-radius: 10px;
            border-bottom-left-radius: 10px;
            background-color: %s
        }
        '''

    def adjust(self, message):
        length = len(message)
        emoji = re.findall(r'<img[^>]+.*?>', message)
        if emoji:
            ln = 0
            weight = len(emoji) * 5
            for em in emoji: ln += len(em)
            length -= ln
            length += weight
        self.mlabel.setMaximumWidth(600)
        if re.match(r'<img[^>]+title.*?>', message): pass
        elif length > 50: self.mlabel.setMinimumWidth(500)
        elif length > 40: self.mlabel.setMinimumWidth(400)
        elif length > 30: self.mlabel.setMinimumWidth(300)
        elif length > 20: self.mlabel.setMinimumWidth(200)
        elif length > 10: self.mlabel.setMinimumWidth(100)
        else: pass
    
    def set_style(self):
        selected = getattr(self, self._style)
        self.setStyleSheet(selected%self.background_color)

    def _setup(self, sender='', message='', time=''):
        self._style = 'status'
        self.background_color = 'rgba(145, 163, 176, 200)'
        self.align = Qt.AlignTop | Qt.AlignCenter

        self.mlabel = QLabel()
        self.mlabel.setWordWrap(True)
        self.mlabel.setText(message)
        self.adjust(message)
        
        if time:
            if sender: 
                self._style = 'received'
                self.background_color = 'rgba(0, 191, 165, 200)'
                self.align = Qt.AlignTop | Qt.AlignLeft

                self.slabel = QLabel()
                self.slabel.setAlignment(Qt.AlignLeft)
                self.slabel.setText(sender)
                self.slabel.setStyleSheet('font-size: 13px; color: black')
                self._layout.addWidget(self.slabel)

            else: 
                self._style = 'sent'
                self.background_color = 'rgba(54, 183, 190, 200)'
                self.align = Qt.AlignTop | Qt.AlignRight

            self.tlabel = QLabel()
            self.tlabel.setAlignment(Qt.AlignRight)
            self.tlabel.setText(time)
            self.tlabel.setStyleSheet('font-size: 11px; color: black; background: %s'%self.background_color)
            self._layout.addWidget(self.tlabel)
            
        self.mlabel.setStyleSheet('font-size: 14px; color: black; background: %s'%self.background_color)
        self._layout.insertWidget(int(bool(time and sender)), self.mlabel)
        
        self.set_style()
        self.setFixedSize(self._layout.sizeHint())

    def createR(self, sender, message, time): self._setup(sender, message, time)

    def createS(self, message, time): self._setup(message=message, time=time)

    def createT(self, message): self._setup(message=message)

    def render(self, *args):
        if len(args) == 1: self.createT(args[0])
        elif len(args) == 2: self.createS(args[0], args[1])
        elif len(args) == 3: self.createR(args[0], args[1], args[2])
        else: return None


class ChatRoomView(Scrolled_Widget):
        def __init__(self):
            Scrolled_Widget.__init__(self)
            # self.setStyleSheet('.QWidget{background-image: url(resources/images/background.svg); background-repeat: repeat-xy; background-color: #dfdbe5;}')



class ChatRoom(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)


class ChatRoomWidget(QFrame):
    def __init__(self, receiver=None):
        QFrame.__init__(self)
        self.receiver = receiver
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # self.parser = TextParser()

        self.setStyleSheet(u"QWidget {background:rgb(20, 36, 43); color: white}\n"
        "\n"
        " QPushButton{\n"
        "	border: 1px solid;\n"
        "	border-radius: 4px ;\n"
        "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
        "                                        stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));\n"
        "	color: rgb(234, 183, 78)\n"
        "}\n"
        "\n"
        " QPushButton:pressed {\n"
        "    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
        "                                        stop: 0 rgb(170, 132, 57), stop: 1 rgb(234, 183, 78));\n"
        "	color:  rgb(20, 36, 43)\n"
        "  }\n"
        "\n"
        "")
        header_layout = QHBoxLayout()
        self.roomName = QPushButton(self, text="Chat Name")
        self.roomName.setMinimumSize(QSize(200, 40))
        font2 = QFont('Segoe UI', 14)
        font2.setBold(True)
        self.roomName.setFont(font2)

        header_layout.addWidget(self.roomName)

        pushButton_4 = QPushButton(self, text="Search")
        pushButton_4.setMaximumSize(QSize(50, 40))
        pushButton_4.setStyleSheet(u"")

        header_layout.addWidget(pushButton_4)

        pushButton_2 = QPushButton(self, "Menu")
        pushButton_2.setMaximumSize(QSize(50, 40))
        pushButton_2.setStyleSheet(u"")

        header_layout.addWidget(pushButton_2)
        self._layout.addLayout(header_layout)

        self.chat_room = ChatRoomView()
        self._layout.addWidget(self.chat_room)

     # bottom frame
        bottom_frame = QFrame()
        bottom_frame_layout = QHBoxLayout()
        bottom_frame.setLayout(bottom_frame_layout)

        fxh = 40
        ss = 24
        sy = 20
        # bottom_frame.setMinimumHeight(fxh+20)
        bottom_frame.setMaximumHeight(fxh+20)
        self._layout.addWidget(bottom_frame)
    
     # emoji button
        embutton = QPushButton()
        embutton.setMinimumSize(fxh, fxh)
        embutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'resources', 'images', 'emoji.svg')))
        embutton.setIconSize(QSize(ss, ss))
        embutton.setToolTip('Open emoji picker')
        embutton.setStyleSheet('.QPushButton{border: 2px solid #91b7b0; border-radius: %dpx; background-color: rgba(145, 163, 176, 200);}.QPushButton::hover{background-color: rgb(64, 64, 64);}'%(sy))

        embutton.clicked.connect(self.show_emoji)
        bottom_frame_layout.addWidget(embutton)

     # text input
        self.text_input = QTextEdit()
        self.text_input.setStyleSheet('font-size: 15px; ')
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self.text_input)
        shortcut.activated.connect(self.send_message)
        bottom_frame_layout.addWidget(self.text_input)
    
     # send button
        sebutton = QPushButton()
        sebutton.setFixedSize(fxh, fxh)
        sebutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'resources', 'images', 'send.svg')))
        sebutton.setIconSize(QSize(ss, 32))
        sebutton.setToolTip('Send a message (Ctrl+Enter)')
        sebutton.setStyleSheet('.QPushButton{border: 2px solid #08b7ff; border-radius: %dpx; background-color: rgba(8, 129, 255, 200);}.QPushButton::hover{background-color: rgb(8, 99, 255);}'%(sy))

        sebutton.clicked.connect(self.send_message)
        bottom_frame_layout.addWidget(sebutton)
        
        self.emoji_widget = EmojiWidget(self.input_emoji)
        self._layout.addWidget(self.emoji_widget)
        self.emoji_widget.hide()
        self.emoji_shown = 0

    def input_emoji(self, path):
        formatted = '<img src = {} />'.format(path)
        self.text_input.insertHtml(formatted)
    
    def show_emoji(self):
        if self.emoji_shown:
            self.emoji_widget.hide()
            self.emoji_shown = 0

        else:
            self.emoji_widget.show()
            self.emoji_shown = 1

    def send_message(self):
        html = self.text_input.toHtml()
        self.parser.feed(html)
        message = self.parser.produce()
        actual = emoji.emojize(message[0], use_aliases = True)#this is what we'll send
        if len(actual) > 0:
            bb = ChatRoomObjectWidget(message=message[1], time='10:46pm')
            self.chat_room._layout.addWidget(bb, alignment = bb.align)
            self.text_input.clear()
            if self.receiver: self.receiver(actual)
            #actually send message, username is -> self.chat_room.get_chat()


class ChatRoomsTab(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.setStyleSheet('''QWidget {background:rgb(20, 36, 43)}; QTabWidget::pane{border: none;}''')
        self.setStyleSheet('''QTabWidget::pane { /* The tab widget frame */
        border-top: 2px solid #C2C7CB;
        }

        QTabWidget::tab-bar {
            left: 5px; /* move to the right by 5px */
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QTabBar::tab {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n stop: 1 rgb(20, 36, 43), stop: 0 rgb(79, 113, 147));
            border: 2px solid #C4C4C3;
            border-bottom-color: #C2C7CB; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 8ex;
            padding: 2px;
        }

        QTabBar::tab:selected, QTabBar::tab:hover {
            background:qlineargradient(spread:pad, x1:0.687, y1:0.510864, x2:0.807, y2:1, stop:0.625 rgba(250, 0, 13, 248), stop:0.852273 rgba(255, 255, 255, 223));
        }

        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #C2C7CB; /* same as pane color */
        }

        QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
        }

        /* make use of negative margins for overlapping tabs */
        QTabBar::tab:selected {
            /* expand/overlap to the left and right by 4px */
            margin-left: -4px;
            margin-right: -4px;
        }

        QTabBar::tab:first:selected {
            margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
        }

        QTabBar::tab:last:selected {
            margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
        }

        QTabBar::tab:only-one {
            margin: 0; /* if there is only one tab, we don't want overlapping margins */
        }''')

        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.del_chat)

        self.chats = {}
        self.new_chat('Group')

    def new_chat(self, alias):
        if alias in self.chats: pass
        else:
            chatwin = ChatRoomWidget()

            self.chats[alias] = chatwin
            self.addTab(chatwin, alias)
        self.setCurrentIndex(self.indexOf(self.chats[alias]))

    def del_chat(self, index):
        alias = str(self.tabText(index))
        if alias in self.chats and alias != 'Group':
            self.widget(index).deleteLater()
            self.removeTab(index)
            del self.chats[alias]
        else:
            print('cannot close tab number {0}: {1}'.format(index, alias))

    def get_chat(self): return self.tabText(self.currentIndex())


class ChatObjectsWidget(QFrame):
    def __init__(self, callback=None):
        QFrame.__init__(self)
        self.callback = callback

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        
     # title of the chats list in view contacts, groups, channels
        title_frame = QFrame()
        title_frame_layout = QHBoxLayout()
        title_frame.setLayout(title_frame_layout)
        title_frame.setMaximumHeight(40)
        self._layout.addWidget(title_frame)

        self.titleLabel = QLabel('Participants')
        self.titleLabel.setStyleSheet('font-size: 21px;')
        title_frame_layout.addWidget(self.titleLabel)
        
        refresh_button = QPushButton()
        refresh_button.setMinimumSize(30, 30)
        refresh_button.setIcon(QIcon(os.path.join('resources', 'images', 'refresh.svg')))
        refresh_button.setIconSize(QSize(25, 25))
        refresh_button.setToolTip('Refresh participants list')
        refresh_button.setStyleSheet('.QPushButton{border-radius: 15px;}.QPushButton::hover{background-color: rgba(94, 94, 94, 150);}')
        
        title_frame_layout.addWidget(refresh_button)

        self.chats_widget = Scrolled_Widget()
        self._layout.addWidget(self.chats_widget)

    def add_objects(self, obj): ...

    def set_title(self, title): self.titleLabel.setText(title)


class AuthForm(QFrame):
    def __init__(self, cred_hook):
        QFrame.__init__(self)
        self.setStyleSheet('AuthForm{background-color: #d3d3d3;}')
        self.create_layout()
        self.create_frames()
        self.create_elements()
        self.create_elements2()
        self.cred_hook = cred_hook

    def create_layout(self):
        self.main_ly = QVBoxLayout()
        self.sign_in_ly = QFormLayout()
        self.sign_up_ly = QFormLayout()
        self.logo_ly = QVBoxLayout()
        self.sizer_ly = QVBoxLayout()

    def create_frames(self):
        self.setLayout(self.main_ly)
        self.sign_in_fr = QFrame()
        self.sign_in_fr.setLayout(self.sign_in_ly)
        self.sign_in_fr.setStyleSheet('.QFrame{background-color: #303030;}')
        self.sign_up_fr = QFrame()
        self.sign_up_fr.setLayout(self.sign_up_ly)
        self.sign_up_fr.setStyleSheet('.QFrame{background-color: #303030;}')
        self.logo_fr = QFrame()
        self.logo_fr.setLayout(self.logo_ly)
        self.sizer_fr = QFrame()
        self.sizer_fr.setFixedHeight(490)
        self.sizer_fr.setLayout(self.sizer_ly)
        limage = QLabel()
        limage.setPixmap(QIcon(os.path.join('resources', 'images', 'chat.svg')).pixmap(QSize(64, 64)))
        self.logo_ly.addWidget(limage)
        ltext = QLabel('Chatz')
        ltext.setStyleSheet('font-size: 22px;')
        self.logo_ly.addWidget(ltext)
        self.tab_fr = QTabWidget()
        self.tab_fr.setFixedSize(330, 314)
        self.tab_fr.addTab(self.sign_in_fr, 'Sign In')
        self.tab_fr.addTab(self.sign_up_fr, 'Sign Up')
        self.tab_fr.setStyleSheet('''QTabBar::tab{color: #f1f1f1; width: 165px; height: 28px; font-size: 22px;}QTabBar::tab:!selected{background-color: #202020;}
                                     QTabBar::tab:selected{background-color: #3a6ff0;}QTabWidget::pane{border: none;}''')
        self.sizer_ly.addWidget(self.tab_fr, alignment = Qt.AlignTop)
        self.main_ly.addWidget(self.logo_fr, alignment = Qt.AlignBottom|Qt.AlignCenter)
        self.main_ly.addWidget(self.sizer_fr, alignment = Qt.AlignCenter)

    def create_elements(self):
        sidlbl = QLabel('Connect URL')
        sidlbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.sid = QLineEdit()
        self.sid.setPlaceholderText('srv.haloserver.io:10950')
        self.sid.setStyleSheet('font-size: 15px;')
        self.sign_in_ly.addRow(sidlbl)
        self.sign_in_ly.addRow(self.sid)
        alslbl = QLabel('Username')
        alslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.als = QLineEdit()
        self.als.setPlaceholderText('John.Doe')
        self.als.setStyleSheet('font-size: 15px;')
        self.sign_in_ly.addRow(alslbl)
        self.sign_in_ly.addRow(self.als)
        psslbl = QLabel('Password')
        psslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.pss = QLineEdit()
        self.pss.setPlaceholderText('p4ssw0rd!')
        self.pss.setEchoMode(QLineEdit.Password)
        self.pss.returnPressed.connect(self.signin)
        self.pss.setStyleSheet('font-size: 15px;')
        self.sign_in_ly.addRow(psslbl)
        self.sign_in_ly.addRow(self.pss)
        spc = QLabel('')
        self.sign_in_ly.addRow(spc)
        self.sbm = QPushButton('Connect And Sign In')
        self.sbm.setFixedHeight(35)
        self.sbm.setDefault(True)
        self.sbm.setStyleSheet('font-size: 15px;')
        self.sbm.clicked.connect(self.signin)
        self.sign_in_ly.addRow(self.sbm)

    def create_elements2(self):
        sidlbl = QLabel('Connect URL')
        sidlbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.sid2 = QLineEdit()
        self.sid2.setPlaceholderText('srv.haloserver.io:10950')
        self.sid2.setStyleSheet('font-size: 15px;')
        self.sign_up_ly.addRow(sidlbl)
        self.sign_up_ly.addRow(self.sid2)
        alslbl = QLabel('Username')
        alslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.als2 = QLineEdit()
        self.als2.setPlaceholderText('John.Doe')
        self.als2.setStyleSheet('font-size: 15px;')
        self.sign_up_ly.addRow(alslbl)
        self.sign_up_ly.addRow(self.als2)
        psslbl = QLabel('Password')
        psslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.pss2 = QLineEdit()
        self.pss2.setPlaceholderText('p4ssw0rd!')
        self.pss2.setEchoMode(QLineEdit.Password)
        self.pss2.returnPressed.connect(self.signup)
        self.pss2.setStyleSheet('font-size: 15px;')
        self.sign_up_ly.addRow(psslbl)
        self.sign_up_ly.addRow(self.pss2)
        spc = QLabel('')
        self.sign_up_ly.addRow(spc)
        self.sbm2 = QPushButton('Connect And Sign Up')
        self.sbm2.setFixedHeight(35)
        self.sbm2.setDefault(True)
        self.sbm2.setStyleSheet('font-size: 15px;')
        self.sbm2.clicked.connect(self.signup)
        self.sign_up_ly.addRow(self.sbm2)

    def signin(self):
        server = str(self.sid.text())
        uname = str(self.als.text())
        passwd = str(self.pss.text())
        creds = (server, uname, passwd)
        self.cred_hook(creds)

    def signup(self):
        server = str(self.sid2.text())
        uname = str(self.als2.text())
        passwd = str(self.pss2.text())
        creds = (server, uname, passwd)
        self.cred_hook(creds)

