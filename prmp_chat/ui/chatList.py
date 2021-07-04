from prmp_chat.backend.client import Contact
from PySide6.QtCore import QMargins, QRect, QPoint, Qt, QRectF, QSize, QPointF, QDateTime
from PySide6.QtGui import QFontMetrics, QTextOption, QTextDocument, QColor, QFont, QStandardItem, QIcon
from PySide6.QtWidgets import QStyle
from prmp_chat.ui.listBase import Delegate, ListModel, ListView
from prmp_chat.backend.core import *



NameRole = Qt.UserRole + 1
DateTimeRole = Qt.UserRole + 2
unreadChatsRole = Qt.UserRole + 3

# for the chat room

class ChatRoomItem:
    def __init__(self, type='chat', tag=None, chatObject=None):
        self.type = type
        self.tag = tag
        self.chatObject = chatObject

        
        # date_time = self.chatObject.date_time
        # self.date_time = f'{DATE(date_time)}, {TIME(date_time)}'
    
    @property
    def data(self): return self.tag.data
    
    @property
    def sender(self): return self.tag.sender
    
    @property
    def date_time(self):
        date_time = self.chatObject.date_time
        date_time = f'{DATE(date_time)}_{TIME(date_time)}'
        return date_time


class ChatRoomDelegate(Delegate):
    
    BUBBLE_PADDING = QMargins(15, 5, 15, 5)
    TEXT_PADDING = QMargins(25, 15, 15, 15)
    BUBBLE_COLORS = {True: "#90caf9", False: "#a5d6a7"}

    offsetFactor = 10
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tagFont = QFont("Times", 8, QFont.Light)

    def _offset(self, rect): return rect.width()/self.offsetFactor
    def offset(self, rect): return rect.width()-self._offset(rect)

    def paint(self, painter, option, index):
        chatRoomItem = self.item(index)
        contentRect = option.rect

        if chatRoomItem.type == 'chat':
            offset = self.offset(contentRect)

            textRect = self.getFontMetrics(option).boundingRect(contentRect.left(), contentRect.top(), offset, 0, Qt.AlignLeft | Qt.AlignTop | Qt.TextWrapAnywhere, chatRoomItem.data)

            toption = QTextOption()
            toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

            sender = chatRoomItem.chatObject.user.id == chatRoomItem.sender

            h = 20 if sender else 10


            textBox = QRectF(contentRect.left(), contentRect.top(), textRect.right()+10, textRect.height()+h)

            # date_time
            date_time = chatRoomItem.date_time
            dateRect = QFontMetrics(self.tagFont).boundingRect(textRect.left(), textRect.top(), 0, 0, Qt.AlignLeft | Qt.AlignTop | Qt.TextSingleLine | Qt.TextDontClip, date_time)

            dateBox = QRectF(textBox.left(), textBox.bottom(), dateRect.width()+5, dateRect.height()+5)

            color = QColor(self.BUBBLE_COLORS[sender])
            painter.setBrush(color)

            if sender:
                textBox.moveTo(contentRect.width()-textBox.width()-15, textBox.top())
                dateBox.moveTo(textBox.right()-dateRect.width()-10, textBox.bottom())

                p1 = textBox.topRight() + QPointF(5, 0)
                points = p1 + QPoint(-5, 0), p1 + QPoint(10, 0), p1 + QPoint(0, 10)
                
            else:
                p1 = textBox.topLeft()
                textBox.moveTo(15, textBox.top())
                dateBox.moveTo(17, textBox.bottom())

                points = p1, p1 + QPoint(15, 0), p1 + QPoint(10, 10)

            painter.drawPolygon(points)
            
            textRect.moveTo(textBox.left()+5, textBox.top()+5)
            dateRect.moveTo(dateBox.left()+2, dateBox.top())
            dateRect.adjust(0, 0, 3, 0)

            painter.drawRoundedRect(textBox, 7, 7)
            # painter.drawRect(dateBox)
            painter.drawRoundedRect(dateBox, 5, 5)

            painter.setPen(Qt.black)
            painter.drawText(QRectF(textRect), chatRoomItem.tag.data, toption)
            painter.drawText(QRectF(dateRect), date_time)

            if sender:
                # draw chat status
                status = 'X' if chatRoomItem.tag.sent == False else '_/'
                rect = self.getFontMetrics(option).boundingRect(status)
                chatStatusRect = QRect(textBox.right()-rect.width()-5, textBox.bottom()-rect.height()-3, rect.width(), rect.height())
                # painter.drawRoundedRect(chatStatusRect, 7, 7)
                painter.drawText(QRectF(chatStatusRect), status)

    def sizeHint(self, option, index):
        chatRoomItem = self.item(index)
        sender = 25 if chatRoomItem.chatObject.user.id == chatRoomItem.tag.sender else 15

        if chatRoomItem.type == 'chat':
            fm = QFontMetrics(option.font)
            needed = fm.boundingRect(0, 0, option.rect.width(), 0, Qt.AlignLeft | Qt.AlignTop | Qt.TextWrapAnywhere, chatRoomItem.tag.data)
            return QSize(option.rect.width(), needed.height()+sender+25)

class ChatRoomListModel(ListModel): ...

class ChatRoomList(ListView):
    delegateClass = ChatRoomDelegate
    modelClass = ChatRoomListModel

    def add(self, type='chat', tag=None, chatObject=None):
        item = ChatRoomItem(type, tag, chatObject)
        self.addObject(item)
    
    def addObject(self, obj):
        super().addObject(obj)
        self.scrollToBottom()

    addChatItem = addObject




# for the chat listing

class ChatListItem(QStandardItem):
    def __init__(self, chatObject):
        self.chatObject = chatObject
        super().__init__(self.icon, self.last_chat)
        self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    
    @property
    def icon(self): return QIcon(self.chatObject.icon)
    
    @property
    def name(self): return self.chatObject.name
    
    @property
    def last_time(self): return self.chatObject.last_time
    
    @property
    def date(self):
        last_time = self.last_time
        if isinstance(last_time, int): last_time = DATETIME(last_time)
        if isinstance(last_time, QDateTime): return last_time.toString("yyyy-MM-dd")
    
    @property
    def time(self):
        last_time = self.last_time
        if isinstance(last_time, int): last_time = DATETIME(last_time)
        if isinstance(last_time, QDateTime): return last_time.toString("HH:mm:ss")

    @property
    def date_time(self): return f'{self.date}, {self.time}'
    
    @property
    def _last_chat(self): return self.chatObject.last_chat
    
    @property
    def last_chat(self):
        if self._last_chat: return self._last_chat.data
    
    @property
    def unread_chats(self): return self.chatObject.unread_chats
    
    @property
    def id(self): return self.chatObject.id

class ChatListDelegate(Delegate):
    chatChop = 20

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.iconSize = QSize(48, 48)
        self.margins = QMargins(8, 0, 8, 8)

        self.verticalSpacing = 12
        self.horizontalSpacing = 4
        self.textStart = self.margins.left() + self.iconSize.width() + self.horizontalSpacing

        self.tagFont = QFont("Times", 8, QFont.Light)
        self.nameFont = QFont("Times", 15, QFont.Bold)
        self.chatFont = QFont("Times", 11, QFont.Light)
    
    def nameRect(self, name): return self.textRect(name, self.nameFont)

    def tagRect(self, tag): return self.textRect(tag, self.tagFont)

    def chatRect(self, msg): return self.textRect(msg, self.chatFont)

    def paint(self, painter, option, index):
        self.initStyleOption(option, index)

        rect = option.rect
        contentRect = rect.adjusted(self.margins.left(), self.margins.top(), self.margins.right(), self.margins.bottom())

        painter.save()
        painter.setClipping(True)
        painter.setClipRect(rect)

        # if currently selected
        if option.state & QStyle.State_Selected:
            LIGHT = self.DARK
            DARK = self.LIGHT
            FORE = self.DARK
        else:
            LIGHT = self.LIGHT
            DARK = self.DARK
            FORE = self.FORE

        #   Draw background
        painter.fillRect(rect, DARK)

        chatListItem = self.item(index)
        # model = index.model()

        #   Draw bottom line
        # lastIndex = model.rowCount() - 1 == index.row()
        bottomEdge = rect.bottom()

        painter.setPen(LIGHT)
        painter.drawLine(rect.left(), bottomEdge, rect.right(), bottomEdge)

        #  Draw icon
        icon = chatListItem.icon

        if not icon.isNull():
            painter.drawPixmap(contentRect.left(), contentRect.top(), icon.pixmap(self.iconSize))

        #  Draw name text
        name = chatListItem.name
        namRect = self.nameRect(name)
        namRect.moveTo(self.textStart, contentRect.top())

        painter.setFont(self.nameFont)
        painter.setPen(FORE)
        painter.drawText(QRectF(namRect), Qt.TextSingleLine, name)

        #  Draw chat text
        chat = chatListItem.last_chat
        if chat:
            if len(chat) > self.chatChop:
                chat = ''.join(chat[:self.chatChop])
                chat += '...'

            msgRect = self.chatRect(chat)
            msgRect.moveTo(self.textStart, namRect.bottom() + self.verticalSpacing - self.margins.bottom()-4)

            painter.setFont(self.chatFont)
            painter.drawText(msgRect, Qt.TextSingleLine, chat)

        #  Draw date time
        painter.setFont(self.tagFont)
        chatObject = chatListItem.chatObject
        if isinstance(chatObject, Contact):
            status = 'ONLINE' if chatObject.status == STATUS.ONLINE else 'Last seen: ' + chatObject.str_last_seen
        else: status = 'Status'
    
        statusTextRect = self.tagRect(status)
        statusTextRect.moveTo(contentRect.right()-statusTextRect.width()-self.margins.right(), contentRect.top())

        painter.drawText(statusTextRect, Qt.TextSingleLine, status)

        time = 'Last time: ' + chatListItem.date_time
        timeTextRect = self.tagRect(time)
        timeTextRect.moveTo(contentRect.right()-timeTextRect.width()-self.margins.right(), contentRect.bottom()-timeTextRect.height()-self.margins.bottom())

        painter.drawText(timeTextRect, Qt.TextSingleLine, time)

        # Draw unreadChats
        count = chatListItem.unread_chats
        if count:
            countRect = self.tagRect(count)

            dy = (timeTextRect.top() - statusTextRect.bottom() - countRect.height()) / 2

            countRect.moveTo(contentRect.right()-countRect.width()-20, statusTextRect.bottom() + dy)

            ds = 2

            cont = QRect(countRect.x()-ds, countRect.y()-ds, countRect.width()+(ds*2), countRect.height()+ds)

            painter.setPen(Qt.white)

            painter.fillRect(cont,  DARK)

            painter.drawText(QRectF(countRect), Qt.TextSingleLine, str(count))
            painter.drawRoundedRect(cont, 2, 2)
        painter.restore()

    def sizeHint(self, option, index):
        self.initStyleOption(option, index)
        chatListItem = self.item(index)

        rect = self.tagRect(chatListItem.date)
        textHeight = rect.height() + self.verticalSpacing + self.chatRect(option.text).height()
        iconHeight = self.iconSize.height()
        height = textHeight if textHeight > iconHeight else iconHeight

        size = QSize(option.rect.width(), self.margins.top() + height + self.margins.bottom())
        return size

class ChatListModel(ListModel):...

class ChatList(ListView):
    delegateClass = ChatListDelegate
    modelClass = ChatListModel
    
    def addObject(self, obj):
        obj = ChatListItem(obj)
        super().addObject(obj)
        self.scrollToTop()

    add = addObject








