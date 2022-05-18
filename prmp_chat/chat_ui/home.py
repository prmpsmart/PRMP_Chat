from .chat_listing import *
from .chat_room import *
from .edit import *
from .details import *
from .call import Call_Notify


class Backend_Hook:
    def __init__(self, client=None, user=None):
        assert user or client

        self.client = client or Client(user=user)
        self.client.relogin = 1

        self.client.LOG = self.LOG
        self.client.RECV_LOG = self.RECV_LOG
        self.client.STATUS_LOG = self.STATUS_LOG
        self.client.CHAT_STATUS = self.CHAT_STATUS

        # self.user.recv_data = False

        self.login_thread = Thread(self, self.start)

    @property
    def user(self):
        return self.client.user

    def start(self):
        if self.user:
            if self.client.online:
                self.client.start_session()

            else:
                self.client.re_login(start=1)

    def LOG(self, *args, **kwargs):
        print(*args, **kwargs)
        ...

    def RECV_LOG(self, tag: Tag):
        ...

    def STATUS_LOG(self, status: STATUS):
        ...

    def CHAT_STATUS(self, status: STATUS):
        ...

    def stop(self):
        self.login_thread.quit()
        self.login_thread.exit()
        self.client.stop()
        DB.SAVE_USER(self.user)


class SideBarButton(IconButton):
    def __init__(self, klass, winKwargs={}, bottom=False, **kwargs):
        super().__init__(**kwargs)

        self.bottom = bottom
        self.popup: QWidget = None
        if winKwargs:
            self.popup = klass(self, **winKwargs)

    def mousePressEvent(self, e=0) -> None:
        win = self.window()
        pos = win.pos()
        geo = self.geometry()

        if self.popup:
            if self.popup.isVisible():
                self.popup.hide()
            else:
                if self.bottom:
                    self.popup.move(
                        pos.x() + geo.width() + 10,
                        pos.y() + geo.y() - self.popup.height() / 2,
                    )

                else:
                    self.popup.move(pos.x() + geo.width() + 10, pos.y() + geo.y())

                self.popup.show()


class SideBar(QFrame):
    def __init__(self, home):
        super().__init__()

        self.setMinimumWidth(50)
        self.setMaximumWidth(50)

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        layout = QVBoxLayout(self)
        layout.setSpacing(50)
        layout.setContentsMargins(5, 50, 5, 50)

        self.personalDetails = SideBarButton(
            Detail_Dialog,
            # tip="Personal Details",
            icon="user",
            size=40,
            winKwargs=dict(client=home.client, chat_object=home.user),
        )
        layout.addWidget(self.personalDetails)

        add = SideBarButton(
            Add_Dialog,
            icon="add",
            size=40,
            winKwargs=dict(home=home),
        )
        layout.addWidget(add)

        new = SideBarButton(
            New_Dialog,
            icon="new",
            size=40,
            winKwargs=dict(home=home),
        )
        layout.addWidget(new)

        reload = IconButton(icon="reload", size=40, tip="Reload")
        reload.clicked.connect(self.reload)
        layout.addWidget(reload)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer)

        settings = SideBarButton(
            Settings,
            icon="settings",
            size=40,
            winKwargs=dict(home=home),
            bottom=True,
        )
        layout.addWidget(settings)

    def reload(self):
        QApplication.instance().quit()


class Home(Window, Backend_Hook):

    recv_signal = Signal(Tag)

    def __init__(self, app=None, client=None, user=None):
        super().__init__(app)

        self.online_pixmap = GET_PIXMAP(None, "online")
        self.offline_pixmap = GET_PIXMAP(None, "offline")

        Backend_Hook.__init__(self, client, user)

        self.setMinimumHeight(500)
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        self._size = None

        self.mb = QMessageBox(self)

        self.response_receiver = Response_Receiver(self)
        self.recv_signal.connect(self.response_receiver)

        self.call_dialog = Call_Dialog(self)
        self.call_notify = Call_Notify(parent=self)
        self.image_view = ImageView(parent=self)

        self.sideBar = SideBar(self)
        self.layout_.addWidget(self.sideBar)
        self.setupLeft()
        self.setupRight()

        self.defaults()

    def defaults(self):
        self.startTimer(500)

    def timerEvent(self, event: QTimerEvent):
        self.login_thread.start()
        if event:
            self.killTimer(event.timerId())

    def setupLeft(self):
        left = QFrame()
        left.setMinimumWidth(300)
        left.setMaximumWidth(300)
        left.setFrameShape(QFrame.StyledPanel)
        left.setFrameShadow(QFrame.Raised)

        leftLayout = QVBoxLayout(left)
        leftLayout.setSpacing(5)
        SET_MARGINS(leftLayout, 0)

        self.layout_.addWidget(left)

        detail = QFrame()
        detail.setMinimumHeight(68)
        detail.setMaximumHeight(68)
        detail.setFrameShape(QFrame.StyledPanel)
        detail.setFrameShadow(QFrame.Raised)
        leftLayout.addWidget(detail)

        horizontalLayout_2 = QHBoxLayout(detail)
        horizontalLayout_2.setSpacing(10)
        SET_MARGINS(horizontalLayout_2, 2)

        self.imageButton = ImageButton(default="user", mask=300)
        h = 60
        self.imageButton.setMinimumSize(QSize(h, h))
        self.imageButton.setMaximumSize(QSize(h, h))
        horizontalLayout_2.addWidget(self.imageButton)

        detailLayout = QFormLayout()
        detailLayout.setLabelAlignment(Qt.AlignRight)
        horizontalLayout_2.addLayout(detailLayout)

        self.nameLabel = QLabel()
        self.nameLabel.setStyleSheet(FONT_FORMAT(19, "bold"))
        detailLayout.addRow("Name : ", self.nameLabel)

        self.idLabel = QLabel()
        detailLayout.addRow("ID : ", self.idLabel)

        self.bioLabel = QLabel()
        self.bioLabel.setWordWrap(1)
        detailLayout.addRow("Bio : ", self.bioLabel)

        self.status = QLabel()
        self.status.setStyleSheet(f"border-radius: {h};")
        h = 25
        self.status.setMinimumSize(h, h)
        self.status.setMaximumSize(h, h)

        horizontalLayout_2.addWidget(self.status)

        leftLower = QFrame(left)
        leftLower.setFrameShape(QFrame.StyledPanel)
        leftLower.setFrameShadow(QFrame.Raised)

        leftLayout.addWidget(leftLower)

        self.center_tab = QTabWidget()
        leftLayout.addWidget(self.center_tab)

        self.contact_frame: ChatsList = CREATE_TAB(
            self.center_tab,
            "contact",
            "Contacts",
            ChatsList,
            kwargs=dict(user=self.user, callback=self.chat_picked),
        )

        self.group_frame: ChatsList = CREATE_TAB(
            self.center_tab,
            "group",
            "Groups",
            ChatsList,
            kwargs=dict(user=self.user, attr="groups", callback=self.chat_picked),
        )
        self.channel_frame: ChatsList = CREATE_TAB(
            self.center_tab,
            "channel",
            "Channels",
            ChatsList,
            kwargs=dict(user=self.user, attr="channels", callback=self.chat_picked),
        )
        self.search_frame = CREATE_TAB(
            self.center_tab,
            "search",
            "Search",
            SearchList,
            kwargs=dict(user=self.user, attr="", callback=self.chat_picked),
        )

        self.update_details()

    def setupRight(self):
        right = QFrame()
        right.setFrameShape(QFrame.StyledPanel)
        right.setFrameShadow(QFrame.Raised)

        self.layout_.addWidget(right)

        self.chat_tab = ChatTab(self)
        self.layout_.addWidget(self.chat_tab)

    def update_details(self):
        self.setWindowTitle(f"Mimi Peach {self.user.get_name()}")

        self.nameLabel.setText(self.user.name)
        self.idLabel.setText(self.user.id)
        self.bioLabel.setText(self.user.bio)
        self.imageButton.set_icon(self.user.icon)
        self.change_status(self.user.status)

    def chat_picked(self, chat):
        self.chat_tab.add_chat_room(chat)

    def change_status(self, status: CONSTANT):
        h = int(self.status.width() / 2)

        if status == STATUS.ONLINE:
            self.status.setPixmap(self.online_pixmap)

        else:
            self.status.setPixmap(self.offline_pixmap)
        self.status.setToolTip(str(status).upper())

    def send_back(self, user):
        widget = None
        index = 0

        if isinstance(user, Contact):
            widget, index = self.contact_frame, 0
        elif isinstance(user, Group):
            widget, index = self.group_frame, 1
        elif isinstance(user, Channel):
            widget, index = self.channel_frame, 2
        else:
            return

        widget.set_current_object(user)
        self.center_tab.setCurrentIndex(index)

    def showEvent(self, event):
        if not self._size:
            self._size = self.size()
        return super().showEvent(event)

    resizeEvent = showEvent

    def fill_chatlists(self):
        self.update_details()
        self.contact_frame.fill()
        self.group_frame.fill()
        self.channel_frame.fill()

    def reload_home(self):
        self.fill_chatlists()
        self.chat_tab.clear()

    def closeEvent(self, event=0):
        self.stop()

    def RECV_LOG(self, tag: Tag):
        self.recv_signal.emit(tag)

    def STATUS_LOG(self, status: STATUS):
        self.change_status(status)

        current = self.chat_tab.current
        if current:
            current.header.update_status()

        contact_frame = self.contact_frame

        c_o: ChatWidget = None
        for c_o in contact_frame.children_widgets:
            c_o.update_status()

    def CHAT_STATUS(self, tag: Tag):
        id, recipient = tag["id", "recipient"]
        chat_room = self.chat_tab.get_chat_room(recipient)
        if chat_room:
            viewer = chat_room.viewer
            message = viewer.get_chat_message(id)
            if message:
                message.update_status()

        chat_widget = self.response_receiver.get_chat_widget(tag.type, recipient)

        if chat_widget and tag == chat_widget.chat_object.last_chat:
            chat_widget.update_chat_details()


class Response_Receiver:
    def get_chat_frame(self, type) -> ChatsList:
        chat_frame = None
        if type in [TYPE.CONTACT, TYPE.USER]:
            chat_frame = self.home.contact_frame

        elif type == TYPE.GROUP:
            chat_frame = self.home.group_frame

        elif type == TYPE.CHANNEL:
            chat_frame = self.home.channel_frame

        return chat_frame

    def get_chat_widget(self, type, id) -> ChatWidget:
        chat_frame = self.get_chat_frame(type)
        if chat_frame:
            return chat_frame.get_chat_object_widget(id)

    def get_chat_room(self, id) -> ChatRoom:
        return self.home.chat_tab.get_chat_room(id)

    def update_chat_room(self, id) -> ChatRoom:
        chat_room = self.get_chat_room(id)
        if chat_room:
            chat_room.update_room()

    def get_chat_room_header(self, id) -> ChatHeader:
        chat_room = self.get_chat_room(id)
        if chat_room:
            return chat_room.header

    def update_chat_room_header(self, id):
        header = self.get_chat_room_header(id)
        if header:
            header.update_status()

    def update_details(self):
        chat_tab = self.home.chat_tab
        c, m = chat_tab.contact_detail, chat_tab.multiUser_detail

        d: Detail_Dialog = None
        for d in (c, m):
            if d.isVisible():
                d.update_details()

    def __init__(self, home: Home):
        self.home = home
        self.mb = home.mb
        self.user = home.user
        self.client = home.client

        self.receivers = {
            ACTION.ADD: self.add_receiver,
            ACTION.ADD_ADMIN: self.add_admin_receiver,
            ACTION.ADD_MEMBER: self.add_member_receiver,
            ACTION.CALL: self.call_receiver,
            ACTION.CALL_RESPONSE: self.call_response_receiver,
            ACTION.CALL_REQUEST: self.call_request_receiver,
            ACTION.CHANGE: self.change_receiver,
            ACTION.CHAT: self.chat_receiver,
            ACTION.CREATE: self.create_receiver,
            ACTION.DATA: self.data_receiver,
            ACTION.ONLY_ADMIN: self.only_admin_receiver,
            ACTION.REMOVE_ADMIN: self.remove_admin_receiver,
            ACTION.REMOVE_MEMBER: self.remove_member_receiver,
            ACTION.STATUS: self.status_receiver,
        }

    def __call__(self, tag: Tag):
        action = tag.action
        if action:
            receiver = self.receivers.get(action)
            if receiver:
                receiver(tag)
                # THREAD_SAVE(self.user)
            else:
                ...

    # =------------=----------------=---------------=

    def add_receiver(self, tag: Tag):
        response, action = tag["response", "action"]

        add_type = tag.type

        self.mb.setWindowTitle(f"{action} {add_type}")

        id = self.client.get_type_id(tag)

        obj = tag.obj

        if obj:
            chat_frame = self.get_chat_frame(add_type)
            chat_frame.add_chat_object(obj)

        if response == RESPONSE.SUCCESSFUL:
            if obj:
                self.mb.setText(f'{add_type} "{obj.get_name()}" is added successfully.')
            else:
                self.mb.setText(f'{add_type} "{id}" add failed.')

        elif response == RESPONSE.EXIST:
            self.mb.setText(f'{add_type} "{id}" already exist.')

        elif response == RESPONSE.EXTINCT:
            self.mb.setText(f'{add_type} "{id}" does not exist.')

        elif response == RESPONSE.ADMIN_ONLY:
            self.mb.setText(f'{add_type} "{id}" only admin can add users.')

        if response:
            self.mb.show()

    def add_admin_receiver(self, tag: Tag):
        multi_user = self.client.get_multi_user(tag)
        if multi_user:
            self.update_details()
            self.update_chat_room(multi_user.id)

    def add_member_receiver(self, tag: Tag):
        multi_user = self.client.get_multi_user(tag)
        user_id = tag.user_id

        if multi_user and user_id:
            self.update_details()
            self.update_chat_room(multi_user.id)

        elif user_id == self.user.id:
            obj = tag.obj
            if obj:
                chat_frame = self.get_chat_frame(tag.type)
                chat_frame.add_chat_object(obj)

    def call_receiver(self, tag: Tag):
        if self.home.call_dialog.active:
            self.home.call_dialog.receive_data(tag)

    def call_request_receiver(self, tag: Tag):
        if not self.home.call_dialog.isVisible():
            self.home.call_notify.loadTag(tag)
        else:
            tag.response = RESPONSE.DECLINED
            self.client.send_action_tag(tag)

    def call_response_receiver(self, tag: Tag):
        self.home.call_dialog.receive_response(tag)

    def change_receiver(self, tag: Tag):
        id = GET_TYPE_ID(tag)

        if id == self.user.id:
            if tag.response == RESPONSE.SUCCESSFUL:
                self.home.update_details()
                popup: Detail_Dialog = self.home.sideBar.personalDetails.popup
                if popup:
                    popup.update_details()

        elif id:
            chat_object = self.user.get_chat_object(id)

            if chat_object:
                chat_widget = self.get_chat_widget(tag.type, id)

                if chat_widget:
                    chat_widget.update_chat_widget()

                chat_tab = self.home.chat_tab
                chat_tab.update_tab(chat_object)

                self.update_details()
                self.update_chat_room_header(id)

                if tag.icon:
                    header = self.get_chat_room_header(id)
                    if header:
                        header.update_icon()

    def chat_receiver(self, tag: Tag):
        sender, recipient = tag["sender", "recipient"]
        id = sender if tag.type == TYPE.CONTACT else recipient

        chat_widget = self.get_chat_widget(tag.type, id)

        if chat_widget:
            chat_widget.update_chat_details()

        chat_tab = self.home.chat_tab
        chat_room = chat_tab.get_chat_room(id)

        if chat_room:
            chat_room.add_unseens()

    def create_receiver(self, tag: Tag):
        type, response = tag["type", "response"]
        id = self.client.get_type_id(tag)

        text = f'{type} "{id}"'

        if response == RESPONSE.EXIST:
            text += " already exist."

        elif (response == RESPONSE.SUCCESSFUL) and tag.obj:
            text += " is created successfully."
            chat_frame = self.get_chat_frame(tag.type)
            chat_frame.add_chat_object(tag.obj, top=1)

        self.mb.setWindowTitle(f"{type} {RESPONSE}")
        self.mb.setText(text)
        self.mb.show()

    def data_receiver(self, tag: Tag):
        if tag.id == self.user.id:
            self.home.fill_chatlists()

    def only_admin_receiver(self, tag: Tag):
        multi_user = self.client.get_multi_user(tag)
        if multi_user:
            self.update_details()
            self.update_chat_room(multi_user.id)

    def remove_admin_receiver(self, tag: Tag):
        multi_user = self.client.get_multi_user(tag)
        if multi_user and tag.user_id:
            self.update_details()
            self.update_chat_room(multi_user.id)

    def remove_member_receiver(self, tag: Tag):
        multi_user = self.client.get_multi_user(tag)
        if multi_user and tag.user_id:
            self.update_details()
            self.update_chat_room(multi_user.id)

    def status_receiver(self, tag: Tag):
        if not tag.statuses:
            id = tag.id
            chat_widget = self.home.contact_frame.get_chat_object_widget(id)

            if chat_widget:
                chat_widget.update_status()

            header = self.update_chat_room_header(id)

            if header:
                header.header.update_status()

        else:
            contact_frame = self.home.contact_frame

            c_o: ChatWidget = None
            for c_o in contact_frame.children_widgets:
                c_o.update_status()
