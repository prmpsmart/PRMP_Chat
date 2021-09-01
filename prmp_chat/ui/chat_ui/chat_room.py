
import os, re, math
from html.parser import HTMLParser
from prmp_lib.prmp_miscs.prmp_images import PRMP_ImageType


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

        self.icon = IconButton(parent=self, size=45)
        self.icon.setStyleSheet('text-align: center; background: %s'%STYLE.LIGHT_SHADE)
        self.icon.mouseReleaseEvent = lambda e: None


        self.mouseDoubleClickEvent = close

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
        self.phone_call = ChatRoomButton(icon='chat_room/phone-call.svg', parent=self, size=w)
        
        self.video_call = ChatRoomButton(icon='chat_room/video.svg', parent=self, size=w)
        self.menu = ChatRoomButton(icon='chat_room/dots.svg', parent=self, size=w)

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
                status = date_time.toString(OFFLINE_FORMAT) if date_time else 'OFFLINE'
                # status = f'OFFLINE | {date_time.toString("dd/MM/yy | HH:mm:ss")}' if date_time else 'OFFLINE'
        
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
        br = self.fontMetrics().boundingRect(0, 0, self.width(), -1, Qt.TextWrapAnywhere, self.toPlainText())
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


        self.emoji = ChatRoomButton(parent=self._wid, icon='chat_room/mood-smile.svg', size=self.w)
        self.emoji.clicked.connect(self.show_emoji)

        self.message = TextInput(parent=self._wid, callback=self.send_message)
        self.message.setTextColor('black')

        self.link = ChatRoomButton(parent=self._wid, icon='chat_room/link.svg', size=self.w)

        self.send = ChatRoomButton(parent=self._wid, icon='chat_room/send.svg', size=self.w)

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
    TYPE = 0

    def  __init__(self, parent=None, space=5, margins=[5, 5, 5, 5], tag=None, maxw=0):
        QFrame.__init__(self, parent)

        self.tag = tag
        self.maxw = maxw
        self.setMaximumWidth(self.maxw)
        self._layout = SETUP_FRAME(obj=self, space=space, margis=margins)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init()
        self.setup()

    def init(self): ...
    def setup(self): ...


class TextType(MessageType):
    max_letters_per_line = 60

    def  __init__(self, **kwargs):
        MessageType.__init__(self, space=0, margins=[], **kwargs)
    
    def restructure_line(self, line):
        length_of_line = len(line)

        text = ''
        lines = math.ceil(length_of_line/self.max_letters_per_line)

        for ln in range(lines):
            txt = line[ln * self.max_letters_per_line: (ln + 1) * self.max_letters_per_line] + '\n'
            text += txt

        return text, lines

    def restructured_text(self, lines):
        total_lines = 0
        rest_text = ''
        for line in lines:
            txt, ln = self.restructure_line(line)
            rest_text += txt
            total_lines += ln
        
        return rest_text.strip(), total_lines
    
    def init(self):
        self.raw_text = self.tag.text
        
        if self.raw_text:
            text_lines = self.raw_text.splitlines()

            length_of_lines = [len(li) for li in text_lines]
            length_longest_line = max(length_of_lines)
            index_of_longest_line = length_of_lines.index(length_longest_line)
            self.longest_line = text_lines[index_of_longest_line]

            self.text, self.lines = self.restructured_text(text_lines)

    def setup(self):

        if self.raw_text:

            if self.lines > 5:
                text = self.raw_text
                self.textView = QTextEdit()
                self.textView.setReadOnly(True)
                
                hh = abs(self.textView.fontMetrics().boundingRect(0, 0, self.textView.width(), -1, Qt.TextWrapAnywhere, text).height())

                if hh < 40: hh = 40
                elif hh > 150: hh = 150
                self.textView.setMinimumHeight(hh)

            else:
                self.textView = QLabel()
                self.textView.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

            self.textView.setAttribute(Qt.WA_TranslucentBackground)
            self.textView.setText(self.text)
            self.textView.setStyleSheet('font-family: Times New Roman; font-size: 14px')
            
            wbr = self.textView.fontMetrics().boundingRect(0, 0, 0, 0, 0, self.longest_line).width()
            
            if wbr > self.maxw:
                wbr = self.maxw
                if self.lines < 5: self.textView.setWordWrap(True)

            self.setMinimumWidth(wbr)
            self._layout.addWidget(self.textView)


class ImageType(MessageType):

    def  __init__(self, **kwargs):
        MessageType.__init__(self, space=5, margins=[], **kwargs)
    
    def sizeHint(self):
        w, h = self._size.toTuple()
        
        if self.tag.text:
            l = self.text.lines
            if l > 1:
                oh = (28 * l)
                h += oh
                self.text.setMinimumHeight(oh)
        return QSize(w, h)

    def init(self):
        data = b64decode(self.tag.data)
        self.ext = PRMP_ImageType.get(data=data)
        
        self._image = QImage.fromData(data, self.ext)
        
        w, h = self._image.size().toTuple()
        sc = 0
        maxw = 200

        if w > maxw:
            w = maxw
            sc = 1
        if h > maxw:
            h = maxw
            sc = 1
        
        self.scaled = self._image.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation) if sc else self._image
        self._pixmap = QPixmap(self.scaled)
        self._size = self.scaled.size()

    def setup(self):
        self.image = QLabel(self)
        self._layout.addWidget(self.image)

        if self.ext == 'gif':
            self.image_layout = QVBoxLayout(self.image)
            self.play_button = IconButton()
        
        if self.tag.text:
            self.text = TextType(parent=self, tag=Tag(**self.tag[['text', 'recipient', 'sender']]), maxw=self._size.width())
            self._layout.addWidget(self.text)
        
        self.image.setPixmap(self._pixmap)
        self.image.setFixedSize(self._size)


class AudioType(MessageType):

    def  __init__(self, **kwargs):
        MessageType.__init__(self, **kwargs)


class VideoType(MessageType):

    def  __init__(self, **kwargs):
        MessageType.__init__(self, **kwargs)


class DocumentType(MessageType):

    def  __init__(self, **kwargs):
        MessageType.__init__(self, **kwargs)


class ChatMessage(QFrame):
    SENT = '#08b7ff'
    RECEIVED = '#02dfa5'

    __style = '''
        border: 2px solid %s;
        border-top-right-radius: 10px;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        background-color: %s;
    '''

    def __init__(self, client, chat_object, tag, mst=None):
        QFrame.__init__(self)
        self.lay = SETUP_FRAME(obj=self, margins=[2, 2, 2, 2], orient='h', space=2)
        self.mst = mst

        self.client = client
        self.user = client.user
        self.chat_object = chat_object
        self.tag = tag

        self.timeFrame = self.iconLabel = self.dateTimeLabel = self.nameLabel = self.statusLabel = None

        self.defaults()
        
        self.setup()

        for a in [self.dateTimeLabel, self.nameLabel, self.statusLabel, self.timeFrame]:
            if a: a.setAttribute(Qt.WA_TranslucentBackground)
            
    def defaults(self):

        self._wid, self._layout = SETUP_FRAME(self.lay, re_obj=1, margins=[4, 4, 4, 4], space=2)
        
        self.maxw = self.mst.width() * .6

        self._sender = self.tag.sender == self.user.id
        
        chat = self.tag.chat


        if chat == CHAT.TEXT: self.messageFrame = TextType(tag=self.tag, maxw=self.maxw)
        elif chat == CHAT.AUDIO: self.messageFrame = AudioType(tag=self.tag, maxw=self.maxw)
        elif chat == CHAT.IMAGE: self.messageFrame = ImageType(tag=self.tag, maxw=self.maxw)
        elif chat == CHAT.VIDEO: self.messageFrame = VideoType(tag=self.tag, maxw=self.maxw)
        else: self.messageFrame = MessageType()

        if isinstance(self.chat_object, Contact): self.chatType = 1
        elif isinstance(self.chat_object, Group): self.chatType = 2
        elif isinstance(self.chat_object, Channel): self.chatType = 3

        self._style = self.SENT
        
        self.arrange_widgets()
        self.set_style()

        graphicEffect = QGraphicsDropShadowEffect(self)
        graphicEffect.setBlurRadius(2)
        self.setGraphicsEffect(graphicEffect)
    
    def arrange_widgets(self):
        self.timeFrame, self.timeFrameLayout = SETUP_FRAME(self._layout, orient='h', re_obj=1, space=3)
        self.timeFrame.setMinimumHeight(12)

        self.dateTimeLabel = QLabel()
        self.dateTimeLabel.setText(self.tag.get_date_time().toString("dd/MM/yy ... HH:mm:ss"))
        self.dateTimeLabel.setAlignment(Qt.AlignRight)
        self.dateTimeLabel.setStyleSheet('font-size: 10px')
        self.timeFrameLayout.addWidget(self.dateTimeLabel)
        
        if self._sender:
            self.align = Qt.AlignBottom | Qt.AlignRight
            self._style = self.SENT
            self.statusLabel = QLabel()
            self.statusLabel.setMaximumSize(20, 20)
            self.timeFrameLayout.addWidget(self.statusLabel)

        else:
            self.align = Qt.AlignBottom | Qt.AlignLeft
            self._style = self.RECEIVED

            if self.chatType == 2:
                self.iconLabel = IconButton(size=40)
                self.iconLabel.setStyleSheet('text-align: center; border-radius: 20px; background: %s'%STYLE.LIGHT_SHADE)
                self.iconLabel.mouseReleaseEvent = lambda e: None
                self.lay.insertWidget(0, self.iconLabel, Qt.AlignBottom)

                self.nameLabel = QLabel()
                self.nameLabel.setStyleSheet('font-family: impact; font-size: 15px')
                self._layout.addWidget(self.nameLabel)
        
        self._layout.addWidget(self.messageFrame)
        self._layout.addWidget(self.timeFrame)
            
    def set_style(self):
        self._wid.setStyleSheet('''
        border: 10px; 
        border-top-right-radius: 10px; 
        background: %s;
        color: black'''\
        %self._style)
        
        self.setStyleSheet(self.__style%(self._style, self._style))

    def setup(self):
        if self.chatType == 2 and not self._sender:
            chat_object = self.user.groups.get(self.tag.sender) or self.user.contacts.get(self.tag.sender)

            if chat_object and chat_object.icon: icon = chat_object.icon
            else: icon = None

            self.iconLabel.set_icon(icon)
            self.nameLabel.setText(chat_object.name)

    def update_(self):
        if self.statusLabel:
            if self.tag.sent: icon = 'chat_room/check.svg'
            else: icon = 'chat_room/clock.svg'
            pix = QIcon(f':{icon}').pixmap(12, 12)
            self.statusLabel.setPixmap(pix)

        if self.iconLabel:
            ...

    def showEvent(self, e=0):
        self.update_()
        # print(self.messageFrame.textView.width())
        # self._wid.setMinimumHeight(self.timeFrame.height()+self.messageFrame.height()+15)
    
    def resizeEvent(self, event):
        self.setMaximumWidth(self.maxw)


class ChatViewer(ScrolledWidget):

    def __init__(self, client: User, chat_object):
        ScrolledWidget.__init__(self, space=4, margins=[0, 0, 7, 7])

        self.client = client
        self.user = client.user
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
        tag = Tag(text=message, action=CHAT, chat=CHAT.TEXT, sender=self.user.id, recipient=self.chat_object.id, date_time=DATETIME(num=0), type=self.chat_object.className)

        self.user.add_chat(tag)

        self.add_tag(tag)

    def add_tag(self, tag):
        obj = ChatMessage(self.client, self.chat_object, tag, mst=self)
        self._chats_.append(obj)
        self._layout.addWidget(obj, 0, obj.align)
    
    def update_(self):
        for chat in self._chats_: chat.update_()


class ChatRoom(QFrame):

    def __init__(self, client, chat_object, profile, closeRoom,  emoji=None, sb=None):
        QFrame.__init__(self)
        self.client = client
        self.send_back = sb

        self.chat_object = chat_object
        self.profile = profile
        layout = SETUP_FRAME(obj=self, orient='v', space=2, margins=[2, 2, 2, 2])

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
    
    def showEvent(self, event):
        self.send_back(self.chat_object)
        self.profile.update_user(self.chat_object)


class ChatTab(QTabWidget):
    
    def __init__(self, client: Client, profile, send_back):
        QTabWidget.__init__(self)

        self.setMinimumWidth(450)

        self.profile = profile
        self._send_back = send_back
        self._chats_index_ = []
        self._chats_id_ = {}
        self.client = client
        self.user = client.user
        s = 28
        self.setIconSize(QSize(s, s))
        
        Emoji_Button.EMOJI_IMAGE = 1
        Emoji_Button.SET_SPRITE()
        self.emoji = Emoji_Ui()
        
        if self.user: self.add_chat_room(self.user.contacts['ade1'])
    
    def add_chat_room(self, chat_object):
        id = chat_object.id
        if id in self._chats_index_: index = self._chats_index_.index(id)
        else:
            w = ChatRoom(self.client, chat_object, self.profile, self.closeRoom, emoji=self.emoji, sb=self.send_back)
            
            icon = GET_ICON(chat_object.icon, ':chat_list/user.svg')
            self.addTab(w, icon, chat_object.name)
            self._chats_index_.append(id)
            self._chats_id_[id] = chat_object
            index = len(self._chats_index_) - 1
        self.setCurrentIndex(index)

    def closeRoom(self, chat_object):
        id = chat_object.id
        if self.count() <= 1: return 
        index = self._chats_index_.index(id)
        self.removeTab(index)
        self._chats_index_.remove(id)
        del self._chats_id_[id]
    
    def send_back(self, user): self._send_back(user)

