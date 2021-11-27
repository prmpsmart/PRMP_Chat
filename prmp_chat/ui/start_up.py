from ..backend.core import RESPONSE
from ..backend.client import LOAD, Client, User
from .widgets import *
from .home import Home, Thread


class Common(QFrame):
    def action(self):
        ...

    @property
    def className(self):
        return self.__class__.__name__

    def __init__(self, client: Client, func):
        QFrame.__init__(self)
        self.client = client
        self.func = func
        self.result = None

        self.mb = QMessageBox(self)
        self.mb.setWindowTitle(f"{self.className} Response!")

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self.username = QLineEdit()
        self.username.returnPressed.connect(lambda: self.password.setFocus())
        self.username.setPlaceholderText("Enter Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.returnPressed.connect(self.action)
        self.password.setPlaceholderText("Enter Password")

        self.password_action = QLabel(self.password)
        self.password_action.setCursor(Qt.ArrowCursor)
        self.password_action.mousePressEvent = lambda e: self.change_password_icon()
        self.password_action.setFixedSize(QSize(25, 25))
        self.password_action.setGeometry(233, 2.75, 28, 21.25)
        layout.addWidget(self.password)

        action = QPushButton()
        action.setText(self.className)
        action.clicked.connect(self.action)
        action.setStyleSheet("text-align: center;")
        layout.addWidget(action)

        for a in [self.username, self.password]:
            a.setMinimumHeight(30)

        self.hide_icon = False
        self.change_password_icon()

    def change_password_icon(self):
        if self.hide_icon:
            icon_name = "eye-off"
            self.password.setEchoMode(QLineEdit.Normal)
            self.hide_icon = False
        else:
            icon_name = "eye"
            self.password.setEchoMode(QLineEdit.Password)
            self.hide_icon = True

        self.password_action.setPixmap(QPixmap(f":chat_room/{icon_name}.svg"))


class Login(Common):
    def __init__(self, client: Client, func):
        Common.__init__(self, client, func)

        self.layout().addSpacerItem(QSpacerItem(1, self.height() / 2))

        self.username.setText("ade1")
        self.password.setText("ade1")

        self.startTimer(2000)

    def timerEvent(self, event: QTimerEvent) -> None:
        self.action()
        self.killTimer(event.timerId())

    def action(self):
        username = self.username.text()
        password = self.password.text()

        if not (username and password):
            self.mb.setText("Username and Password must be set!")
            self.mb.show()
        else:
            if self.client.alive:
                self.result = self.client.login(id=username, key=password, start=True)
                self.mb.setText(str(self.result))
                self.launch(self.mb.exec())
            else:
                self.mb.setText("Not Connected to Server!")
                self.mb.show()

    def launch(self, button):
        if self.result == RESPONSE.SUCCESSFUL:
            self.func()


class Signup(Common):
    def __init__(self, client: Client, func):
        Common.__init__(self, client, func)

        icon_frame = QFrame()
        icon_frame.setStyleSheet("background-color: orange")

        layout = self.layout()

        layout.insertWidget(0, icon_frame, stretch=2, alignment=Qt.AlignCenter)

        ic_layout = QVBoxLayout(icon_frame)
        ic_layout.setContentsMargins(2, 2, 2, 2)

        self.icon = QPushButton()
        self.icon.setStyleSheet("text-align: center;")
        self.icon.setText("Set Icon")

        self.icon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        icon_frame.setMinimumSize(150, 100)

        ic_layout.addWidget(self.icon)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter Name")
        layout.insertWidget(1, self.name)

        self.name.setMinimumHeight(30)

    def action(self):
        print("signup")


class Login_Signup(QFrame):
    def log(self, *a):
        ...

    def __init__(self, app):
        QFrame.__init__(self)
        self.app = app
        self.db = User.user_db

        self.server_settings = self.db.load_server_settings()

        layout = QVBoxLayout(self)
        self.setWindowTitle("Login or Signup")

        self.client = Client(
            **(self.server_settings or {"ip": "127.0.0.1", "port": 7767}),
            relogin=1,
            LOG=self.log,
        )

        self.setStyleSheet(GET_STYLE())

        # buttons
        frame_v = QFrame()
        frame_v.setMaximumHeight(50)
        layout_v = QHBoxLayout(frame_v)
        layout.addWidget(frame_v)

        self.login = QPushButton()
        self.login.setText("Login?")
        self.login.setStyleSheet("text-align: center;")
        self.login.clicked.connect(lambda: self.change(1))
        layout_v.addWidget(self.login)

        self.signup = QPushButton()
        self.signup.setText("Signup?")
        self.signup.setStyleSheet("text-align: center;")
        self.signup.clicked.connect(lambda: self.change(2))
        layout_v.addWidget(self.signup)

        self.advance = QPushButton()
        self.advance.setText("Connection Settings")
        self.advance.clicked.connect(lambda: self.change(3))
        layout_v.addWidget(self.advance)

        # frames
        frame_h = QFrame()
        frame_h.setMinimumSize(300, 200)
        layout.addWidget(frame_h)

        self.layout_h = QHBoxLayout(frame_h)

        self._login = Login(self.client, self.accept_login)
        self.layout_h.addWidget(self._login)

        self._signup = Signup(self.client, self.accept_signup)
        self.layout_h.addWidget(self._signup)

        self._advance = QFrame()
        self.layout_h.addWidget(self._advance)

        layout_a = QVBoxLayout(self._advance)

        self.server_ip = QLineEdit(self.server_settings.get("ip") or "")
        self.server_ip.setPlaceholderText("Server IP")
        layout_a.addWidget(self.server_ip)

        self.server_port = QLineEdit(str(self.server_settings.get("port")) or "")
        self.server_port.setPlaceholderText("Server PORT")
        layout_a.addWidget(self.server_port)

        buttons_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_server_settings)
        save_button.setStyleSheet("text-align: center;")
        buttons_layout.addWidget(save_button)

        default_button = QPushButton("Default")
        default_button.clicked.connect(self.default_server_settings)
        default_button.setStyleSheet("text-align: center;")
        buttons_layout.addWidget(default_button)

        layout_a.addLayout(buttons_layout)
        layout_a.addSpacerItem(QSpacerItem(1, self.height() / 2))

        for a in [self.server_ip, self.server_port]:
            a.setMinimumHeight(30)

        self.change()

        self.mb = QMessageBox(self)
        self.mb.setWindowTitle("Error!")

        self.status_indicator = QLabel()
        layout.addWidget(self.status_indicator, alignment=Qt.AlignHCenter)

        # timers
        self.set_status_timerId = self.startTimer(1000)
        self.connect_client_timerId = self.startTimer(500)
        self.connect_ = Thread(self, self.client._connect)

    def timerEvent(self, event: QTimerEvent):
        timerId = event.timerId()

        if timerId == self.set_status_timerId:
            self.set_status()
        elif timerId == self.connect_client_timerId:
            self.connect_client()

    def connect_client(self):
        if not self.client.alive:
            # self.client._connect()
            self.connect_.start()

    def set_status(self):
        if self.client.alive:
            color = "green"
            text = "Connected !"

        else:
            color = "red"
            text = "Not Connected ! Check Server Settings."

        self.status_indicator.setText(text)
        self.status_indicator.setStyleSheet(f"color: {color};")

    def save_server_settings(self):
        ip = self.server_ip.text()
        port = self.server_port.text()

        if not ip:
            self.mb.setText("Ip Address cannot be empty !")
            self.mb.show()

        try:
            int(port)
        except:
            self.mb.setText("Invalid Port\nMust be a number!")
            self.mb.show()

        self.db.save_server_settings(ip, port)
        self.mb.setText("Server settings saved!")
        self.mb.show()

    def default_server_settings(self):
        self.server_ip.setText("localhost")
        self.server_port.setText("7767")

    def change(self, w=1):
        if w == 1:
            self._advance.hide()
            self.login.setEnabled(0)
            self._login.show()

            self.signup.setEnabled(1)
            self._signup.hide()
            self.setFixedHeight(250)

        elif w == 2:
            self._advance.hide()
            self.login.setEnabled(1)
            self._login.hide()

            self.signup.setEnabled(0)
            self._signup.show()
            self.setFixedHeight(450)

        elif w == 3:
            self.login.setEnabled(1)
            self.signup.setEnabled(1)
            self._advance.show()
            self._login.hide()
            self._signup.hide()
            self.setFixedHeight(250)

    def accept_login(self):
        self.close()
        Home(self.app, client=self.client)

    def accept_signup(self):
        print("result")
        # Home

    def closeEvent(self, event) -> None:
        self.connect_.exit()
        return super().closeEvent(event)


def launch(app) -> QWidget:
    # user = User.load_user()
    user = LOAD()
    if user:
        w = Home(app, user=user)
    else:
        w = Login_Signup(app)
    return w
