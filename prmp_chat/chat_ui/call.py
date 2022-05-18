from .extras import *
from backend.client import Client
from .mimi_plarec import Player, Recorder


class _Call_Dialog(QDialog):
    def __init__(self, parent=None, isVideo=True) -> None:
        super().__init__(parent)
        self.image: QImage = None

        self.isVideo = isVideo
        self.switched = False

        self.active = False

        self.layout_ = QVBoxLayout(self)
        SET_MARGINS(self.layout_)

        hlay = QHBoxLayout()
        self.layout_.addLayout(hlay)

        self.view = QLabel()
        self.view.setMinimumSize(470, 268)
        self.view.setAlignment(Qt.AlignCenter)
        hlay.addWidget(self.view)

        pre_lay = QVBoxLayout()
        hlay.addLayout(pre_lay)

        pre_lay.setAlignment(Qt.AlignBottom)

        self.preview = QLabel()
        self.preview.setFrameShape(QFrame.StyledPanel.Box)
        self.preview.setStyleSheet("border-color: lime")
        self.preview.setMinimumSize(250, 141)
        pre_lay.addWidget(self.preview)

        bottomLay = QHBoxLayout()
        self.layout_.addLayout(bottomLay)

        self.switch_camera = QPushButton("Switch Camera")
        self.switch_camera.clicked.connect(self.switchCamera)
        bottomLay.addWidget(self.switch_camera)

        self.hide_detail = QPushButton("Hide Detail")
        self.hide_detail.clicked.connect(self.hideDetail)
        bottomLay.addWidget(self.hide_detail)

        mute_audio = QPushButton("Mute Audio")
        bottomLay.addWidget(mute_audio)

        cut = QPushButton("Cut")
        cut.clicked.connect(self.cut)
        bottomLay.addWidget(cut)

        background_layout = QVBoxLayout(self.view)
        background_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.caller_detail = QFrame()
        background_layout.addWidget(self.caller_detail)

        caller_detail_layout = QVBoxLayout(self.caller_detail)
        caller_detail_layout.setAlignment(Qt.AlignCenter)

        self.imageButton = QPushButton("Image")
        h = 100
        self.imageButton.setMinimumSize(h, h)
        self.imageButton.setMaximumSize(h, h)
        self.imageButton.setStyleSheet("border-radius: 50px; background: white")
        caller_detail_layout.addWidget(self.imageButton)

        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignCenter)
        caller_detail_layout.addWidget(self.nameLabel)

        self.statusLabel = QLabel("Calling...")
        self.statusLabel.setAlignment(Qt.AlignCenter)
        caller_detail_layout.addWidget(self.statusLabel)

        self.player = Player()
        self.recorder = Recorder()
        self.camera = Camera(receiver=self.imageCapture, mirror=1)

    def imageCapture(self, image: QImage):
        self.image = image
        self.viewPixmap(image)

    def getScaledPixmap(self, image: QImage, label: QLabel) -> QPixmap:
        aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio
        aspectMode = Qt.AspectRatioMode.KeepAspectRatio
        # aspectMode = Qt.AspectRatioMode.KeepAspectRatioByExpanding

        transform = Qt.TransformationMode.FastTransformation
        transform = Qt.TransformationMode.SmoothTransformation

        if label == self.view:
            image = image.scaled(label.size(), aspectMode, transform)
        else:
            image = image.scaledToWidth(label.width(), transform)

        return QPixmap(image)

    def viewPixmap(self, image: QImage):
        pixmap = self.getScaledPixmap(image, self.view)
        self.view.setPixmap(pixmap)

    def previewPixmap(self, image: QImage):
        pixmap = self.getScaledPixmap(image, self.preview)
        self.preview.setPixmap(pixmap)

    def switchCamera(self):
        self.preview, self.view = self.view, self.preview
        self.switched = not self.switched

    def hideDetail(self):
        if self.caller_detail.isVisible():
            self.caller_detail.hide()
            self.hide_detail.setText("Show Detail")
        else:
            self.caller_detail.show()
            self.hide_detail.setText("Hide Detail")

    def muteAudio(self):
        ...

    def cut(self):
        ...

    def setIsVideo(self, isVideo):
        self.isVideo = isVideo
        self.update_call()

    def update_call(self):
        if self.isVideo:
            self.switch_camera.show()
            self.preview.show()
            self.caller_detail.setStyleSheet("background: transparent")
            self.camera.start()
        else:
            self.view.setStyleSheet("background: green;")
            self.view.setPixmap(QPixmap())
            self.switch_camera.hide()
            self.preview.hide()
            self.camera.stop()

    def showEvent(self, event: QShowEvent):
        self.update_call()
        self.statusLabel.setText("Calling...")
        self.active = True

    def closeEvent(self, event: QCloseEvent) -> None:
        self.active = False
        self.camera.stop()
        self.player.stop()
        self.recorder.stop()

    hideEvent = closeEvent


class Call_Dialog(_Call_Dialog):
    def __init__(self, home, **kwargs) -> None:
        super().__init__(home, **kwargs)
        self.client: Client = home.client
        self.mode = True
        self.contact: Contact = None

    def muteAudio(self):
        ...

    def cut(self):
        ...

    def imageCapture(self, image: QImage):
        super().imageCapture(image)

        # image.mirror(1, 0)
        # self.previewPixmap(image)

    def set_contact(self, contact: Contact):
        self.contact = contact

        if self.contact.icon:
            self.imageButton.setIcon(GET_ICON(self.contact.icon, "user"))
            self.imageButton.setText("")

        self.nameLabel.setText(self.contact.name)
        self.setWindowTitle(
            ("Video" if self.isVideo else "Audio") + f" call from {self.contact.id}"
        )

    def set_mode(self, mode: bool):
        self.mode = mode
        if not mode:
            self.camera.stop()

    def send_request(self, contact: Contact, isVideo: bool):
        self.set_mode(True)
        self.setIsVideo(isVideo)
        self.set_contact(contact)

        self.client.send_action_tag(
            Tag(
                action=ACTION.CALL_REQUEST,
                recipient=self.contact.id,
                sender=self.client.user.id,
                call="VIDEO" if self.isVideo else "AUDIO",
            )
        )

    def receive_request(self, sender: str):
        self.set_mode(False)

        user = self.client.user.users[sender]
        if user:
            self.set_contact(user)
            self.show()

    def receive_response(self, tag: Tag):
        sender, response = tag["sender", "response"]
        if sender == self.contact.id:
            self.statusLabel.setText(f"{response}")
            if response == RESPONSE.ACCEPTED:
                self.switchCamera()
                self.hideDetail()
                Thread(self, self.send_data).start()

            else:
                ...

    def send_data(self):
        while (
            self.active and self.client.online and self.contact.status == STATUS.ONLINE
        ):
            if self.image:
                data = GET_IMAGE_DATA(self.image)

                tag = Tag(
                    action=ACTION.CALL,
                    recipient=self.contact.id,
                    sender=self.client.user.id,
                    call="VIDEO" if self.isVideo else "AUDIO",
                    data=data,
                )

                self.client.send_action_tag(tag)

    def receive_data(self, tag: Tag):
        if self.isVideo:
            if tag.sender == self.contact.id:
                image = GET_PIXMAP(tag.raw_data, None)
                if not image.isNull():
                    self.previewPixmap(image)


class Call_Notify(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.call_dialog: Call_Dialog = parent.call_dialog
        self.client: Client = parent.client
        self.tag: Tag = None

        lay = QVBoxLayout(self)

        self.label = QLabel()
        lay.addWidget(self.label)

        hlay = QHBoxLayout()
        lay.addLayout(hlay)

        accept = QPushButton("Accept")
        accept.clicked.connect(self.accept_)
        hlay.addWidget(accept)

        decline = QPushButton("Decline")
        decline.clicked.connect(self.decline_)
        hlay.addWidget(decline)

    def accept_(self):
        self.send_tag(1)

    def decline_(self):
        self.send_tag(0)

    def send_tag(self, accepted):
        self.tag.action = ACTION.CALL_RESPONSE
        self.tag.response = RESPONSE.ACCEPTED if accepted else RESPONSE.DECLINED
        recipient, sender = self.tag["recipient", "sender"]
        self.tag.recipient = sender
        self.tag.sender = recipient
        self.client.send_action_tag(self.tag)

        self.close()

        if accepted:
            self.call_dialog.receive_request(sender)

    def loadTag(self, tag: Tag):
        self.tag = tag
        action, sender, call = tag["action", "sender", "call"]
        self.setWindowTitle(f"{action} FROM {sender}")
        self.label.setText(f"A {call} CALL REQUEST from {sender}")
        self.show()

    def showEvent(self, arg__1: QShowEvent) -> None:
        return super().showEvent(arg__1)

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        return super().closeEvent(arg__1)
