from .widgets import *

class Login(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        # layout.setContentsMargins(10, 10, 10, 10)

        self.username = QLineEdit()
        self.username.setPlaceholderText('Enter Username')
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Enter Password')
        layout.addWidget(self.password)

        self.action = QPushButton()
        self.action.setText('Login')
        self.action.clicked.connect(self.login)
        layout.addWidget(self.action)
        layout.addSpacerItem(QSpacerItem(1, self.height()/2))

    
    def login(self):
        print('login')


class Signup(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        # layout.setContentsMargins(10, 10, 10, 10)

        icon_frame = QFrame()
        icon_frame.setStyleSheet('background-color: orange')
        layout.addWidget(icon_frame)

        ic_layout = QVBoxLayout(icon_frame)
        ic_layout.setContentsMargins(2, 2, 2, 2)

        self.icon = QPushButton()
        self.icon.setStyleSheet(BUTTON_ICON)
        self.icon.setText('Enter Icon')
        
        self.icon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        icon_frame.setMaximumSize(150, 100)

        ic_layout.addWidget(self.icon)

        self.name = QLineEdit()
        self.name.setPlaceholderText('Enter Name')
        layout.addWidget(self.name)

        self.username = QLineEdit()
        self.username.setPlaceholderText('Enter Username')
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Enter Password')
        layout.addWidget(self.password)

        self.action = QPushButton()
        self.action.setText('Signup')
        self.action.clicked.connect(self.signup)
        layout.addWidget(self.action)
    
    def signup(self):
        print('signup')


class Login_Signup(QFrame):
    def __init__(self):
        QFrame.__init__(self)

        layout = QVBoxLayout(self)
        self.setWindowTitle('Login or Signup')
        
        # buttons
        frame_v = QFrame()
        frame_v.setMaximumHeight(50)
        layout_v = QHBoxLayout(frame_v)
        layout.addWidget(frame_v)

        self.signup = QPushButton()
        self.signup.setText('Signup?')
        self.signup.clicked.connect(lambda: self.change(1))
        layout_v.addWidget(self.signup)

        self.login = QPushButton()
        self.login.setText('Login?')
        self.login.clicked.connect(lambda: self.change(2))
        layout_v.addWidget(self.login)
        
        advance = QPushButton()
        advance.setText('Connection Settings')
        advance.clicked.connect(lambda: self.change(3))
        layout_v.addWidget(advance)

        # frames
        frame_h = QFrame()
        frame_h.setMinimumSize(300, 200)
        layout.addWidget(frame_h)
        
        self.layout_h = QHBoxLayout(frame_h)

        self._login = Login()
        self._login.hide()
        self._signup = Signup()

        self._advance = QFrame()
        layout_a = QVBoxLayout(self._advance)
        self._advance.hide()

        self.server_ip = QLineEdit()
        self.server_ip.setPlaceholderText('Server IP')
        layout_a.addWidget(self.server_ip)

        self.server_port = QLineEdit()
        self.server_port.setPlaceholderText('Server PORT')
        layout_a.addWidget(self.server_port)
        layout_a.addSpacerItem(QSpacerItem(1, self.height()/2))


        self.layout_h.addWidget(self._signup)
        self.layout_h.addWidget(self._login)
        self.layout_h.addWidget(self._advance)
    
        self.change()

    def change(self, w=1):
        if w == 1:
            self._advance.hide()
            self.login.setEnabled(1)
            self._login.hide()

            self.signup.setEnabled(0)
            self._signup.show()
            self.setMinimumHeight(400)
            
        elif w == 2:
            self._advance.hide()
            self.login.setEnabled(0)
            self._login.show()
            
            self.signup.setEnabled(1)
            self._signup.hide()
            self.setMinimumHeight(200)
        
        elif w == 3:
            self.login.setEnabled(1)
            self.signup.setEnabled(1)
            self._advance.show()
            self._login.hide()
            self._signup.hide()

