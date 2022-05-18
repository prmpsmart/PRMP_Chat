from chat_ui.account import Login_Signup
from chat_ui.home import Home, QApplication, Qt
from backend.client import DB


class Chat_App(QApplication):
    def __init__(self):
        super().__init__()

        DB.LOAD()

        user = DB.GET_LAST_USER()

        if user:
            self.window = Home(self, user=user)
            # self.window.setWindowFlag(Qt.WindowStaysOnBottomHint)
        else:
            self.window = Login_Signup(self, Home)
            self.window.setWindowFlag(Qt.WindowStaysOnTopHint)

    def start(self):
        self.window.show()
        self.exec()
