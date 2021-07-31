
from .widgets import *

users = ['alien', 'brand-producthunt', 'brand-python', 'face-id', 'user-circle']
colors = ['red', 'blue', 'grey', 'green', 'orange']

_users = tuple(zip(users, colors))

users = []
for u in range(2): users.extend(_users)


class Chat_LineEdit(QLineEdit):
    buttonClicked = Signal()
    
    def __init__(self, icon='', go_icon='', parent=None, completer=False, default_values=[], completer_sense=Qt.CaseInsensitive, callback=None, height=35, margin=4):
        QLineEdit.__init__(self, parent)
    
        self.default_values = default_values
        self.completer_sense = completer_sense
        self.callback = callback
        
        if completer or default_values: self.set_completer(default_values, completer_sense)

        self.button = None
        self.margin = margin
        self._height = height

        if icon:
            icon = QIcon(f':{icon}')
            self.addAction(icon, QLineEdit.LeadingPosition)
        
        if go_icon:
            self.gw = height
            self.button = QPushButton(self)
            self.button.setIcon(QIcon(f':{go_icon}'))
            self.button.setToolTip('Go')

            self.button.setStyleSheet('''
            QLineEdit{
                /*padding-right: px*/
                }
            QPushButton{
                background: %s;
                text-align: center
                }
            QPushButton::hover{
                background: %s
                }
            QPushButton::pressed{
                background: %s
                }'''
                % (
                    STYLE.LIGHT_SHADE,
                    STYLE.DARK_SHADE, 
                    STYLE.DARK,
                  )
                )

            self.button.setCursor(Qt.ArrowCursor)
            self.button.clicked.connect(self.buttonClicked.emit)
            self.returnPressed.connect(self.button.click)
            self.buttonClicked.connect(self.call_callback)

        if self._height:
            self.setMinimumHeight(self._height)
            self.setMaximumHeight(self._height)
    
    def call_callback(self):
        if self.callback: self.callback(self.text())
    
    def set_completer(self, default_values=[], completer_sense=Qt.CaseInsensitive):
        self.default_values = default_values or self.default_values
        self.completer_sense = completer_sense

        completer = QCompleter(self.default_values)
        completer.setCaseSensitivity(self.completer_sense)
        self.setCompleter(completer)

    def showEvent(self, event):
        if self.button:
            size = self.size()
            w = size.width()
            h = size.height()
            m = self.margin
            
            gw = self.gw - m
            mh = (h-gw)/4
            g = (w-gw, mh, gw, gw-mh)

            self.button.setIconSize(QSize(20, 20))
            self.button.setMaximumHeight(gw)
            self.button.setGeometry(*g)

    resizeEvent = showEvent
    
    def clear_default_values(self): self.default_values = []

    def add_default_value(self, value): self.default_values.append(value)


class IconButton(QPushButton):
    def __init__(self, parent=None, icon_size=25, icon='', size=0):
        QPushButton.__init__(self, parent)

        self.setIconSize(QSize(icon_size+10, icon_size))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._style = 'text-align: center'
        self.default_style = lambda: self.setStyleSheet(self._style)
        
        if icon: self.set_icon(icon)
        if size:
            self.setMinimumSize(size, size)
            self.setMaximumSize(size, size)
    
    def set_icon(self, icon):
        # print(icon)
        # return
        icon = QIcon(f':{icon}')
        self.setIcon(icon)
    
    def showEvent(self, event): self.default_style()


class Chat_Widget(QFrame):
    
    def __init__(self, svg, color, callback, user=None):

        QFrame.__init__(self)
        self._style = 'border-radius: 5px; background: %s; color: %s'
        self.leaveEvent(0)

        self.user = user
        self.callback = callback
        
        self.setMinimumHeight(70)
        self.setMaximumHeight(70)
        
        m = 2
        layout = SETUP_FRAME(obj=self, orient='h', margins=[m*2, m*2, m*2, m*2], space=4)

        self.icon_frame, icon_layout = SETUP_FRAME(mother_layout=layout, re_obj=1)
        d = 60
        self.icon_frame.setMinimumSize(d, d)
        self.icon_frame.setMaximumSize(d, d)
        self.icon_frame.setStyleSheet('border-radius: %spx'%(d/2))

        self.icon = IconButton(icon=f'chat_list/{svg}.svg', icon_size=d-10)
        icon_layout.addWidget(self.icon)

        self.status_bubble = QLabel(self.icon_frame)
        self.status_bubble.setStyleSheet('background: green; border-radius: 5px; color: white')
        self.status_bubble.setToolTip('online')
        
        self.texts_frame, _ = SETUP_FRAME(mother_layout=layout, re_obj=1)

        self.name = QLabel(self.texts_frame)
        self.name.setText(svg)
        self.name.setGeometry(5, 0, 150, 20)
        self.name.setStyleSheet('font: bold 13.5pt')

        self.last_info = QLabel(self.texts_frame)
        self.last_info.setText(svg + '...')
        self.last_info.setGeometry(5, 42, 150, 15)
        self.last_info.setStyleSheet('font: 8pt')

        date_time = QDateTime.currentDateTime()
        date = date_time.toString('dd/MM/yy')
        self.date = QLabel(self.texts_frame)
        self.date.setText(date)
        font = QFont()
        font.setPointSizeF(8)
        fm = QFontMetrics(font)
        self.dbr = fm.boundingRect(date)
        self.date.setFont(font)

        self.unread_bubble = QLabel(self.texts_frame)
        unread = '5000'
        self.unread_bubble.setText(unread)
        font = QFont()
        font.setBold(1)
        self.unread_bubble.setFont(font)
        self.unread_bubble.setAlignment(Qt.AlignCenter)
        fm = QFontMetrics(font)
        self.ubr = fm.boundingRect(unread)
        self.unread_bubble.setStyleSheet('background: green; border-radius: 5px; color: white')

        time = date_time.toString('HH:mm:ss')
        self.time = QLabel(self.texts_frame)
        self.time.setText(time)
        font = QFont()
        font.setPointSizeF(8)
        fm = QFontMetrics(font)
        self.tbr = fm.boundingRect(time)
        self.time.setFont(font)

        self.user = svg
    
    def enterEvent(self, event): self.setStyleSheet(self._style % (STYLE.DARK_SHADE, STYLE.LIGHT))
        
    def leaveEvent(self, event): self.setStyleSheet(self._style % (STYLE.LIGHT, STYLE.DARK))


    def mouseReleaseEvent(self, event):
        self.leaveEvent(event)
        self.callback(self.user)

    def mousePressEvent(self, event):
        self.setStyleSheet(self._style % (STYLE.DARK, STYLE.LIGHT))

    def showEvent(self, event):
        w = self.icon_frame.width()
        h = self.icon_frame.width()
        self.status_bubble.setGeometry(w-12, h-12, 10, 10)

        w = self.texts_frame.width()
        h = self.texts_frame.height()

        self.date.setGeometry(w-self.dbr.width()-6, 0, self.dbr.width(), self.dbr.height())
        self.unread_bubble.setGeometry(w-self.ubr.width()-12,  (h-self.ubr.height())/2, self.ubr.width()+6, self.ubr.height()+3)
        self.time.setGeometry(w-self.tbr.width()-6, 48, self.tbr.width(), self.tbr.height())
    
    resizeEvent = showEvent


class Chats_Widget(Scrolled_Widget):

    def __init__(self, tab, callback=None):
        Scrolled_Widget.__init__(self, tab, space=2, margins=[2, 2, 2, 2])
        self._layout.setAlignment(Qt.AlignTop)
        self.set_bars_off()
        self._callback = callback

    def add_chat_object(self, chat_object):
        chat = Chat_Widget(*chat_object, callback=self.callback)
        self._layout.addWidget(chat)
    
    def fill(self):
        for user in users: self.add_chat_object(user)

    def callback(self, user):
        print(user)


class ChatRoomButton(IconButton): ...


class Chat_Room_HeaderFooter(QFrame):

    def __init__(self, w=5):
        QFrame.__init__(self)
        self._w = w
        self.deff = (
                STYLE.DARK_SHADE, STYLE.LIGHT, w,
                STYLE.LIGHT_SHADE,
                STYLE.DARK,
              )
        self.leaveEvent(0)
    
    def set_style(self, tup):
        self.setStyleSheet('''
            QWidget{
                background: %s;
                color: %s;
                border-radius: %d
                }
            
            ChatRoomButton::hover{
                background: %s;
                }
            QPushButton::pressed{
                background: %s;
                }
            '''
            % tup
            )
    
    def enterEvent(self, event):
        self.set_style(
            (
                STYLE.DARK, STYLE.LIGHT, self._w,
                STYLE.LIGHT_SHADE,
                STYLE.DARK,
              )
            )
        
    def leaveEvent(self, event): self.set_style(self.deff)


class Chat_Room_Header(Chat_Room_HeaderFooter):
    
    def __init__(self, icon, name):
        Chat_Room_HeaderFooter.__init__(self)
        
        self.icon = ChatRoomButton(parent=self, icon=icon,  icon_size=45, size=45)

        w = 60
        self.name = QLabel(self)
        self.name.setText(name)
        self.name.setObjectName('nam')
        font = QFont()
        font.setBold(1)
        font.setPointSizeF(15)
        fm = QFontMetrics(font)
        br = fm.boundingRect(name)
        self.name.setFont(font)
        self.name.setGeometry(w, 0, br.width(), br.height())

        self.status = QLabel(self)

        date_time = QDateTime.currentDateTime()
        time = date_time.toString('HH:mm:ss')
        date = date_time.toString('dd/MM/yy')

        status = f'Offline | {date} | {time} '
        self.status.setText(status)
        font = QFont()
        font.setPointSizeF(10)
        fm = QFontMetrics(font)
        br = fm.boundingRect(status)
        self.status.setFont(font)
        self.status.setGeometry(w, w-br.height()-13, br.width(), br.height())

        s, w = 30, 40
        self.phone_call = ChatRoomButton(icon='chat_room/phone-call.svg', parent=self, icon_size=s, size=w)
        
        self.video_call = ChatRoomButton(icon='chat_room/video.svg', parent=self, icon_size=s, size=w)
        self.menu = ChatRoomButton(icon='chat_room/dots.svg', parent=self, icon_size=s, size=w)

        self.setMaximumHeight(50)
    
    def showEvent(self, e):
        h = self.height()
        w = 60

        y = abs((h-w)/2) 
        self.icon.setGeometry(5, 2.5, w, w)

        d = 20
        w -= d
        dd = w-d-d

        self.phone_call.setGeometry(self.width()-w*3-5, y, dd, w)
        self.video_call.setGeometry(self.width()-w*2-5, y, dd, w)
        self.menu.setGeometry(self.width()-w-5, y, dd, w)
    
    resizeEvent = showEvent


class Text_Input(QTextEdit):
    def __init__(self, parent=None, callback=None):
        QTextEdit.__init__(self, parent)
        self._par = parent

        self.setPlaceholderText('Type a message ...')
        self.setStyleSheet('background: %s; color: %s; padding: 3px'%(STYLE.LIGHT_SHADE, STYLE.DARK_SHADE))
    
        self.fm = QFontMetrics(self.font())

        self.setMinimumHeight(40)
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut.activated.connect(callback)
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
    def input_emoji(self, path):
        formatted = '<img src = {} />'.format(path)
        self.insertHtml(formatted)
    
    @property
    def text(self): return self.toPlainText().strip()
    
    def keyReleaseEvent(self, e):
        br = self.fm.boundingRect(0, 0, self.width(), 0, 0, self.toPlainText())
        h = br.height()
        hh = abs(h)

        if hh < 40: hh = 40
        elif hh > 240: hh = 240

        self.setMinimumHeight(hh)

        hh += 10
        self._par.setMinimumHeight(hh)
        self._par.setMaximumHeight(hh)


class Chat_Room_Footer(Chat_Room_HeaderFooter):
    
    def __init__(self):
        Chat_Room_HeaderFooter.__init__(self, 5)

        self.setMinimumHeight(50)
        self.setMaximumHeight(50)

        self.w = 40
        self.s = 30

        self.emoji = ChatRoomButton(parent=self, icon='chat_room/mood-smile.svg', icon_size=self.s, size=self.w)

        self.message = Text_Input(self, self.send_message)
        self.message.setTextColor('black')

        self.link = ChatRoomButton(parent=self, icon='chat_room/link.svg', icon_size=self.s, size=self.w)

        self.send = ChatRoomButton(parent=self, icon='chat_room/send.svg', icon_size=self.s, size=self.w)
        self.send.setToolTip('Send a message (Ctrl+Enter)')

    
    def send_message(self):
        return
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

    def showEvent(self, e):
        w = self.width()
        h = self.height()

        j = h-self.w
        self.emoji.setGeometry(5, j, 0, 0)
        self.message.setGeometry(50, 5, w-140, 0)
        self.link.setGeometry(w-(self.w*2)-5, j, 0, 0)
        self.send.setGeometry(w-self.w-5, j, 0, 0)

    resizeEvent = showEvent


class Chat_Room_Object(QFrame):
    def __init__(self, obj):
        QFrame.__init__(self)
        self.obj = obj

        # date
        # message
            # received
            # sent
            # picture
            # document
            # audio
            # video
            # contact
        # 



class Chat_Room(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        layout = SETUP_FRAME(obj=self)










        for a, b in [('adadada', 1), ('ashagsas', 2), ('askakd', 3)]: self.add_object(a, b)
    
    def add_object(self, obj, type):
        ...



class Chat_Room_Widget(QFrame):
    def __init__(self, icon, name, profile):
        QFrame.__init__(self)

        self.icon, self.name = icon, name
        self.profile = profile
        layout = SETUP_FRAME(obj=self, orient='v', margins=[2, 2, 2, 2])

        self.header = Chat_Room_Header(icon, name)
        layout.addWidget(self.header)

        self.room = Chat_Room()
        layout.addWidget(self.room)
        self.setStyleSheet('''
            QFrame{
                background: url(:chat_room/wallpaper14.png) center
            }
            ''')

        self.footer = Chat_Room_Footer()
        layout.addWidget(self.footer)

    
    def showEvent(self, event):
        self.profile.update_user(self.icon, self.name)


class Chat_Rooms_Tab(QTabWidget):
    
    def __init__(self, profile):
        QTabWidget.__init__(self)
        self.setMinimumWidth(450)
        self.profile = profile
    
    def add_chat_room(self, icon, name):
        w = Chat_Room_Widget(icon, name, self.profile)
        self.addTab(w, QIcon(f':{icon}'), name)


class Chat_Profile(QFrame):

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.setMaximumWidth(250)
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

        details, details_layout = SETUP_FRAME(layout, re_obj=1)

        icon_frame, icon_layout = SETUP_FRAME(details_layout, re_obj=1, margins=[10, 5, 10, 0])
        icon_layout.setAlignment(Qt.AlignHCenter)
        r = 120

        self.icon = IconButton(icon='chat_list/user-circle.svg', icon_size=r)
        self.icon.setMinimumSize(r, r)
        self.icon.setMaximumSize(r, r)
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
        layout.addWidget(media)

        block = QPushButton()
        block.setIcon(QIcon(':profile/message-circle-off.svg'))
        block.setText('Block contact')
        layout.addWidget(block)

        report = QPushButton()
        report.setText('Report contact')
        report.setIcon(QIcon(':profile/thumb-down.svg'))
        layout.addWidget(report)

    def update_user(self, icon, name):
        self.icon.set_icon(icon)
        self.name.setText(name)
        
        br = self.n_fm.boundingRect(name)
        self.name.setText(name)
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setMinimumHeight(br.height()+5)
        self.name.setMaximumHeight(br.height()+5)

        username = 'prmpsmart@gmail.com'
        br = self.u_fm.boundingRect(username)
        self.username.setText(username)
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setMinimumHeight(br.height()+5)
        self.username.setMaximumHeight(br.height()+5)










