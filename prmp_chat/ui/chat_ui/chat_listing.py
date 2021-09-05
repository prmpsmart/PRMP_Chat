from base64 import b64decode
from ..widgets import *
from ...backend.client import *



class ChatLineEdit(QLineEdit):
    buttonClicked = Signal()
    
    def __init__(self, icon='', parent=None, completer=False, default_values=[], completer_sense=Qt.CaseInsensitive, callback=None, height=35, margin=4):
        QLineEdit.__init__(self, parent)
    
        self.default_values = default_values
        self.completer_sense = completer_sense
        self.callback = callback
        
        if completer or default_values: self.set_completer(default_values, completer_sense)

        self.button = None
        self.margin = margin
        self._height = height

        if icon:
            self.gw = height
            self.button = QPushButton(self)
            self.button.setIcon(QIcon(f':{icon}'))
            self.button.setToolTip('Go')

            self.set_style(self._style_colors)

            self.button.setCursor(Qt.ArrowCursor)
            self.button.clicked.connect(self.buttonClicked.emit)
            self.returnPressed.connect(self.button.click)
            self.buttonClicked.connect(self.call_callback)

        if self._height:
            self.setMinimumHeight(self._height)
            self.setMaximumHeight(self._height)
    
    @property
    def _style_colors(self): return (
        STYLE.LIGHT_SHADE,
        STYLE.DARK_SHADE, 
        STYLE.DARK,
        )

    def set_style(self, tup):
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
            % tup)
    
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
            g = (w-gw, mh+3, gw-3, gw-mh-10)
            # self.button.setIconSize(QSize(20, 20))
            # self.button.setMaximumHeight(gw)
            self.button.setFixedSize(QSize(27, 27))
            self.button.setGeometry(*g)

    resizeEvent = showEvent
    
    def clear_default_values(self): self.default_values = []

    def add_default_value(self, value): self.default_values.append(value)


class IconButton(ImageButton):
    def __init__(self, **kwargs):
        ImageButton.__init__(self, **kwargs)


class ChatWidget(QFrame):
    
    def __init__(self, chat_object:Chats, callback=None, index=0):
        QFrame.__init__(self)
        self.chat_object = chat_object

        self._style = 'border-radius: 5px; background: %s; color: %s'
        self.isCurrent = 0
        self.index = index

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

        self.icon = IconButton(offset=10)
        icon_layout.addWidget(self.icon)

        if isinstance(chat_object, Contact): self.status_bubble = QLabel(self.icon_frame)
        
        self.texts_frame, _ = SETUP_FRAME(mother_layout=layout, re_obj=1)

        self.name = QLabel(self.texts_frame)
        self.name.setGeometry(5, 0, 150, 20)
        self.name.setStyleSheet('font: bold 13.5pt')

        self.last_info = QLabel(self.texts_frame)
        self.last_info.setGeometry(5, 42, 150, 15)
        self.last_info.setStyleSheet('font: 8pt')

        self.date = QLabel(self.texts_frame)
        font = QFont()
        font.setPointSizeF(8)
        self.fm = QFontMetrics(font)
        self.date.setFont(font)

        self.unread_bubble = QLabel(self.texts_frame)
        font = QFont()
        font.setBold(1)
        self.unread_bubble.setFont(font)
        self.unread_bubble.setAlignment(Qt.AlignCenter)
        self.ufm = QFontMetrics(font)
        self.unread_bubble.setStyleSheet('background: green; border-radius: 5px; color: white')

        self.time = QLabel(self.texts_frame)
        font = QFont()
        font.setPointSizeF(8)
        self.tfm = QFontMetrics(font)
        self.time.setFont(font)

        self.leaveEvent(0)
        self.update_chat_widget()
    
    def update_chat_widget(self):
        
        self.name.setText(self.chat_object.name)

        if isinstance(self.chat_object, Contact):
            self.status_bubble.setStyleSheet(f'background: {"green" if self.chat_object.status == STATUS.ONLINE else "gray"}; border-radius: 5px; color: white')
            
            self.status_bubble.setToolTip(self.chat_object.status)
        
        self.icon.set_icon(self.chat_object.icon)
        
        date_time = self.chat_object.last_time
        date = date_time.toString('dd/MM/yy')
        
        self.date.setText(date)
        self.dbr = self.fm.boundingRect(date)
        
        time = date_time.toString('HH:mm:ss')
        self.time.setText(time)
        self.tbr = self.tfm.boundingRect(time)

        unread = str(self.chat_object.unread_chats)
        self.unread_bubble.setText(unread)
        self.ubr = self.ufm.boundingRect(unread)
        
        last_chat = self.chat_object.last_chat
        if last_chat:
            last_text = last_chat.text
            if last_text:
                if len(last_text) > 50: last_text = ''.join(last_text[:50])
                self.last_info.setText(last_text + '...')
    
    def enterEvent(self, event):
        if not self.isCurrent: self.setStyleSheet(self._style % (STYLE.LIGHT, STYLE.DARK))

        self.icon.setStyleSheet('background: %s'%STYLE.LIGHT_SHADE)
        
    def leaveEvent(self, event=0):
        if not self.isCurrent: self.setStyleSheet(self._style % (STYLE.DARK_SHADE, STYLE.LIGHT))
        
        self.icon.setStyleSheet('background: %s'%STYLE.LIGHT)
    
    def uncheck(self):
        self.isCurrent = 0
        self.leaveEvent()

    def mouseReleaseEvent(self, event):
        if not self.isCurrent: self.callback(self)

    def check(self):
        self.isCurrent = 1
        self.setStyleSheet(self._style % (STYLE.DARK, STYLE.LIGHT))
        
        self.icon.setStyleSheet('background: %s'%STYLE.LIGHT)

    def showEvent(self, event):
        w = self.icon_frame.width()
        h = self.icon_frame.width()
        
        if isinstance(self.chat_object, Contact): self.status_bubble.setGeometry(w-12, h-12, 10, 10)

        w = self.texts_frame.width()
        h = self.texts_frame.height()

        self.date.setGeometry(w-self.dbr.width()-6, 0, self.dbr.width(), self.dbr.height())
        
        if self.chat_object.unread_chats: self.unread_bubble.setGeometry(w-self.ubr.width()-12,  (h-self.ubr.height())/2, self.ubr.width()+6, self.ubr.height()+3)

        else: self.unread_bubble.hide()
        
        self.time.setGeometry(w-self.tbr.width()-6, 48, self.tbr.width(), self.tbr.height())
    
    resizeEvent = showEvent


class ChatsList(ScrolledWidget):

    def __init__(self, tab, user, attr='contacts', callback=None):
        ScrolledWidget.__init__(self, tab, space=2, margins=[2, 2, 2, 2])
        self._layout.setAlignment(Qt.AlignTop)
        self.set_bars_off()
        self.current = None
        self._callback = callback
        self.user = user
        self.attr = attr

        self._chats_objects_ = {}

        self.setStyleSheet('background: url(:chat_room/wallpaper14.png) center')

        self.fill()

    def add_chat_object(self, chat_object):
        chat = ChatWidget(chat_object, callback=self.callback, index=self._layout.count())
        self._layout.addWidget(chat)
        self._chats_objects_[chat_object] = chat

    def fill(self):
        if self.user:
            manager = getattr(self.user, self.attr, None)
            if manager:
                for obj in manager.objects: self.add_chat_object(obj)

    def callback(self, chat_widget: ChatWidget, q=1):
        if self.current:
            try: self.current.uncheck()
            except: ...

        self.current = chat_widget
        # self._layout.insertWidget(0, self.current)
        if q: self._callback(chat_widget.chat_object)
        self.current.check()
    
    def showEvent(self, event):
        if self.current: self.callback(self.current)
    
    def set_current_object(self, chat_object):
        widget = self._chats_objects_.get(chat_object)
        if widget: self.callback(widget, q=0)

    def update_list(self):
        for v in self._chats_objects_.values(): v.update_chat_widget()



class SearchList(ChatsList):

    def __init__(self, tab, **kwargs):
        super().__init__(tab, **kwargs)

        self.chats_objects = [*self.user.users[:], *self.user.groups[:], *self.user.channels[:]]
        self.searched_objects = []
    
    def clear(self):
        dd = list(self._chats_objects_.items())
        for a, b in dd:
            b.deleteLater()
            del self._chats_objects_[a]
        self.searched_objects = []
    
    def add_searched_objects(self, so):
        if so in self.searched_objects: return
        self.searched_objects.append(so)

    def search(self, text):
        self.clear()

        if not text: return

        for co in self.chats_objects:
            if text in co.name.lower() or text in co.id.lower(): self.add_searched_objects(co)

            else:
                for chat in co.chats:
                    if text in chat.text.lower():
                        self.add_searched_objects(co)
                        break
        
        for so in self.searched_objects: self.add_chat_object(so)

        if not self.searched_objects: self.clear()
