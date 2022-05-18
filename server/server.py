from importlib import reload
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from threading import Thread, active_count

import prmp_chat.backend.server as server


class Button(QPushButton):
    def __init__(self, layout: QHBoxLayout, text, command=None, max=1):
        super().__init__(text)
        layout.addWidget(self)
        if command:
            self.clicked.connect(command)
        if max:
            self.setMaximumWidth(50)


class Log(QFrame):
    def showEvent(self, event: QShowEvent) -> None:
        if self.func:
            self.func()
        return super().showEvent(event)

    def __init__(self, layout: QVBoxLayout, text, func=None):
        super().__init__()

        layout.addWidget(self)
        self.func = func

        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)

        hlayout.addWidget(QLabel(text + " LOG: "))

        self.log = QTextBrowser()
        self.vertical = self.log.verticalScrollBar()
        vlayout.addWidget(self.log)

        hlayout.addSpacerItem(QSpacerItem(50, 1, hData=QSizePolicy.Fixed))

        clear = Button(hlayout, "Clear " + text + " LOG", self.log.clear, max=0)

        hlayout.addSpacerItem(QSpacerItem(1, 1, hData=QSizePolicy.Expanding))

        self.startTimer(200)

    def timerEvent(self, event):
        if not self.hasFocus():
            self.vertical.setValue(self.vertical.maximum())

    def insertPlainText(self, text):
        self.log.insertPlainText(text)


class ServerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.server = None
        self.thread: Thread = None

        self.setWindowTitle("Chat Server")

        layout = QVBoxLayout(self)

        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)

        Button(buttonLayout, "Start", self.start)
        Button(buttonLayout, "Restart", self.restart)
        Button(buttonLayout, "Stop", self.stop)
        self.Switch = Button(buttonLayout, "Switch", self.switch)
        self.clients = Button(buttonLayout, "", self.switch)

        buttonLayout.addSpacerItem(QSpacerItem(1, 1, hData=QSizePolicy.Expanding))

        self.status = QLabel()

        font = QFont("Maiandra GD", 15, 2)
        self.status.setToolTip("Press to Reload")

        font.setBold(True)
        self.status.setFont(font)
        self.status.setMargin(5)
        buttonLayout.addWidget(self.status)

        self.server_log = Log(layout, "Server")
        self.error_log = Log(layout, "Error", func=self.lightSwitch)
        self.error_log.hide()

        self.mb = QMessageBox()

        self.update_status()

        self.startTimer(100)

        screens = QApplication.screens()
        if len(screens) > 1:
            self.setScreen(screens[1])

        self.moveToScreen()

    def moveToScreen(self):
        screen_geo = self.screen().availableGeometry()
        self.move(screen_geo.left() + 10, 20)

    def timerEvent(self, event):
        self.clients.setText(str(len(server.USERS_SESSIONS)))

    def switch(self):
        print(f"{active_count()=}")

        if self.server_log.isVisible():
            self.server_log.hide()
            self.error_log.show()
        else:
            self.error_log.hide()
            self.server_log.show()

    def lightSwitch(self):
        self.Switch.setStyleSheet("")

    def update_status(self):
        if self.server:
            status = "Online"
            color = "green"
        else:
            status = "Offline"
            color = "red"

        self.status.setText(status)
        self.status.setStyleSheet(
            f"background: {color}; color: white; border-radius: 8px;"
        )

    def getText(self, args):
        text = ", ".join([str(arg) for arg in args]) + "\n"
        print(text)
        return text

    def write(self, *args):
        text = self.getText(args)
        if self.isVisible():
            if not self.server_log.isVisible():
                self.switch()
            self.server_log.insertPlainText(text)

    def errorWrite(self, *args):
        text = self.getText(args)
        # if not self.error_log.isVisible():
        #     self.switch()
        if self.isVisible():
            self.Switch.setStyleSheet("background: red")
            self.error_log.insertPlainText(text)

    def start(self):
        if self.server:
            self.mb.setWindowTitle("Server Start")
            self.mb.setText("Server is already started")
            return

        self.server_log.log.clear()

        reload(server)

        Server, server_test = server.Server, server.server_test
        server_test()

        # return

        self.server = Server(LOG=self.write, ERROR_LOG=self.errorWrite)

        self.thread_start()
        self.update_status()

        if not self.server_log.isVisible():
            self.switch()

    def thread_start(self):
        if self.server:
            Thread(target=self.server.start).start()

    def restart(self):
        self.stop()
        self.start()
        self.error_log.log.clear()
        self.lightSwitch()

    def stop(self, o=0):
        if self.server:
            self.server.stop()
            del self.server
            self.server = None

            if not o:
                self.update_status()

    def showEvent(self, event: QCloseEvent) -> None:
        self.start()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.stop(1)


class ServerApp(QApplication):
    def __init__(self):
        super().__init__()

        self.window = ServerWindow()
        self.startTimer(5000)

    def timerEvent(self, event):
        server.SAVE()

    def start(self):
        self.window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.window.show()
        self.exec()
