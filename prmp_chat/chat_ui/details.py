from .extras import *


class Detail(QFrame):
    def __init__(
        self,
        client: Client = None,
        chat_object: Union[User, Contact, Multi_Users] = None,
    ) -> None:
        super().__init__()
        self.client = client
        self.editing = True
        self.imageChooser = ImageChooser(self.setImage, self)

        self.chat_object: Union[User, Multi_Users] = None

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.chosenImage: QImage = None

        self.layout_ = QVBoxLayout(self)
        SET_MARGINS(self.layout_)

        self.online_pixmap = GET_PIXMAP(None, "online")
        self.offline_pixmap = GET_PIXMAP(None, "offline")

        self.setup()
        self.set_chat_object(chat_object)
        self.switch()

    @property
    def statusable(self):
        return isinstance(self.chat_object, (User, Contact))

    @property
    def editable(self):
        return isinstance(self.chat_object, User) or (
            isinstance(self.chat_object, Multi_Users)
            and self.client.user.id in self.chat_object.admins
        )

    def set_chat_object(self, chat_object: Union[User, Contact, Multi_Users]):
        self.chat_object = chat_object

        if self.statusable:
            self.status.show()
        else:
            self.status.hide()

        if self.editable:
            self.editButton.show()
        else:
            self.editButton.hide()

        self.update_details()

    def setup(self):
        self.view = QFrame()
        self.layout_.addWidget(self.view)

        viewLayout = QVBoxLayout(self.view)
        viewLayout.setAlignment(Qt.AlignCenter)
        SET_MARGINS(viewLayout)

        self.image = ImageButton(GET_DEFAULT_ICON(self.chat_object))
        self.image.setMinimumHeight(200)
        self.image.clicked.connect(self.changeIcon)
        viewLayout.addWidget(self.image, Qt.AlignRight)

        verticalLayout = QVBoxLayout()
        viewLayout.addLayout(verticalLayout)

        SET_MARGINS(verticalLayout)

        formLayout = QFormLayout()
        formLayout.setLabelAlignment(Qt.AlignRight)
        verticalLayout.addLayout(formLayout)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter Name")
        formLayout.addRow("Name : ", self.name)

        self.id = QLineEdit()
        self.id.setPlaceholderText("Enter ID")
        formLayout.addRow("ID : ", self.id)

        self.bio = QPlainTextEdit()
        self.bio.setPlaceholderText("Enter Bio")
        self.bio.setMaximumHeight(100)
        self.bio.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bio.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        formLayout.addRow("Bio : ", self.bio)

        self.keyLabel = QLabel("Key : ")
        self.key = PasswordEdit(clear=1)
        self.key.setPlaceholderText("Enter Key")
        formLayout.addRow(self.keyLabel, self.key)

        othersLayout = QHBoxLayout()
        othersLayout.setAlignment(Qt.AlignRight)
        verticalLayout.addLayout(othersLayout)

        self.status = QLabel()
        h = 25
        self.status.setStyleSheet(f"border-radius: {h}; margin-top: 5px")
        self.status.setAlignment(Qt.AlignRight)
        othersLayout.addWidget(self.status)

        self.editButton = IconButton(icon="edit", size=30, tip="Edit")
        self.editButton.setStyleSheet("border-radius: 15;")
        self.editButton.clicked.connect(self.switch)
        self.editButton.hide()
        othersLayout.addWidget(self.editButton)

        actionLayout = QHBoxLayout()
        verticalLayout.addLayout(actionLayout)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.switch)
        actionLayout.addWidget(self.cancelButton)
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        actionLayout.addWidget(self.saveButton)

    def showEvent(self, event: QShowEvent) -> None:
        # self.bio.setMaximumWidth(self.id.width())

        return super().showEvent(event)

    def update_details(self):
        if not self.chat_object:
            return
        self.bio.setReadOnly(1)
        self.name.setText(self.chat_object.name)
        self.id.setText(self.chat_object.id)
        self.image.set_icon(self.chat_object.icon, GET_DEFAULT_ICON(self.chat_object))
        self.bio.setPlainText(self.chat_object.bio)

        if self.statusable:
            if self.chat_object.status == STATUS.ONLINE:
                self.status.setPixmap(self.online_pixmap)

            else:
                self.status.setPixmap(self.offline_pixmap)
            self.status.setToolTip(str(self.chat_object.status).upper())

    def switch(self):
        parent = self.parent()
        height = 0
        if not self.editing:
            if parent and not height:
                height = parent.height()

            self.id.setToolTip("ID is not editable")
            self.id.setEnabled(0)

            for wid in [self.id, self.name, self.key, self.bio]:
                wid.setReadOnly(0)
                if wid != self.bio:
                    wid.setClearButtonEnabled(True)

            if isinstance(self.chat_object, User):
                self.keyLabel.show()
                self.key.show()
                self.key.setText(self.chat_object.key)
            else:
                self.keyLabel.hide()
                self.key.hide()

            self.status.hide()
            self.editButton.hide()

            self.cancelButton.show()
            self.saveButton.show()

            self.editing = True

        else:

            for wid in [self.id, self.name, self.key, self.bio]:
                wid.setReadOnly(1)
                if wid != self.bio:
                    wid.setClearButtonEnabled(False)

            self.keyLabel.hide()
            self.key.hide()
            self.saveButton.hide()
            self.cancelButton.hide()

            self.editing = False

            self.set_chat_object(self.chat_object)

        if parent and height:
            parent.setFixedHeight(height)

    def changeIcon(self):
        if self.editing:
            self.imageChooser.show()

    def setImage(self, image: QImage):
        self.chosenImage = image
        self.image.set_icon(image)

    def save(self):
        dic = {}
        id = self.chat_object.id
        if isinstance(self.chat_object, User):
            dic["type"] = TYPE.USER
            dic["user_id"] = id
        elif isinstance(self.chat_object, Multi_Users):
            if isinstance(self.chat_object, Group):
                dic["type"] = TYPE.GROUP
                dic["group_id"] = id
            else:
                dic["type"] = TYPE.CHANNEL
                dic["channel_id"] = id

        tag = Tag(action=ACTION.CHANGE, **dic)

        name = self.name.text()
        bio = self.bio.toPlainText()

        data = Tag()
        edited = False

        if self.chosenImage:
            self.image.setIcon(QPixmap(self.chosenImage))
            icon = GET_IMAGE_DATA(self.chosenImage)

            data.icon = B64_ENCODE(icon)
            edited = True

        if name and (name != self.chat_object.name):
            data.name = name
            edited = True

        if bio and (bio != self.chat_object.bio):
            data.bio = bio
            edited = True

        if isinstance(self.chat_object, User):
            key = self.key.text()
            if key and (key != self.chat_object.key):
                data.key = key
                edited = True

        if edited:
            tag.data = data
            if isinstance(self.chat_object, User):
                self.chat_object.set_pending_change_data(data)
            self.send_tag(tag)

        self.switch()

    def send_tag(self, tag):
        self.client.send_action_tag(tag)


class Detail_Dialog(QDialog):
    def __init__(self, parent=None, client: Client = None, chat_object=None) -> None:

        self.detail = Detail(client=client, chat_object=chat_object)
        self.move_xywh = ()

        super().__init__(parent, f=Qt.Tool)

        self.layout_ = QVBoxLayout(self)
        m = 5
        self.layout_.setContentsMargins(m, m, m, m)
        self.layout_.addWidget(self.detail)

    def set_chat_object(self, chat_object: Union[User, Contact, Multi_Users]):
        self.setWindowTitle(f"Detail of {self.detail.chat_object}")
        self.detail.set_chat_object(chat_object)

    def update_details(self):
        self.detail.update_details()

    def showEvent(self, e=0):
        self.update_details()
        if self.move_xywh:
            self.setGeometry(*self.move_xywh)

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.detail.editing = True
        self.detail.switch()
        return super().closeEvent(arg__1)


class MemberItem(QPushButton):
    def __init__(
        self,
        func,
        id,
        admin=False,
    ):
        super().__init__()
        self.id = id
        self.setMinimumHeight(40)
        self.setCheckable(1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(QLabel(id))

        if admin:
            adminButton = IconButton("admin", size=30)
            # label.setAlignment(Qt.AlignCenter)
            # w, h = 50, 20
            # label.setMinimumSize(w, h)
            # label.setMaximumSize(w, h)
            # label.setStyleSheet(
            #     "color: white; background: green; border-radius: 5px; font-family: Hobo Std; font-weight: bold; font-size: 13px"
            # )
            layout.addWidget(adminButton)
        self.clicked.connect(lambda: func(self))


class MemberList(ScrolledWidget):
    def __init__(self, parent):
        ScrolledWidget.__init__(
            self, parent, space=2, margins=[0, 0, 0, 0], autoscroll=0
        )
        self.chosen: MemberItem = None
        self.setMinimumHeight(150)

    def add(self, id, admin=False):
        child = MemberItem(self.setChosen, id, admin)
        self.add_child(child, id)

    @property
    def chosen_id(self):
        if self.chosen and self.chosen.isChecked():
            return self.chosen.id

    def setChosen(self, item: MemberItem):
        if self.chosen:
            self.chosen.setChecked(False)
        self.chosen = item

    def clear(self):
        super().clear()
        self.chosen = None


class MultiUser_Detail(Detail_Dialog):
    def __init__(
        self,
        parent,
        client,
    ) -> None:
        super().__init__(parent, client)

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Raised)
        self.layout_.addWidget(hline)

        horizontalLayout = QHBoxLayout()
        self.layout_.addLayout(horizontalLayout)

        membersGroupBox = QGroupBox("Members")
        membersGroupBox.setMinimumWidth(170)
        membersGroupBoxLayout = QVBoxLayout(membersGroupBox)

        self.membersListWidget = MemberList(membersGroupBox)
        membersGroupBoxLayout.addWidget(self.membersListWidget)

        requestDetails = QPushButton("Request Details")
        membersGroupBoxLayout.addWidget(requestDetails)

        horizontalLayout.addWidget(membersGroupBox)

        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Raised)

        horizontalLayout.addWidget(vline)

        self.administrationGroupBox = QGroupBox("Administration")
        administrationGroupBoxLayout = QVBoxLayout(self.administrationGroupBox)
        self.memberIDLineEdit = QLineEdit()
        self.memberIDLineEdit.setPlaceholderText("Member ID")

        administrationGroupBoxLayout.addWidget(self.memberIDLineEdit)

        addMember = QPushButton("Add Member")
        addMember.clicked.connect(self.addMember)
        administrationGroupBoxLayout.addWidget(addMember)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        administrationGroupBoxLayout.addItem(verticalSpacer)

        addAdmin = QPushButton("Add Admin")
        addAdmin.clicked.connect(self.addAdmin)
        administrationGroupBoxLayout.addWidget(addAdmin)

        removeAdmin = QPushButton("Remove Admin")
        removeAdmin.clicked.connect(self.removeAdmin)
        administrationGroupBoxLayout.addWidget(removeAdmin)

        removeMember = QPushButton("Remove Member")
        removeMember.clicked.connect(self.removeMember)
        administrationGroupBoxLayout.addWidget(removeMember)

        self.updating = False

        self.only_admin = QCheckBox("Only Admin")
        self.only_admin.stateChanged.connect(self.set_only_admin)
        administrationGroupBoxLayout.addWidget(self.only_admin)

        horizontalLayout.addWidget(self.administrationGroupBox)
        self.administrationGroupBox.hide()

    def set_chat_object(self, chat_object: Union[User, Contact, Multi_Users]):
        super().set_chat_object(chat_object)
        self.update_others()

        if self.detail.client.user.id in chat_object.admins:
            self.administrationGroupBox.show()
        else:
            self.administrationGroupBox.hide()

    def update_details(self):
        super().update_details()
        self.update_others()

    def update_others(self):
        self.updating = True
        if isinstance(self.detail.chat_object, Group):
            self.only_admin.setChecked(self.detail.chat_object.only_admin)
            self.only_admin.show()
        else:
            self.only_admin.hide()

        self.updating = False

        chat_object = self.detail.chat_object
        admins = chat_object.admins
        users = chat_object.users

        self.membersListWidget.clear()

        ready = list(admins)
        for user in users:
            if user not in admins:
                ready.append(user)

        ready.sort()

        for user in ready:
            admin = user in admins
            self.membersListWidget.add(user, admin=admin)

    def addMember(self):
        id = self.memberIDLineEdit.text()
        if id:
            self.send_tag(ACTION.ADD_MEMBER, id=id)

    def addAdmin(self):
        self.send_tag(ACTION.ADD_ADMIN, id=self.choosen)

    def removeAdmin(self):
        self.send_tag(ACTION.REMOVE_ADMIN, id=self.choosen)

    def removeMember(self):
        self.send_tag(ACTION.REMOVE_MEMBER, id=self.choosen)

    def set_only_admin(self, state):
        if self.updating == False:
            self.send_tag(ACTION.ONLY_ADMIN, data=bool(state))

    @property
    def choosen(self) -> str:
        return self.membersListWidget.chosen_id

    def send_tag(self, action, id="", data=None):
        if ((not id) and (data == None)) or (id == self.detail.chat_object.user.id):
            return

        dic = {"user_id": id or data}
        if isinstance(self.detail.chat_object, Group):
            dic["type"] = TYPE.GROUP
            dic["group_id"] = self.detail.chat_object.id
        else:
            dic["type"] = TYPE.CHANNEL
            dic["channel_id"] = self.detail.chat_object.id

        tag = Tag(action=action, **dic)
        self.detail.send_tag(tag)

    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)
