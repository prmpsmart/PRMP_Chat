from .extras import *
from .account import *


class Dialog(QDialog):
    def __init__(self, parent, home) -> None:
        super().__init__(parent, f=Qt.Popup)

        self.home = home
        self.client: Client = home.client
        self.user: User = home.user
        self.mb: QMessageBox = home.mb

        self.layout_ = QVBoxLayout(self)


class Edit_Dialog(Dialog):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        horizontalLayout_4 = QHBoxLayout()

        self.idLineEdit = QLineEdit(self)
        horizontalLayout_4.addWidget(self.idLineEdit)
        self.idLineEdit.setPlaceholderText("ID")

        self.validID = QLabel("Valid")
        self.validID.setToolTip("Valid")
        self.validID.setMinimumSize(QSize(30, 30))
        self.validID.setMaximumSize(QSize(30, 30))

        horizontalLayout_4.addWidget(self.validID)

        self.layout_.addLayout(horizontalLayout_4)

        self.chooseGroupBox = QGroupBox("Choose")
        self.chooseGroupBox.setMinimumSize(QSize(0, 50))
        self.chooseGroupBox.setMaximumSize(QSize(16777215, 50))
        horizontalLayout = QHBoxLayout(self.chooseGroupBox)
        horizontalLayout.setContentsMargins(5, 0, 5, 0)

        self.userRadioButton = QRadioButton("User")
        horizontalLayout.addWidget(self.userRadioButton)

        self.groupRadioButton = QRadioButton("Group")
        horizontalLayout.addWidget(self.groupRadioButton)

        self.channelRadioButton = QRadioButton("Channel")
        horizontalLayout.addWidget(self.channelRadioButton)

        self.layout_.addWidget(self.chooseGroupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(30)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.horizontalLayout_2.addWidget(self.buttonBox)

        self.layout_.addLayout(self.horizontalLayout_2)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


class Add_Dialog(Edit_Dialog):
    def __init__(self, parent, home) -> None:
        super().__init__(parent, home)

        self.setMinimumSize(QSize(0, 140))
        self.setMaximumSize(QSize(281, 140))

        new = QPushButton("New")
        new.clicked.connect(self.new)
        self.horizontalLayout_2.insertWidget(0, new)

    def new(self):
        newDialog = New_Dialog(self, self.home)
        newDialog.show()

    def accept(self) -> None:

        if not self.client.alive:
            self.mb.setWindowTitle("No Connection")
            self.mb.setText("Not connected to Server")
            self.mb.show()
            return

        id = self.idLineEdit.text()

        if not id:
            self.mb.setWindowTitle("Required")
            self.mb.setText("ID is required!")
            self.mb.show()
            return

        user = self.userRadioButton.isChecked()
        group = self.groupRadioButton.isChecked()
        channel = self.channelRadioButton.isChecked()

        tag = Tag(action=ACTION.ADD)
        if user:
            tag["user_id"] = id
            tag["type"] = TYPE.CONTACT
        elif group:
            tag["group_id"] = id
            tag["type"] = TYPE.GROUP
        elif channel:
            tag["channel_id"] = id
            tag["type"] = TYPE.CHANNEL
        else:
            self.mb.setText("Choose among User, Group, Channel")
            self.mb.show()
            return

        if (
            (id == self.user.id)
            or self.user.users[id]
            or self.user.groups[id]
            or self.user.channels[id]
        ):
            self.idLineEdit.setText("")
            self.mb.setWindowTitle(f"{tag.type} Exists")
            self.mb.setText(f"{tag.type} {id} already exists")
            self.mb.show()
            return

        self.client.send_action_tag(tag)

        return super().accept()


class New_Dialog(Edit_Dialog):
    def __init__(self, parent, home) -> None:
        super().__init__(parent, home)

        self.setMinimumSize(QSize(219, 241))
        self.setMaximumSize(QSize(219, 241))

        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setPlaceholderText("Name")
        self.layout_.insertWidget(0, self.nameLineEdit)

        self.userRadioButton.hide()

        self.bioPlainTextEdit = QPlainTextEdit()
        self.bioPlainTextEdit.setPlaceholderText("Bio")
        self.layout_.insertWidget(2, self.bioPlainTextEdit)

    def accept(self) -> None:
        client: Client = self.home.client

        if not client.alive:
            self.mb.setWindowTitle("No Connection")
            self.mb.setText("Not connected to Server")
            self.mb.show()
            return

        id = self.idLineEdit.text()
        name = self.nameLineEdit.text()
        bio = self.bioPlainTextEdit.toPlainText()

        if not (id and name):
            self.mb.setWindowTitle("Required")
            self.mb.setText("Name and ID are required!")
            self.mb.show()
            return

        elif id == client.user.id:
            self.idLineEdit.setText("")
            return

        group = self.groupRadioButton.isChecked()
        channel = self.channelRadioButton.isChecked()

        tag = Tag(action=ACTION.CREATE, name=name, bio=bio)
        if group:
            tag.type = TYPE.GROUP
            tag.group_id = id
        elif channel:
            tag.type = TYPE.CHANNEL
            tag.channel_id = id
        else:
            self.mb.setText("Choose among Group, Channel")
            self.mb.show()
            return

        client.send_action_tag(tag)
        self.user.pending_created_objects[tag.id] = tag

        return super().accept()


class Settings(Dialog):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        hlay = QHBoxLayout()
        self.layout_.addLayout(hlay)

        comboLabel = QLabel("Icon Set")
        comboLabel.setFrameShape(QFrame.StyledPanel)

        self.combo = QComboBox()
        self.icon_sets = ["svg", "png"]
        self.combo.addItems(self.icon_sets)
        self.combo.setCurrentIndex(self.icon_sets.index(DB.GET_ICON_SET()))
        self.combo.currentIndexChanged.connect(self.set_icon_set)

        hlay.addWidget(comboLabel)
        hlay.addWidget(self.combo)

        self.loggingButton = QPushButton()
        self.loggingButton.clicked.connect(self.logging)
        self.layout_.addWidget(self.loggingButton)

        updateData = QPushButton("Update Data")
        updateData.clicked.connect(self.updateData)
        self.layout_.addWidget(updateData)

        clearData = QPushButton("Clear Data")
        clearData.clicked.connect(self.clearData)
        self.layout_.addWidget(clearData)

        changeUser = QPushButton("Change User")
        changeUser.clicked.connect(self.changeUser)
        self.layout_.addWidget(changeUser)

        self.serve_settings = ServerSettings()
        self.serve_settings.setWindowFlag(Qt.Popup)

        serverSettings = QPushButton("Server Settings")
        serverSettings.clicked.connect(self.serverSettings)
        self.layout_.addWidget(serverSettings)

        self.update_buttons()

    def set_icon_set(self, index):
        icon_set = self.icon_sets[index]
        DB.SET_ICON_SET(icon_set)

    def updateData(self):
        self.client.send_data(self.user.id)

    def clearData(self):
        # confirm first
        DB.CLEAR_USER(self.user.id)

    def changeUser(self):
        account = Login_Signup(self.home.app, None, self.home)
        account.show()

    def serverSettings(self):
        w, h = self.pos().toTuple()
        self.serve_settings.setGeometry(w, h, 0, 0)
        self.serve_settings.show()

    def showEvent(self, event):
        print(f"{threading.active_count()=}")

    def logging(self):
        if self.client.online:
            self.client.logout(False)
        else:
            res = self.client.login()

            self.mb.setWindowTitle("LOGIN RESPONSE")
            self.mb.setText(str(res))
            self.mb.show()
        self.update_buttons()

    def update_buttons(self):
        self.loggingButton.setText("Log " + ("Out" if self.client.online else "In"))
