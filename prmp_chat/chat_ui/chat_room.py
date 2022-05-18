import os, math
from html.parser import HTMLParser
import re
from turtle import width

from .emoji_ui import *
from .chat_listing import *
from .details import *
from .mimi_plarec import Player, Recorder, QAudio
from .call import Call_Dialog

DE_PATTERN = re.compile("(:[A-zÀ-ÿ0-9\\-_&.’”“()! #*+?–]+:)")


def DE_EMOJIZE(text):
    def replace(match: re.Match):
        hexcode = match.group(1).replace(":", "")
        path = f":emoji_icons/{hexcode}.png"
        n = 20
        html = f"<img src={path} width={n} height={n}/> "
        return html

    de = DE_PATTERN.sub(replace, text)
    return de


class TextParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._pretty = ""
        self._textout = ""
        self.paragraph = False

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for x in attrs:
                if x[0] == "src":
                    self._pretty += f'<img src="{x[1]}"/>'
                    self._textout += ":{}:".format(x[1].split("/")[-1].split(".")[0])
        elif tag == "p":
            self.paragraph = True

    def handle_endtag(self, tag):
        if tag == "p":
            self._pretty += "\n"
            self._textout += "\n"
            self.paragraph = False

    def handle_data(self, data):
        if self.paragraph:
            self._pretty += data
            self._textout += data

    def produce(self):
        temp = self._textout.strip()
        temp2 = self._pretty.strip()
        self._pretty = ""
        self._textout = ""
        return temp, temp2


class ChatRoomH_F(QPushButton):
    def __init__(self, w=5):
        super().__init__()
        self._w = w
        self.leaveEvent(0)

        self.setMinimumHeight(50)
        self.setMaximumHeight(50)

    @property
    def _style_colors(self):
        return
        return (
            STYLE.DARK,
            STYLE.LIGHT,
            self._w,
            STYLE.DARK_SHADE,
            STYLE.LIGHT_SHADE,
        )

    def set_style(self, tup):
        return
        self.setStyleSheet(
            """
            QWidget{
                background: %s;
                color: %s;
                border-radius: %d
                }
            ImageButton::hover{
                background: %s;
                }
            QPushButton::pressed{
                background: %s;
                }
            """
            % tup
        )

    def enterEvent(self, event):
        self.set_style(
            (
                STYLE.DARK,
                STYLE.LIGHT,
                self._w,
                STYLE.LIGHT_SHADE,
                STYLE.LIGHT,
            )
        )

    def leaveEvent(self, event):
        self.set_style(self._style_colors)


class Chat_Menu(QDialog):
    def __init__(
        self,
        parent=None,
        closeRoom=None,
        header: "ChatHeader" = None,
    ) -> None:
        super().__init__(parent, f=Qt.Popup)

        self.setMinimumSize(QSize(100, 225))
        self.setMaximumSize(QSize(100, 225))

        self.header = header

        self.chat_viewer: ChatViewer = header.chat_viewer
        self.chat_object = self.chat_viewer.chat_object

        self.layout_ = QVBoxLayout(self)

        info = QPushButton("Info")
        info.clicked.connect(self.info)
        self.layout_.addWidget(info)

        search = QPushButton("Search")
        search.clicked.connect(self.search)
        self.layout_.addWidget(search)

        photos = QPushButton("Photos")
        photos.clicked.connect(self.photos)
        self.layout_.addWidget(photos)

        clearChat = QPushButton("Clear Chat")
        clearChat.clicked.connect(self.clearChat)
        self.layout_.addWidget(clearChat)

        block = QPushButton("Block")
        block.clicked.connect(self.block)
        # self.layout_.addWidget(block)

        delete = QPushButton("Delete")
        delete.clicked.connect(self.delete)
        self.layout_.addWidget(delete)

        if not isinstance(self.chat_object, Contact):
            exitGroup = QPushButton("Exit")
            exitGroup.clicked.connect(self.exit)
            self.layout_.addWidget(exitGroup)

        self._closeRoom = closeRoom
        close = QPushButton("Close")
        close.clicked.connect(self.closeRoom)
        self.layout_.addWidget(close)

    def info(self):
        self.header.mousePressEvent(0)
        if self.isVisible():
            self.close()

    def search(self):
        self.close()

    def clearChat(self):
        self.chat_viewer.clear()
        self.chat_object.chats.clear()
        self.close()

    def photos(self):
        self.close()

    def block(self):
        self.close()

    def delete(self):
        self.close()

    def exit(self):
        if isinstance(self.chat_object, Group):
            ...
        else:
            ...
        self.close()

    def closeRoom(self):
        self._closeRoom(0)
        self.close()


class ChatHeader(ChatRoomH_F):
    def __init__(
        self,
        chat_room: "ChatRoom",
        closeRoom,
        show_info: Callable[[Union[Contact, Multi_Users]], None],
    ):
        ChatRoomH_F.__init__(self)

        self.chat_room = chat_room
        self.chat_viewer = chat_room.chat_viewer
        self.chat_object = self.chat_viewer.chat_object
        self.call_dialog: Call_Dialog = chat_room.chat_tab.home.call_dialog
        self.show_info = show_info

        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        width = 50
        self.imageButton = ImageButton(
            GET_DEFAULT_ICON(self.chat_object), size=width, mask=width * 2
        )
        self.layout_.addWidget(self.imageButton)
        self.imageButton.clicked.connect(self.iconClicked)

        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)

        self.name = QLabel("Apata Miracle Peter")
        self.name.setStyleSheet(FONT_FORMAT(size=22, weight="bold"))

        vlayout.addWidget(self.name)

        self.status = QLabel("OFFLINE")
        self.status.setStyleSheet(FONT_FORMAT(size=12))
        vlayout.addWidget(self.status)

        self.layout_.addLayout(vlayout)

        if isinstance(self.chat_object, Contact) and 0:
            self.voiceButton = IconButton(
                icon="phone", parent=self, size=50, tip="Voice Call"
            )
            self.voiceButton.clicked.connect(self.voice_call)
            self.layout_.addWidget(self.voiceButton)

            self.videoButton = IconButton(
                icon="video", parent=self, size=50, tip="Video Call"
            )
            self.videoButton.clicked.connect(self.video_call)
            self.layout_.addWidget(self.videoButton)

        self.menuButton = IconButton(icon="menu", parent=self, size=50, tip="Menu")
        self.menuButton.clicked.connect(self.openMenu)
        self.layout_.addWidget(self.menuButton)

        self._menu = Chat_Menu(
            self.menuButton,
            closeRoom=closeRoom,
            header=self,
        )

        self.update_status()
        self.update_icon()

    def video_call(self):
        self.showCall(True)

    def voice_call(self):
        self.showCall(False)

    def showCall(self, isVideo: bool):
        if (
            self.chat_room.chat_tab.home.client.online
            and self.chat_object.status == STATUS.ONLINE
        ):
            if not self.call_dialog.isVisible():
                self.call_dialog.send_request(self.chat_object, isVideo)
                self.call_dialog.show()
            else:
                QMessageBox.critical(self, "ONGOING CALL", "There is an ongoing call.")
        else:
            QMessageBox.critical(self, "OFFLINE", "Call cannot be made!")

    def mousePressEvent(self, event):
        self.show_info(self.chat_object)

    def update_status(self):
        w = 60

        self.name.setText(self.chat_object.get_name())
        if self.chat_object.user.status == STATUS.ONLINE:
            self.status.show()
            status = ""

            if isinstance(self.chat_object, Contact):
                status = "ONLINE"
                if self.chat_object._status != STATUS.ONLINE:
                    date_time = self.chat_object.last_seen
                    status = (
                        date_time.toString(OFFLINE_FORMAT) if date_time else "OFFLINE"
                    )

            self.status.setText(status)

        else:
            self.status.hide()

    def update_icon(self):
        self.imageButton.set_icon(self.chat_object.icon)

    def openMenu(self):

        win = self.window()
        win_geo = win.geometry()
        menu_geo = self._menu.geometry()

        x = win_geo.x() + win_geo.width() - menu_geo.width()
        y = win_geo.y() + self.menuButton.y() + self.menuButton.height()

        self._menu.move(x, y)
        self._menu.show()

    def showEvent_(self, e):
        h = self.height()
        w = 60

        y = abs((h - w) / 2)
        self.imageButton.setGeometry(5, 2.5, w, w)

        d = 20
        w -= d
        dd = w - d - d

        self.menu.setGeometry(self.width() - w - 5, y, dd, w)

    def iconClicked(self):
        print("iconClicked")


class TextInput(QTextEdit):
    def __init__(self, parent=None, callback=None, container: QWidget = None):
        QTextEdit.__init__(self, parent)

        self.container = container
        self.parser = TextParser()

        self.setPlaceholderText("Type a message ...")

        self.setStyleSheet("font-size: 14;")

        self.setMinimumHeight(40)
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut.activated.connect(callback)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTextInputSize()

    def setTextInputSize(self):
        br = self.fontMetrics().boundingRect(
            0, 0, self.width(), -1, Qt.TextWrapAnywhere, self.toPlainText()
        )
        h = br.height()
        hh = abs(h)

        if hh < 40:
            hh = 40
        elif hh > 200:
            hh = 200

        hh += 10
        if self.container:
            hh += 250 if self.container._emoji_on else 0
            self.container.setMinimumHeight(hh)
            self.container.setMaximumHeight(hh)

    def input_emoji(self, emoji: Emoji):
        path = f":emoji_icons/{emoji.hexcode}.png"
        n = 20
        html = f"<img src={path} width={n} height={n}/> "
        self.insertHtml(html)
        self.setTextInputSize()

    @property
    def text(self) -> str:
        return self.toPlainText().strip()

    @property
    def message(self) -> str:
        html = self.toHtml()
        self.parser.feed(html)
        message = self.parser.produce()

        actual = emoji.emojize(message[0], use_aliases=True)  # this is what we'll send
        return actual

    def keyReleaseEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Backspace:
            ...

        self.setTextInputSize()


class VoiceRecorder(QFrame):
    def __init__(self, footer: "ChatFooter") -> None:
        super().__init__()
        self.footer = footer

        self.record_stopWatch = StopWatch()
        self.play_stopWatch = StopWatch()

        self.player = Player(stateReceiver=self.playState)
        self.recorder = Recorder(stateReceiver=self.recordState)
        self.byteArray = QByteArray()

        layout = SETUP_FRAME(obj=self, orient="h", margins=[2, 2, 2, 2])

        w = 40

        close = IconButton(icon="close", size=w)
        close.clicked.connect(self.close)
        layout.addWidget(close)

        self.recorded = QLabel("Recorded Bytes")
        self.recorded.setMaximumHeight(w)
        self.recorded.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.recorded)

        timeLay = QFormLayout()
        timeLay.setContentsMargins(2, 5, 2, 2)
        timeLay.setLabelAlignment(Qt.AlignBottom | Qt.AlignCenter)
        timeLay.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        layout.addLayout(timeLay)

        self.record_time = QLabel("00:00:00")
        self.record_time.setMaximumWidth(90)
        self.record_time.setAlignment(Qt.AlignCenter)
        timeLay.addRow("Rec : ", self.record_time)

        self.play_time = QLabel("00:00:00")
        self.play_time.setMaximumWidth(90)
        self.play_time.setAlignment(Qt.AlignCenter)
        timeLay.addRow("Play : ", self.play_time)

        self._recordStop = IconButton(icon="record", size=w)
        self._recordStop.clicked.connect(self.recordStop)
        layout.addWidget(self._recordStop)

        self._playPause = IconButton(icon="play", size=w)
        self._playPause.clicked.connect(self.playPause)
        layout.addWidget(self._playPause)

        send = IconButton(icon="send", size=w)
        send.clicked.connect(self.send)
        layout.addWidget(send)

        self.recording_timer = QTimer()
        self.recording_timer.setInterval(10)
        self.recording_timer.timeout.connect(self.update_recording_details)

        self.playing_timer = QTimer()
        self.playing_timer.setInterval(10)
        self.playing_timer.timeout.connect(self.updatePlayTime)

    def update_recorded(self):
        size = self.byteArray.size()
        self.recorded.setText(f"{size} B")

    def updatePlayTime(self):
        timeString = self.play_stopWatch.timeString
        self.play_time.setText(timeString)

    def updateRecordTime(self):
        timeString = self.record_stopWatch.timeString
        self.record_time.setText(timeString)

    def update_recording_details(self):
        self.update_recorded()
        self.updateRecordTime()

    def playState(self, state: QAudio.State):
        if state == QAudio.State.ActiveState:
            self.play_stopWatch.start()
            self.playing_timer.start()
            self._playPause.set_icon("pause")
            self._recordStop.setEnabled(0)

        else:
            self.playing_timer.stop()
            self.play_stopWatch.reset()
            self._playPause.set_icon("play")
            self._recordStop.setEnabled(1)

        self.updatePlayTime()

    def recordState(self, state: QAudio.State):
        if state == QAudio.State.ActiveState:
            self.record_stopWatch.start()
            self.recording_timer.start()
            self._recordStop.set_icon("stop")
            self._playPause.setEnabled(0)

        elif state == QAudio.State.StoppedState:
            self.recording_timer.stop()
            self.record_stopWatch.pause()
            self._recordStop.set_icon("record")
            self._playPause.setEnabled(1)

        self.update_recording_details()

    def playPause(self):
        if self.player.active:
            self.player.stop()
        elif self.byteArray.size():
            self.player.play(byteArray=self.byteArray)

    def recordStop(self):
        if self.recorder.active:
            self.recorder.stop()
        else:
            self.byteArray = self.recorder.record(byteArray=self.byteArray)

    def resetStopWatch(self):
        self.record_time.setText("00:00:00")
        self.stopWatch.reset()

    def send(self):
        if self.byteArray.size():
            self.footer.chat_viewer.add_audio(self.byteArray.data())

    def closeEvent(self, e):
        self.player.stop()
        self.recorder.stop()
        self.byteArray.clear()
        self.play_stopWatch.reset()
        self.play_time.setText("00:00:00:00")
        self.record_stopWatch.reset()
        self.record_time.setText("00:00:00:00")
        self.update_recorded()
        self.footer.toggle_voice_note_recorder()

    hideEvent = closeEvent


class SendImagePreview(CropImage):
    def __init__(self, footer: "ChatFooter", image: str, parent=None, **kwargs):
        super().__init__(image, f=Qt.Tool, parent=parent, title="Send Image", **kwargs)

        self.footer = footer
        self.actions_frame.hide()

        frame = QFrame()
        frame._emoji_on = False
        hlay = QHBoxLayout(frame)
        SET_MARGINS(hlay, 0)

        self.message = TextInput(callback=self.send_message, container=frame)
        self.message.setTextColor("black")
        hlay.addWidget(self.message, Qt.AlignBaseline)

        self.send = IconButton(icon="send", size=40, tip="Send a message (Ctrl+Enter)")
        self.send.clicked.connect(self.send_message)
        hlay.addWidget(self.send)

        self.layout().addWidget(frame)

        self.show()

    def send_message(self):
        image = self.view.selected_image or self.image
        if image:
            image_data = GET_IMAGE_DATA(image)
            text = self.message.message
            self.footer.chat_viewer.add_image(image_data, text)

            self.close()


class ChatFooter(ChatRoomH_F):
    def __init__(self, chat_tab: "ChatTab", chat_viewer: "ChatViewer" = None):
        ChatRoomH_F.__init__(self, 5)

        self.w = 40

        self.chat_viewer = chat_viewer
        self.chat_tab = chat_tab
        self._emoji_on = False

        self.imageChooser = ImageChooser(self.addImage, self)

        layout = SETUP_FRAME(obj=self)
        self.text_messaging = SETUP_FRAME(layout, orient=0)
        self.voice_note_recorder = SETUP_FRAME(
            layout, orient=0, klass=VoiceRecorder, footer=self
        )
        self.voice_note_recorder.hide()

        hlayout = QHBoxLayout(self.text_messaging)
        hlayout.setAlignment(Qt.AlignTop)
        SET_MARGINS(hlayout, 5)

        self.emoji = IconButton(icon="emoji", size=self.w)
        self.emoji.clicked.connect(self.show_emoji)
        hlayout.addWidget(self.emoji)

        self.message = TextInput(callback=self.send_message, container=self)
        self.message.textChanged.connect(self.toggle_send_voice)
        self.message.setTextColor("black")
        hlayout.addWidget(self.message)

        self.add_image = IconButton(icon="image", size=self.w)
        self.add_image.clicked.connect(self.imageChooser.show)
        hlayout.addWidget(self.add_image)

        self.send = IconButton(
            icon="send", size=self.w, tip="Send a message (Ctrl+Enter)"
        )
        self.send.clicked.connect(self.send_message)
        self.send.hide()
        hlayout.addWidget(self.send)

        self.microphone = IconButton(
            icon="microphone", size=self.w, tip="Send Voice Note"
        )
        self.microphone.clicked.connect(self.toggle_voice_note_recorder)
        hlayout.addWidget(self.microphone)

        self.toggle_voice_note_recorder()

    def show_emoji(self):
        emoji = self.chat_tab.emoji
        h = 50
        if self._emoji_on:
            self._emoji_on = False
            emoji.hide()
        else:
            h = 250
            self._emoji_on = True
            lay = self.layout()
            lay.addWidget(emoji)
            emoji.show()

        self.setMinimumHeight(h)
        self.setMaximumHeight(h)

    def addImage(self, image: QImage):
        SendImagePreview(footer=self, image=image, parent=self)

    def toggle_send_voice(self):
        if self.message.toPlainText():
            self.microphone.hide()
            self.send.show()
        else:
            self.microphone.show()
            self.send.hide()

    def toggle_voice_note_recorder(self):
        if self.text_messaging.isVisible():
            self.text_messaging.hide()
            self.voice_note_recorder.show()
        else:
            self.text_messaging.show()
            self.voice_note_recorder.hide()

    def add_emoji(self, emoji: Emoji):
        self.message.input_emoji(emoji)
        # self.message.insertPlainText(emoji.emoji)
        # self.message.setTextInputSize()

    def send_message(self):
        if not self.chat_viewer:
            return

        message = self.message.message
        if message:
            self.chat_viewer.add_message(message)

        self.message.clear()


class MessageType(QFrame):
    TYPE = 0

    def __init__(
        self, chatMessage=None, space=5, margins=[5, 5, 5, 5], tag: Tag = None, maxw=0
    ):
        QFrame.__init__(self)

        self.chatMessage = chatMessage
        self.tag = tag
        self.maxw = maxw
        self.setMaximumWidth(self.maxw)
        self._layout = SETUP_FRAME(obj=self, space=space, margis=margins)

        self.init()
        self.setup()

    def init(self):
        ...

    def setup(self):
        ...


class TextType(MessageType):
    max_letters_per_line = 64

    def __init__(self, **kwargs):
        MessageType.__init__(self, space=0, margins=[], **kwargs)

    def setup(self):
        text = self.tag.text

        if text:

            self.textView = QLabel()
            self._layout.addWidget(self.textView)

            self.textView.setStyleSheet(FONT_FORMAT(15))
            self.textView.setTextInteractionFlags(
                Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse
            )
            self.textView.setWordWrap(True)
            self.textView.setText(text)

            if self.tag.type == TYPE.CHANNEL:
                self.textView.setAlignment(Qt.AlignCenter)

            boundingRect: QRect = self.textView.fontMetrics().boundingRect(text)

            width = boundingRect.width()
            height = boundingRect.height()

            for ch in text:
                if ord(ch) > 200:
                    height += 30
                    break

            self.textView.setMinimumSize(width, height)


class ImageView(QDialog):
    def __init__(self, parent):
        super().__init__(parent, f=Qt.Popup)

        self.setWindowTitle("IMAGE ")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self._pixmap: QPixmap = None
        self.image = QLabel()
        layout.addWidget(self.image, Qt.AlignCenter)

        self.button = QPushButton("Save")
        self.button.clicked.connect(self.save)
        layout.addWidget(self.button)

        w = 515
        self.setMinimumSize(w, w - 100)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        self.set = 0

    def setImage(self, _pixmap: QPixmap):
        self._pixmap = _pixmap
        self.set = 0

    def save(self):
        file = QFileDialog.getSaveFileName(
            self,
            "Choose Image ",
            "",
            f"Image files (*.png)",
        )[0]

        if file:
            self._image.save(file)

    def showEvent(self, event):
        w = h = 500
        cm = self.layout().contentsMargins()
        l, t, r, b = cm.left(), cm.top(), cm.right(), cm.bottom()
        bh = self.button.height()
        sp = self.layout().spacing()

        h = h - t - b - sp - bh
        w = w - l - r

        if self._pixmap:
            _pixmap = self._pixmap.scaled(
                w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            self.image.setPixmap(_pixmap)
            w, h = _pixmap.size().toTuple()
            h += bh + sp

            QTimer.singleShot(100, lambda: self.res(w, h))

    def res(self, w, h):
        if not self.set:
            self.setMinimumSize(w, h)
            self.setMaximumSize(w, h)
            self.set = 1

    resizeEvent = showEvent


class ImageType(MessageType):
    def __init__(self, image_view: ImageView, **kwargs):
        self._image: QImage = None
        self.image_view = image_view
        self._size: QSize = None
        MessageType.__init__(self, space=5, margins=[], **kwargs)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.image_view.setImage(self._image)
        window = self.window()
        if not window.isMaximized():
            self.image_view.setGeometry(*event.globalPos().toTuple(), 1, 1)
        else:
            self.image_view.setGeometry(
                *(window.rect().center() - self.image_view.rect().center()).toTuple(),
                1,
                1,
            )

        self.image_view.show()

    def sizeHint(self) -> QSize:
        w, h = self._size.toTuple()

        if self.tag.text:
            h += 28
            self.text.setMinimumHeight(28)
        return QSize(w, h)

    def init(self):
        self._image = GET_PIXMAP(self.tag.raw_data, "lock", mobile=self.tag.mobile)

        w, h = self._image.size().toTuple()
        sc = 0
        maxw = 250

        if w > maxw:
            w = maxw
            sc = 1
        if h > maxw:
            h = maxw
            sc = 1

        self.scaled = (
            self._image.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            if sc
            else self._image
        )
        self._pixmap = QPixmap(self.scaled)
        self._size = self.scaled.size()

    def setup(self):
        self.image = QLabel(self)
        self._layout.addWidget(self.image)

        if self.tag.text:
            self.text = TextType(
                tag=Tag(**self.tag[["text", "recipient", "sender"]]),
                maxw=self._size.width(),
            )
            self._layout.addWidget(self.text)

        self.image.setPixmap(self._pixmap)
        self.image.setFixedSize(self._size)

    def showEvent(self, event: QShowEvent):
        self.setMinimumSize(self.sizeHint())
        super().showEvent(event)


class AudioType(MessageType):
    def __init__(self, **kwargs):
        MessageType.__init__(self, space=5, margins=[0, 0, 0, 0], **kwargs)

    def init(self):

        self.play_stopWatch = StopWatch()

        self.player = Player(stateReceiver=self.playState)
        self.byteArray = QByteArray(self.tag.raw_data)

        self.playing_timer = QTimer()
        self.playing_timer.setInterval(10)
        self.playing_timer.timeout.connect(self.updatePlayTime)

    def setup(self):
        w = 40

        hlay = QHBoxLayout()
        SET_MARGINS(hlay, 4)
        hlay.setSpacing(0)
        self._layout.addLayout(hlay)

        self._layout.setSpacing(0)

        self._playPause = IconButton("play", size=w)
        self._playPause.clicked.connect(self.playPause)
        hlay.addWidget(self._playPause)

        self.time = (
            QTime(0, 0, 0, 0)
            .addSecs(self.player.duration(self.byteArray.data()))
            .toString("HH:mm:ss")
        )

        self.play_time = QLabel(self.time)
        self.play_time.setMaximumSize(90, w)
        self.play_time.setAlignment(Qt.AlignCenter)
        hlay.addWidget(self.play_time)

    def updatePlayTime(self):
        timeString = self.play_stopWatch.timeString if self.player.active else self.time
        self.play_time.setText(timeString)

    def playPause(self):
        if self.player.active:
            self.player.stop()
        elif self.byteArray.size():
            self.player.play(byteArray=self.byteArray)

    def playState(self, state: QAudio.State):
        if state == QAudio.State.ActiveState:
            self._playPause.set_icon("pause")
            self.play_stopWatch.start()
            self.playing_timer.start()

        else:
            self._playPause.set_icon("play")
            self.play_stopWatch.reset()
            self.playing_timer.stop()

        self.updatePlayTime()


class VideoType(MessageType):
    def __init__(self, **kwargs):
        MessageType.__init__(self, space=5, margins=[], **kwargs)


class ChatContextMenu(QDialog):
    def __init__(self, chat_message: "ChatMessage"):
        super().__init__(chat_message, f=Qt.Popup)

        self.chat_message = chat_message

        layout = QVBoxLayout(self)
        SET_MARGINS(layout, 5)
        layout.setSpacing(2)

        if chat_message.tag["sender"] == chat_message.user.id:
            resend = QPushButton("Resend")
            resend.clicked.connect(self.resend)
            layout.addWidget(resend)

        forward = QPushButton("Forward")
        forward.clicked.connect(self.forward)
        layout.addWidget(forward)

        delete = QPushButton("Delete")
        delete.clicked.connect(self.delete)
        layout.addWidget(delete)

    def resend(self):
        self.close()
        self.chat_message.resend()

    def forward(self):
        self.close()

    def delete(self):
        self.close()
        self.chat_message.delete()

    def show(self, event: QMouseEvent):
        self.setGeometry(*event.globalPos().toTuple(), 1, 1)
        super().show()


class ChatMessage(QFrame):
    SENT = "#08b7ff"
    RECEIVED = "#02dfa5"

    __style = """
        border: 2px solid %s;
        border-top-right-radius: 10px;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        background-color: %s;
    """

    def __init__(self, client, chat_widget: ChatWidget, tag, chat_viewer: "ChatViewer"):
        QFrame.__init__(self)

        m = 2
        self.lay = SETUP_FRAME(obj=self, orient="h", space=0, margins=[m, m, m, 0])
        self.chat_viewer = chat_viewer

        self.client = client
        self.user = client.user
        self.chat_widget = chat_widget
        self.tag = tag

        self.context_menu = ChatContextMenu(self)

        self.timeFrame = (
            self.iconLabel
        ) = self.dateTimeLabel = self.nameLabel = self.statusLabel = None

        self.defaults()

    @property
    def maxw(self):
        return self.chat_viewer.width() * 0.5

    def defaults(self):
        m = 2
        self._wid, self._layout = SETUP_FRAME(
            self.lay, re_obj=1, margins=[m, m, 0, m * 2], space=0
        )

        self.isSender = self.tag.sender == self.user.id
        self._style = self.SENT if self.isSender else self.RECEIVED

        chat = self.tag.chat
        type = self.tag.type
        action = self.tag.action

        if chat == CHAT.TEXT:
            self.messageFrame = TextType(chatMessage=self, tag=self.tag, maxw=self.maxw)
        elif chat == CHAT.IMAGE:
            self.messageFrame = ImageType(
                chatMessage=self,
                tag=self.tag,
                maxw=self.maxw,
                image_view=self.chat_viewer.image_view,
            )
        elif chat == CHAT.AUDIO:
            self.messageFrame = AudioType(
                chatMessage=self, tag=self.tag, maxw=self.maxw
            )
            ...
        elif chat == CHAT.VIDEO:
            self.messageFrame = VideoType(
                chatMessage=self, tag=self.tag, maxw=self.maxw
            )
            ...

        if (action == ACTION.CHAT) and (type != TYPE.CHANNEL):
            alignSide = Qt.AlignRight if self.isSender else Qt.AlignLeft
            self.align = Qt.AlignBottom | alignSide
        else:
            self.align = Qt.AlignCenter | Qt.AlignTop

        self.arrange_widgets()
        self.set_style()

    def arrange_widgets(self):
        m = 2
        self.timeFrame, self.timeFrameLayout = SETUP_FRAME(
            self._layout, orient="h", re_obj=1, space=3, margins=[m, m, m, 0]
        )
        self.timeFrame.setMinimumHeight(12)
        self.timeFrame.mousePressEvent = lambda e: self.context_menu.show(e)

        self.dateTimeLabel = QLabel()
        self.dateTimeLabel.setText(
            self.tag.get_date_time().toString("dd/MM/yy ... HH:mm:ss")
        )
        self.dateTimeLabel.setAlignment(Qt.AlignRight)
        self.dateTimeLabel.setStyleSheet(FONT_FORMAT(12))
        self.dateTimeLabel.setMaximumHeight(15)
        self.dateTimeLabel.setWordWrap(True)
        self.timeFrameLayout.addWidget(self.dateTimeLabel)

        if self.isSender:
            self.statusLabel = QLabel()
            s = 13
            self.statusLabel.setMinimumSize(s, s)
            self.statusLabel.setMaximumSize(s, s)
            self.timeFrameLayout.addWidget(self.statusLabel)
            self.update_status()

        elif self.tag.type == TYPE.GROUP:
            self.nameLabel = QLabel(self.tag.sender)
            h = 15
            font = QFont("Times New Roman")
            font.setPointSize(13)
            font.setBold(1)

            self.nameLabel.setFont(font)
            self.nameLabel.setAlignment(Qt.AlignRight)
            self.nameLabel.setMinimumHeight(h)
            self.nameLabel.setMaximumHeight(h)
            self._layout.addWidget(self.nameLabel)

        self._layout.addWidget(self.messageFrame)
        self._layout.addWidget(self.timeFrame)

    def resend(self):
        self.chat_viewer.new_tag(**self.tag[["text", "chat", "data"]])

    def delete(self):
        self.chat_viewer.delete_chat_message(self.tag.id)

    def set_style(self):
        self._wid.setStyleSheet(
            """
        border: 2px; 
        border-top-right-radius: 10px; 
        background: %s;
        color: black"""
            % self._style
        )

        self.setStyleSheet(self.__style % (self._style, self._style))

    def update_status(self):
        if self.statusLabel:
            if self.tag.sent:
                icon = "check"
            else:
                icon = "clock"
            s = 13
            pix = GET_PIXMAP(None, icon).scaled(s, s)
            self.statusLabel.setPixmap(pix)

    def showEvent(self, e=0):
        self.update_status()

        if not self.tag.seen:
            self.tag.seen = True
            self.chat_widget.update_chat_details()

    def moveEvent(self, event):
        self.update_status()


class ChatViewer(ScrolledWidget):
    def __init__(self, chat_tab: "ChatTab", chat_widget: ChatWidget):
        ScrolledWidget.__init__(self, space=4, margins=[7, 0, 7, 7])

        self.chat_tab = chat_tab
        self.client = chat_tab.home.client
        self.user: User = self.client.user
        self.chat_widget = chat_widget
        self.chat_object = chat_widget.chat_object
        self.image_view: ImageView = chat_tab.home.image_view

        self.fill()

    def fill(self):
        for chat in self.chat_object.chats:
            self.add_tag(chat)

    def new_tag(self, text="", chat=CHAT.TEXT, data=b""):
        tag = Tag(
            text=text,
            action=CHAT,
            chat=chat,
            sender=self.user.id,
            recipient=self.chat_object.id,
            type=self.chat_object.className,
            data=data,
        )
        tag = self.client.send_chat_tag(tag)
        self.add_tag(tag)

    def add_message(self, message):
        self.new_tag(text=message, chat=CHAT.TEXT)

    def add_image(self, image: bytes, text: str = ""):
        self.new_tag(text=text, data=image, chat=CHAT.IMAGE)

    def add_audio(self, data=b""):
        self.new_tag(data=data, chat=CHAT.AUDIO)

    def add_tag(self, tag):
        if self.get_child(tag.id):
            return

        obj = ChatMessage(self.client, self.chat_widget, tag, chat_viewer=self)
        self.add_child(obj, tag.id, 0, obj.align)

        self.chat_widget.update_chat_details()

    def get_chat_message(self, tag_id: str) -> ChatMessage:
        return self.get_child(tag_id)

    def delete_chat_message(self, tag_id: str):
        self.remove_child(tag_id)
        self.chat_object.remove_chat(tag_id)
        self.chat_widget.update_chat_details()

    def update_status(self):
        for chat in self.children_widgets:
            chat.update_status()

    def add_unseens(self):
        unseen_chats = self.chat_object.unseen_chats()
        for chat in unseen_chats:
            self.add_tag(chat)

    def showEvent(self, event: QShowEvent) -> None:
        self.add_unseens()


class ChatRoom(QFrame):
    def __init__(
        self,
        chat_tab: "ChatTab",
        chat_widget: ChatWidget,
    ):
        QFrame.__init__(self)
        self.chat_tab = chat_tab

        self.client = chat_tab.client
        self.send_back = chat_tab.send_back

        self.chat_widget = chat_widget
        self.chat_object = chat_widget.chat_object

        layout = SETUP_FRAME(obj=self, orient="v", space=0, margins=[2, 2, 2, 2])

        self.chat_viewer = ChatViewer(chat_tab, self.chat_widget)

        self.header = ChatHeader(
            chat_room=self,
            closeRoom=lambda e: chat_tab.closeRoom(self.chat_object),
            show_info=chat_tab.show_info,
        )

        layout.addWidget(self.header)
        layout.addWidget(self.chat_viewer)

        self.status = QLabel()
        font = QFont("Times New Roman")
        font.setPointSize(15)
        font.setBold(1)
        self.status.setFont(font)
        self.status.setAlignment(Qt.AlignCenter)

        self.status.setMinimumHeight(50)
        self.status.setMaximumHeight(50)
        layout.addWidget(self.status)

        self.footer = ChatFooter(chat_tab, chat_viewer=self.chat_viewer)
        layout.addWidget(self.footer)

        self.update_room()

    def update_room(self):
        self.header.update_status()
        # hide [status = True, footer = False, both = None]
        hide = False

        if isinstance(self.chat_object, (Group, Channel)):
            if self.client.user.id not in self.chat_object.users:
                self.status.setText("YOU WERE REMOVED")
                hide = True
            elif self.client.user.id in self.chat_object.admins:
                hide = False
            elif self.chat_object.only_admin:
                hide = True
                self.status.setText("ONLY ADMIN")
                if isinstance(self.chat_object, Channel):
                    hide = None

        if hide == None:
            self.status.hide()
            self.footer.hide()

        elif hide == True:
            self.footer.hide()
            self.status.show()

        elif hide == False:
            self.status.hide()
            self.footer.show()

    def resizeEvent(self, event):
        self.header.update_status()
        self.chat_viewer.update_status()

    def showEvent(self, event):
        self.send_back(self.chat_object)
        self.resizeEvent(event)

    def add_unseens(self):
        self.chat_viewer.add_unseens()


class ChatTab(QTabWidget):
    def __init__(self, home: "Home"):
        QTabWidget.__init__(self)

        self.home = home

        self.setMinimumWidth(450)
        self._emoji_on = False

        self._send_back = home.send_back
        self._chats_ids_ = []
        self._chats_rooms_ = {}
        self.client = home.client
        self.user = home.client.user
        s = 28
        self.setIconSize(QSize(s, s))

        self.contact_detail = Detail_Dialog(parent=self, client=home.client)
        self.multiUser_detail = MultiUser_Detail(parent=self, client=home.client)

        self.emoji = None

    def add_chat_room(self, chat_widget: ChatWidget):
        chat_object = chat_widget.chat_object

        id = chat_object.id
        if id in self._chats_ids_:
            index = self._chats_ids_.index(id)
        else:
            w = ChatRoom(
                self,
                chat_widget,
            )

            self._chats_ids_.append(id)
            self._chats_rooms_[id] = w

            icon = GET_ICON(chat_object.icon, GET_DEFAULT_ICON(chat_object), mask=100)

            index = self.addTab(w, icon, chat_object.get_name())
            self.update_tab(chat_object)

        self.setCurrentIndex(index)

    def update_tab(self, chat_object: Union[Contact, Multi_Users]):
        if chat_object.id in self._chats_ids_:
            index = self._chats_ids_.index(chat_object.id)
            icon = GET_ICON(chat_object.icon, GET_DEFAULT_ICON(chat_object), mask=100)
            self.setTabIcon(index, icon)
            self.setTabText(index, chat_object.get_name())

    def show_info(self, chat_object):
        self.contact_detail.close()
        self.multiUser_detail.close()

        if isinstance(chat_object, Contact):
            detail = self.contact_detail
        else:
            detail = self.multiUser_detail

        detail.set_chat_object(chat_object)

        win_geo = self.window().geometry()

        w, h = detail.size().toTuple()
        x = win_geo.x() + win_geo.width() - w - 5
        y = win_geo.y() + 20

        detail.move_xywh = (x, y, w, h)
        # detail.setMaximumSize(w, h)
        if not detail.isVisible():
            detail.show()
        else:
            detail.showEvent(None)

    def closeRoom(self, chat_object):
        id = chat_object.id
        if self.count() <= 1:
            return
        index = self._chats_ids_.index(id)
        self.removeTab(index)
        self._chats_ids_.remove(id)
        del self._chats_rooms_[id]

    def send_back(self, chat_object: Union[Contact, Multi_Users]):
        self._send_back(chat_object)

    def get_chat_room(self, id: str) -> ChatRoom:
        return self._chats_rooms_.get(id)

    @property
    def current(self) -> ChatRoom:
        chat_room = self.currentWidget()
        return chat_room

    def showEvent(self, event):
        self.emoji = Emoji(self)

    def emoji_closed(self):
        self._emoji_on = False

    def show_emoji(self):
        if self.emoji:
            if self._emoji_on:
                self._emoji_on = False
                self.emoji.hide()
                # self.setMaximumHeight(50)
            else:
                self._emoji_on = True
                self.emoji.show()
