
import os, re
from html.parser import HTMLParser


from .emoji_ui import *
from .chat_listing import *


class TextParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._pretty = ''
        self._textout = ''
        self.paragraph = False

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for x in attrs:
                if x[0] == 'src':
                    self._pretty += '<img src="{}" />'.format(x[1])
                    self._textout += ':{}:'.format(x[1].split(os.path.sep)[-1].split('.')[0])
        elif tag == 'p':
            self.paragraph = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self._pretty += '\n'
            self._textout += '\n'
            self.paragraph = False

    def handle_data(self, data):
        if self.paragraph:
            self._pretty += data
            self._textout += data

    def produce(self):
        temp = self._textout.strip()
        temp2 = self._pretty.strip()
        self._pretty = ''
        self._textout = ''
        return temp, temp2



class ChatRoomButton(IconButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mousePressEvent(self, e) -> None:
        self.setStyleSheet('background: %s; color: %s'%(STYLE.LIGHT, STYLE.LIGHT))
        self.clicked.emit()
    
    def enterEvent(self, event):
        self.setStyleSheet('background: %s; color: %s'%(STYLE.DARK_SHADE, STYLE.LIGHT))

    def mouseReleaseEvent(self, event):
        self.setStyleSheet('background: %s; color: %s'%(STYLE.DARK, STYLE.LIGHT))
    
    leaveEvent = mouseReleaseEvent


class ChatRoomH_F(QFrame):

    def __init__(self, w=5):
        QFrame.__init__(self)
        self._w = w
        self.leaveEvent(0)
        
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)

    @property
    def _style_colors(self): return (
        STYLE.DARK, STYLE.LIGHT, self._w,
        STYLE.DARK_SHADE,
        STYLE.LIGHT_SHADE,
    )
    
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
                STYLE.LIGHT,
              )
            )
        
    def leaveEvent(self, event): self.set_style(self._style_colors)


class ChatHeader(ChatRoomH_F):
    
    def __init__(self, chat_object, close):
        ChatRoomH_F.__init__(self)
        self.chat_object = chat_object

        self.icon = IconButton(parent=self, icon_size=45, size=45)
        self.icon.setStyleSheet('text-align: center; background: %s'%STYLE.LIGHT_SHADE)
        self.icon.mouseReleaseEvent = lambda e: None


        # self.mouseDoubleClickEvent = close

        self.name = QLabel(self)
        font = QFont()
        font.setBold(1)
        font.setPointSizeF(15)
        self.nfm = QFontMetrics(font)
        self.name.setFont(font)

        self.status = QLabel(self)

        font = QFont()
        font.setPointSizeF(10)
        self.sfm = QFontMetrics(font)
        self.status.setFont(font)
        
        s, w = 30, 40
        self.phone_call = ChatRoomButton(icon='chat_room/phone-call.svg', parent=self, icon_size=s, size=w)
        
        self.video_call = ChatRoomButton(icon='chat_room/video.svg', parent=self, icon_size=s, size=w)
        self.menu = ChatRoomButton(icon='chat_room/dots.svg', parent=self, icon_size=s, size=w)

        self.leaveEvent(0)
        self.update_()
    
    def update_(self):
        w = 60
        
        self.name.setText(self.chat_object.name)
        br = self.nfm.boundingRect(self.chat_object.name)
        self.name.setGeometry(w, 0, br.width(), br.height())
        
        status = 'ONLINE'

        if isinstance(self.chat_object, Contact):
            if self.chat_object._status != STATUS.ONLINE:
                date_time = self.chat_object.last_seen
                status = f'OFFLINE | {date_time.toString("dd/MM/yy | HH:mm:ss")}' if date_time else 'OFFLINE'
        
        self.status.setText(status)
        br = self.sfm.boundingRect(status)
        self.status.setGeometry(w, w-br.height()-13, br.width(), br.height())

        self.icon.set_icon(self.chat_object.icon)
    
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


class TextInput(QTextEdit):

    def __init__(self, parent=None, callback=None):
        QTextEdit.__init__(self, parent)

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
        br = self.fm.boundingRect(0, 0, self.width(), -1, Qt.TextWrapAnywhere, self.toPlainText())
        h = br.height()
        hh = abs(h)

        if hh < 40: hh = 40
        elif hh > 240: hh = 240

        self.setMinimumHeight(hh)

        hh += 10
        _par = self.parent().parent()
        _par.setMinimumHeight(hh)
        _par.setMaximumHeight(hh)


class ChatFooter(ChatRoomH_F):
    
    def __init__(self, emoji, room=None):
        ChatRoomH_F.__init__(self, 5)

        self.w = 40
        self.s = 30

        self._emoji = emoji
        self.room = room
        self._emoji_on = False

        self.parser = TextParser()
        
        self._layout = SETUP_FRAME(obj=self)
        self._wid = SETUP_FRAME(self._layout, orient=0)


        self.emoji = ChatRoomButton(parent=self._wid, icon='chat_room/mood-smile.svg', icon_size=self.s, size=self.w)
        self.emoji.clicked.connect(self.show_emoji)

        self.message = TextInput(parent=self._wid, callback=self.send_message)
        self.message.setTextColor('black')

        self.link = ChatRoomButton(parent=self._wid, icon='chat_room/link.svg', icon_size=self.s, size=self.w)

        self.send = ChatRoomButton(parent=self._wid, icon='chat_room/send.svg', icon_size=self.s, size=self.w)

        # self._emoji.hide()
        # self._layout.addWidget(self._emoji)

        self.send.setToolTip('Send a message (Ctrl+Enter)')
        self.send.clicked.connect(self.test_pressed)
    
    def show_emoji(self):
        if self._emoji_on:
            # self._layout.removeWidget(self._emoji)
            self._emoji_on = False
            self._emoji.hide()
            self.setMaximumHeight(50)
        else:
            self._emoji_on = True
            self._emoji.show()
            # self.setMaximumHeight(250)

    def test_pressed(self):
        self.send_message()
    
    def send_message(self):
        if not self.room: return

        html = self.message.toHtml()
        self.parser.feed(html)
        message = self.parser.produce()

        actual = emoji.emojize(message[0], use_aliases = True)#this is what we'll send
        if actual: self.room.add_message(actual)

        self.message.clear()

    def showEvent(self, e):
        _wid = self.emoji.parent()
        w = _wid.width()
        h = _wid.height()

        j = h-self.w
        self.emoji.setGeometry(5, j, 0, 0)
        self.message.setGeometry(50, 5, w-140, 0)
        self.link.setGeometry(w-(self.w*2)-5, j, 0, 0)
        self.send.setGeometry(w-self.w-5, j, 0, 0)

    resizeEvent = showEvent


class MessageType(QFrame):

    def  __init__(self, parent=None, space=5, margins=[5, 5, 5, 5]):
        QFrame.__init__(self, parent)

        self._layout = SETUP_FRAME(obj=self, space=space, margis=margins)

        self.setup()

    def setup(self): ...


class TextType(QFrame):

    def  __init__(self, tag,  **kwargs):
        MessageType.__init__(self, **kwargs)


class ImageType(QFrame):

    def  __init__(self, tag,  **kwargs):
        MessageType.__init__(self, **kwargs)


class AudioType(QFrame):

    def  __init__(self, tag,  **kwargs):
        MessageType.__init__(self, **kwargs)


class VideoType(QFrame):

    def  __init__(self, tag,  **kwargs):
        MessageType.__init__(self, **kwargs)




class ChatMessage(QFrame):
    SENT = '#08b7ff'
    RECEIVED = '#02dfa5'

    def __init__(self, client, chat_object, tag):
        QFrame.__init__(self)
        self.lay = SETUP_FRAME(obj=self, margins=[2, 2, 2, 2], orient='h', space=2)

        self.client = client
        self.chat_object = chat_object
        self.tag = tag

        self._wid, self._layout = SETUP_FRAME(self.lay, re_obj=1, margins=[4, 4, 4, 4], space=2)
        
        # chat_place = [chat_object, group, channel]
        # types = [text, image, music, voice note, video, document preview]

        # self.setAttribute(Qt.WA_TranslucentBackground)

        date_time = QDateTime.currentDateTime().toString('dd/MM/yy, HH:mm:ss  ')
        self.dateTime = date_time
        # message
            # received
            # sent
            # picture
            # document
            # audio
            # video
            # contact
        self.maxw = self.width() * 5 / 6
        self.botWid = self.iconLabel = self.textLabel = self.dateTimeLabel = self.nameLabel = self.statusLabel = None
        
        self.setup()
        self.set_style()

        for a in [self.textLabel, self.dateTimeLabel, self.nameLabel, self.statusLabel, self.botWid]:
            if a: a.setAttribute(Qt.WA_TranslucentBackground)
        
        graphicEffect = QGraphicsDropShadowEffect(self)
        graphicEffect.setBlurRadius(2)
        self.setGraphicsEffect(graphicEffect)
            
    def setup(self):
        self.text = 'Samuel Abraham, said hat we have to wait for Daramola David for the components before the practical can continue.'
        
        self.__style = '''
            border: 2px solid %s;
            border-top-right-radius: 10px;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            background-color: %s;
        '''
        self._style = self.SENT

        self.textLabel = QLabel()
        self.textLabel.setWordWrap(True)
        
        self.textLabel.setText(self.tag.data)
        self.textLabel.setStyleSheet('font-family: Times New Roman; font-size: 14px')


        self._layout.addWidget(self.textLabel)
        self.botWid, self._botLay = SETUP_FRAME(self._layout, orient='h', re_obj=1, space=3)

        self.dateTimeLabel = QLabel()
        self.dateTimeLabel.setText(self.tag.date_time.toString("dd/MM/yy ... HH:mm:ss"))
        self.dateTimeLabel.setAlignment(Qt.AlignRight)
        self.dateTimeLabel.setStyleSheet('font-size: 10px')
        self._botLay.addWidget(self.dateTimeLabel)
        
        self.textLabel.setMaximumWidth(self.maxw-200)

        self._sender = self.tag.sender == self.client.id
        chat = self.tag.chat
        
        if chat == CHAT.TEXT: self.build_text()
        elif chat == CHAT.AUDIO: self.build_audio()
        elif chat == CHAT.IMAGE: self.build_image()
        elif chat == CHAT.VIDEO: self.build_video()

    def set_style(self):
        self._wid.setStyleSheet('''
        border: 10px; 
        border-top-right-radius: 10px; 
        background: %s;
        color: black'''\
        %self._style)
        
        self.setStyleSheet(self.__style%(self._style, self._style))

    def build_text(self):
        if self._sender:
            self.align = Qt.AlignBottom | Qt.AlignRight
            self._style = self.SENT
            self.statusLabel = QLabel()
            
            if self.tag.sent: icon = 'chat_room/check.svg'
            else: icon = 'chat_room/clock.svg'
            pix = QIcon(f':{icon}').pixmap(12, 12)
            self.statusLabel.setPixmap(pix)

            self.statusLabel.setMaximumSize(20, 20)
            self._botLay.addWidget(self.statusLabel)

        else:
            if isinstance(self.chat_object, Group):
                chat_object = self.client.groups.get(self.tag.sender) or self.client.contacts.get(self.tag.sender)

                if chat_object and chat_object.icon: icon = QImage(chat_object.icon)
                else: icon = None

                self.iconLabel = IconButton(icon=icon, icon_size=30)
                self.iconLabel.setFixedSize(40, 40)
                self.iconLabel.setStyleSheet('text-align: center; border-radius: 20px; background: %s'%STYLE.LIGHT_SHADE)
                self.iconLabel.mouseReleaseEvent = lambda e: None
            
                self.lay.insertWidget(0, self.iconLabel, Qt.AlignBottom)

            self.align = Qt.AlignBottom | Qt.AlignLeft
            self._style = self.RECEIVED
            self.nameLabel = QLabel()
            self.nameLabel.setText(self.chat_object.name)
            self.nameLabel.setStyleSheet('font-family: impact; font-size: 15px')
            self._layout.insertWidget(0, self.nameLabel)

        # the widget gets the 3/4 width of the chat room
    
    def build_audio(self):
        ...
    def build_image(self):
        ...
    def build_video(self):
        ...
    
    def update_(self):
        if self.statusLabel:
            ...
        if self.iconLabel:
            ...
    
    # def resizeEvent(self, event):
    #     s = self.textLabel.size()
    #     self.textLabel.setMinimumHeight(s.height()+5)

    def monitor_send_status(self): ...




class ChatViewer(ScrolledWidget):

    def __init__(self, client, chat_object):
        ScrolledWidget.__init__(self, space=4, margins=[0, 0, 7, 7])

        self.client = client
        self.chat_object = chat_object
        self._chats_ = []
        
        self._widget.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.set_style()

        self.fill()
    
    def fill(self):
        for chat in self.chat_object.chats: self.add_tag(chat)

    def set_style(self):
        self.setStyleSheet('''
        QFrame{
            /*background: orange*/
            }
        QScrollBar:vertical {
            margin: 1px;
            width: 5px;
            background: %s
            }
        QScrollBar.add-line:vertical {
            height: 0;
            margin: 0
            }
        QScrollBar.sub-line:vertical {
            height: 0;
            margin: 0
            }

        ''' % (STYLE.DARK))

    def add_message(self, message):
        tag = Tag(data=message, action=CHAT, chat=CHAT.TEXT, sender=self.client.id, recipient=self.client.id, date_time=DATETIME(num=0))

        self.add_tag(tag)

    def add_tag(self, tag):
        obj = ChatMessage(self.client, self.chat_object, tag)
        self._chats_.append(obj)
        self._layout.addWidget(obj, 0, obj.align)
    
    def update_(self):
        for chat in self._chats_: chat.update_()


class ChatRoom(QFrame):

    def __init__(self, client, chat_object, profile, closeRoom, index=0, emoji=None, sb=None):
        QFrame.__init__(self)
        self.client = client
        self.send_back = sb

        self.chat_object = chat_object
        self.profile = profile
        layout = SETUP_FRAME(obj=self, orient='v', space=2, margins=[2, 2, 2, 2])
        self.index = index

        self.header = ChatHeader(chat_object, lambda e: closeRoom(chat_object))
        layout.addWidget(self.header)

        self.room = ChatViewer(client, chat_object)
        layout.addWidget(self.room)

        self.setStyleSheet('background: url(:chat_room/wallpaper14.png) center')

        self.footer = ChatFooter(emoji, room=self.room)
        layout.addWidget(self.footer)

    def resizeEvent(self, event): self.profile.update_user(self.chat_object)
    
    def update_(self):
        self.header.update_()
        self.room.update_()
    
    def showEvent(self, event): self.send_back(self.chat_object)



class ChatTab(QTabWidget):
    
    def __init__(self, client, profile, send_back):
        QTabWidget.__init__(self)

        self.setMinimumWidth(500)
        self.profile = profile
        self._send_back = send_back
        self._chats_ = {}
        self.client = client
        
        Emoji_Button.EMOJI_IMAGE = 1
        Emoji_Button.SET_SPRITE()
        self.emoji = Emoji_Ui()
    
    def add_chat_room(self, chat_object):
        
        count = self.count()
        if chat_object in self._chats_: index = self._chats_[chat_object]
        else:
            w = ChatRoom(self.client, chat_object, self.profile, self.closeRoom, index=count, emoji=self.emoji, sb=self.send_back)
            self._chats_[chat_object] = w.index

            icon = QIcon(':chat_list/user.svg')
            if chat_object.icon: icon = QIcon(QByteArray(chat_object.icon))
            
            self.addTab(w, icon, chat_object.name)
            index = count

        self.setCurrentIndex(index)

    def closeRoom(self, chat_object):
        ind = self._chats_[chat_object]
        self.removeTab(ind)
        del self._chats_[chat_object]
    
    def send_back(self, user): self._send_back(user)


