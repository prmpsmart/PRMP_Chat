from .extras import *


class ChatWidget(QPushButton):
    def __init__(self, chat_object: Chats, callback=None, index=0):
        super().__init__()

        self.chat_object = chat_object

        self.index = index

        self.setCheckable(True)

        self.setMinimumHeight(70)
        self.setMaximumHeight(70)

        m = 2
        layout = SETUP_FRAME(
            obj=self, orient="h", margins=[m * 2, m * 2, m * 2, m * 2], space=4
        )

        self.icon_frame, icon_layout = SETUP_FRAME(mother_layout=layout, re_obj=1)
        d = 60
        self.icon_frame.setMinimumSize(d, d)
        self.icon_frame.setMaximumSize(d, d)
        self.icon_frame.setStyleSheet("border-radius: %spx" % (d / 2))

        self.imageButton = ImageButton(GET_DEFAULT_ICON(chat_object), size=50, mask=100)
        icon_layout.addWidget(self.imageButton)

        if isinstance(chat_object, Contact):
            self.status_bubble = QLabel(self.icon_frame)

        self.texts_frame, _ = SETUP_FRAME(mother_layout=layout, re_obj=1)

        self.name = QLabel(self.texts_frame)
        self.name.setGeometry(5, 0, 150, 20)
        self.name.setStyleSheet(FONT_FORMAT(20, "bold"))

        self.last_info = QLabel(self.texts_frame)
        self.last_info.setGeometry(5, 42, 140, 15)
        font_str = FONT_FORMAT(size=15)
        self.last_info.setStyleSheet(font_str)

        self.chat_status = QLabel(self.texts_frame)
        self.chat_status.setGeometry(145, 42, 30, 15)
        self.chat_status.setStyleSheet(font_str)

        self.date = QLabel(self.texts_frame)
        self.date.setStyleSheet(FONT_FORMAT(size=14))
        self.fm = QFontMetrics(self.date.font())

        self.new_message = QLabel(self.texts_frame)
        s = 25
        self.new_message.setPixmap(GET_PIXMAP(None, "new_message").scaled(s, s))

        self.unseen_bubble = QLabel(self.texts_frame)
        self.unseen_bubble.setLayoutDirection(Qt.RightToLeft)
        self.ufm = QFontMetrics(self.unseen_bubble.font())

        self.time = QLabel(self.texts_frame)
        self.time.setStyleSheet(FONT_FORMAT(size=14))
        self.tfm = QFontMetrics(self.time.font())

        self.update_chat_widget()

        self.clicked.connect(lambda: callback(self))

    def update_status(self):

        if isinstance(self.chat_object, Contact):
            if self.chat_object.user.status == STATUS.ONLINE:
                self.status_bubble.setStyleSheet(
                    f'background: {"green" if self.chat_object.status == STATUS.ONLINE else "gray"}; border-radius: 5px; color: white'
                )
                self.status_bubble.show()

                self.status_bubble.setToolTip(self.chat_object.status)
            else:
                self.status_bubble.hide()

    def update_details(self):
        self.name.setText(self.chat_object.get_name())

        date_time = self.chat_object.last_time
        date = date_time.toString("dd/MM/yy")

        self.date.setText(date)
        self.dbr = self.fm.boundingRect(date)

        time = date_time.toString("HH:mm:ss")
        self.time.setText(time)
        self.tbr = self.tfm.boundingRect(time)

        unseen = str(self.chat_object.unseens)

        self.unseen_bubble.setText(unseen)
        self.ubr = self.ufm.boundingRect(unseen)
        self.chat_status.hide()

        last_chat = self.chat_object.last_chat
        if last_chat:
            last_text = last_chat.text
            self_ = last_chat.sender == self.chat_object.user.id

            is_image = last_chat.chat == CHAT.IMAGE
            is_audio = last_chat.chat == CHAT.AUDIO

            if last_text:
                last_text = last_text.split("\n")[0]
                if self_:
                    last_text = f"You: {last_text}"

                else:
                    if isinstance(self.chat_object, Multi_Users):
                        last_text = f"{last_chat.sender}: {last_text}"

                n = 25
                if len(last_text) > n:
                    last_text = "".join(last_text[:n])

                self.last_info.setText(last_text + "...")
            else:
                if is_image:
                    text = "IMAGE"
                elif is_audio:
                    text = "AUDIO"

                if self_:
                    text = "You: " + text
                self.last_info.setText(text)

            if self_ and self.chat_status:
                if last_chat.sent:
                    icon = "check"
                else:
                    icon = "clock"

                s = 16
                pix = GET_ICON(None, icon).pixmap(s, s)
                self.chat_status.setPixmap(pix)
                self.chat_status.show()

    def update_icon(self):
        self.imageButton.set_icon(self.chat_object.icon)

    def update_chat_widget(self):
        self.update_status()
        self.update_icon()
        self.update_chat_details()

    def update_chat_details(self):
        self.update_details()
        self.place_details()

    def place_details(self, event=0):
        w = self.icon_frame.width()
        h = self.icon_frame.width()

        if isinstance(self.chat_object, Contact):
            self.status_bubble.setGeometry(w - 20, h - 20, 10, 10)

        w = self.texts_frame.width()
        h = self.texts_frame.height()

        a = 5
        self.date.setGeometry(
            w - self.dbr.width() - 4 - a, 0, self.dbr.width() + a, self.dbr.height() + a
        )

        if self.chat_object.unseens:
            self.unseen_bubble.setGeometry(
                w - self.ubr.width() - 42,
                (h - self.ubr.height()) / 2,
                self.ubr.width() + 6,
                self.ubr.height() + 3,
            )
            self.unseen_bubble.show()

            self.new_message.setGeometry(
                w - 30,
                (h - 30) / 2,
                30,
                30,
            )
            self.new_message.show()

        else:
            self.new_message.hide()
            self.unseen_bubble.hide()

        self.time.setGeometry(
            w - self.tbr.width() - 6 - a,
            48 - a,
            self.tbr.width() + a + a,
            self.tbr.height() + a,
        )

    def showEvent(self, event=None):
        self.place_details()

    resizeEvent = showEvent


class ChatsList(ScrolledWidget):
    def __init__(self, tab, user: User, attr="contacts", callback=None):
        ScrolledWidget.__init__(self, tab, space=2, margins=[2, 2, 2, 2])
        self._layout.setAlignment(Qt.AlignTop)
        self.set_bars_off()
        self.current = None
        self._callback = callback
        self.user = user
        self.attr = attr

        self.last = None
        self.filled = False

    def get_chat_object_widget(
        self, id_obj: Union[str, Contact, Multi_Users]
    ) -> ChatWidget:

        chat_object = None
        if isinstance(id_obj, str):
            for c_o in self.key_children_widgets:
                if c_o.id == id_obj:
                    chat_object = c_o
                    break
        else:
            chat_object = id_obj

        return self.get_child(chat_object)

    def add_chat_object(self, chat_object, top=0):
        if self.get_child(chat_object):
            return

        chat = ChatWidget(
            chat_object, callback=self.callback, index=self._layout.count()
        )
        if top:
            self.insert_child(0, chat, chat_object)
        else:
            self.add_child(chat, chat_object)

        if not self.last:
            self.last = chat

    def fill(self):
        if self.user:
            manager = getattr(self.user, self.attr, None)
            if manager:
                self.clear()
                for obj in manager.objects:
                    self.add_chat_object(obj)

    def callback(self, chat_widget: ChatWidget):
        if self.current and self.current != chat_widget:
            try:
                self.current.setChecked(0)
            except:
                ...
        self.switch_current(chat_widget)
        self._callback(chat_widget)

    def set_current_object(self, chat_object):
        widget = self.get_child(chat_object)
        if widget:
            self.switch_current(widget)

    def switch_current(self, widget: ChatWidget):
        if self.current:
            self.current.setChecked(0)

        self.current = widget
        self.current.setChecked(1)

    def update_subs(self, func: str):
        for v in self.children_widgets:
            getattr(v, func)()

    def showEvent(self, event):
        if not self.filled:
            QTimer.singleShot(50, self.fill)
            self.filled = True

        # objs = (
        #     self.user.users["ade3"],
        #     self.user.groups["g_ade2"],
        #     self.user.channels["c_ade2"],
        # )

        # for obj in objs:
        #     if obj:
        #         self.set_current_object(obj)

        if self.current:
            self.callback(self.current)
        ...


class SearchList(ChatsList):
    def __init__(self, tab, **kwargs):
        super().__init__(tab, **kwargs)

        if self.user:
            self.chats_objects = [
                *self.user.users[:],
                *self.user.groups[:],
                *self.user.channels[:],
            ]
        else:
            self.chats_objects = []
        self.searched_objects = []

    def add_searched_objects(self, so):
        if so in self.searched_objects:
            return
        self.searched_objects.append(so)

    def search(self, text):
        self.clear()

        if not text:
            return

        for co in self.chats_objects:
            if text in co.get_name().lower() or text in co.id.lower():
                self.add_searched_objects(co)

            else:
                for chat in co.chats:
                    if text in chat.text.lower():
                        self.add_searched_objects(co)
                        break

        for so in self.searched_objects:
            self.add_chat_object(so)

        if not self.searched_objects:
            self.clear()
