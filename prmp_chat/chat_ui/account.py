from .extras import *


class Login(QFrame):
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
        self.username.setClearButtonEnabled(True)
        self.username.returnPressed.connect(lambda: self.password.setFocus())
        self.username.setPlaceholderText("Enter Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setClearButtonEnabled(True)
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

        self.username.setText("ade")

    def change_password_icon(self):
        if self.hide_icon:
            icon_name = "eye-off"
            self.password.setEchoMode(QLineEdit.Normal)
            self.hide_icon = False
        else:
            icon_name = "eye"
            self.password.setEchoMode(QLineEdit.Password)
            self.hide_icon = True

        self.password_action.setPixmap(QPixmap(f":icons/{icon_name}.svg"))

    def action(self):
        username = self.username.text()
        password = self.password.text()

        if not (username and password):
            self.mb.setText("Username and Password must be set!")
        else:
            if self.client.alive:
                # user = DB.GET_USER(username)
                self.result = self.client.login(id=username, key=password)

                self.mb.setText(str(self.result))

                if self.result == RESPONSE.SUCCESSFUL:
                    self.func()
                    return

            else:
                self.mb.setText("Not Connected to Server!")

        self.mb.show()


class Signup(Login):
    def __init__(self, client: Client, func):
        super().__init__(client, func)

        layout = self.layout()

        self.name = QLineEdit()
        self.name.setClearButtonEnabled(True)
        self.name.setPlaceholderText("Enter Name")
        layout.insertWidget(0, self.name)

        self.name.setMinimumHeight(30)

    def action(self):
        name = self.name.text()
        username = self.username.text()
        password = self.password.text()

        if not (username and password):
            self.mb.setText("Username and Password must be set!")
        else:
            if self.client.alive:
                self.result = self.client.signup(id=username, key=password, name=name)

                self.mb.setText(str(self.result))
                if self.result == RESPONSE.SUCCESSFUL:
                    self.mb.show()
                    self.func()
                    return

                elif self.result == RESPONSE.EXIST:
                    self.mb.setText(f"Username '{username}' already EXIST!")
            else:
                self.mb.setText("Not Connected to Server!")
        self.mb.show()


class Login_Signup(Window):
    def log(self, *a):
        ...

    def __init__(self, app, Home=None, home=None):
        super().__init__(app)
        self.Home = Home
        self.home = home

        self.server_settings = ServerSettings()

        if home:
            self.client = home.client
        else:
            self.client = Client(
                **(
                    self.server_settings.server_settings
                    or {"ip": "127.0.0.1", "port": 7767}
                ),
                relogin=1,
                LOG=self.log,
            )

        self.mb = self.server_settings.mb

        # timers
        self.set_status_timerId = self.startTimer(1000)
        self.connect_client_timerId = self.startTimer(500)

        self.connect_ = Thread(self, self.client._connect)

        layout = QVBoxLayout(self)
        self.setWindowTitle("Login or Signup")

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
        self.advance.setText("Server Settings")
        self.advance.clicked.connect(lambda: self.change(3))
        layout_v.addWidget(self.advance)

        # frames
        frame_h = QFrame()
        layout.addWidget(frame_h)

        self.layout_h = QHBoxLayout(frame_h)

        self._login = Login(self.client, self.accept_login)
        self.layout_h.addWidget(self._login)

        self._signup = Signup(self.client, self.accept_signup)
        self.layout_h.addWidget(self._signup)

        self.layout_h.addWidget(self.server_settings)

        self.change()

        self.status_indicator = QLabel()
        layout.addWidget(self.status_indicator, alignment=Qt.AlignHCenter)

    def timerEvent(self, event: QTimerEvent):
        timerId = event.timerId()

        if timerId == self.set_status_timerId:
            self.set_status()
        elif timerId == self.connect_client_timerId:
            self.connect_client()

    def connect_client(self):
        if not self.client.alive:
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

    def change(self, w=1):
        if w == 1:
            self.advance.setEnabled(1)
            self.server_settings.hide()

            self.login.setEnabled(0)
            self._login.show()

            self.signup.setEnabled(1)
            self._signup.hide()

        elif w == 2:
            self.advance.setEnabled(1)
            self.server_settings.hide()

            self.login.setEnabled(1)
            self._login.hide()

            self.signup.setEnabled(0)
            self._signup.show()

        elif w == 3:
            self.login.setEnabled(1)
            self._login.hide()

            self.signup.setEnabled(1)
            self._signup.hide()

            self.advance.setEnabled(0)
            self.server_settings.show()

    def accept_login(self):
        self.close()

        if self.home:
            self.home.reload_home()

        else:
            self.app.window = self.Home(self.app, client=self.client)
            self.app.window.show()

    def accept_signup(self):
        self.change()

    def closeEvent(self, event) -> None:
        self.connect_.exit()
        return super().closeEvent(event)
