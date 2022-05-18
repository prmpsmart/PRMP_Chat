from mimi_camera import *
import socket, threading, time


class Socket:
    def __init__(
        self, app=None, ip=None, port=None, sock: socket.socket = None, server=False
    ):
        self.app = app
        self.ip = ip
        self.port = port
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        if ip != None and port:
            func = self.bind if server else self.connect
            func(ip, port)

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except Exception as e:
            # print(e)
            ...

    def bind(self, host, port):
        self.sock.bind((host, port))

    def send(self, data):
        return self.sock.send(data)

    def recv(self, read):
        return self.sock.recv(read)

    def accept(self, time=3):
        self.sock.settimeout(time)
        return self.sock.accept()

    def listen(self, *args):
        return self.sock.listen(*args)

    def close(self):
        try:
            self.sock.setblocking(False)
            self.sock.shutdown(0)
            self.sock.close()
        except Exception as e:
            # print(e)
            ...

    def __del__(self):
        del self.sock


class VideoFeed(QApplication):
    DELIM = b"<<>>"

    def __init__(self, name="Video Feed", ip=None, port=0, server=0, demo=0):
        super().__init__()
        self.name = name
        self.demo = demo
        self.server = server

        self._sss = True

        w = 500
        w, h = w * 2, 300
        self.frame = QFrame()
        self.frame.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.frame.showEvent = self.showEvent

        if server:
            self.frame.setGeometry(20, 40, 1, 1)
        else:
            self.frame.setGeometry(900, 40, 1, 1)

        self.sock: Socket = None
        if ip != None and port:
            self.sock = Socket(self, ip, port, server=server)

        layout = QHBoxLayout(self.frame)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        self.camera = MimiCamera(
            name,
            start=server,
            min_size=(w / 2, h),
            output=1,
            receiver=self.set_view_image if demo else None,
            parent=self.frame,
        )
        layout.addWidget(self.camera)

        self.view = QLabel()
        layout.addWidget(self.view)

        args = []

        if demo:
            start = self.start_demo
        elif server:
            go = 1
            if go:
                start = self.start_server
            else:
                self.client_socket = None
                self.button = QPushButton("Send", self.camera)
                self.button.clicked.connect(self.send_data)
                start = print
            args.append(go)

        else:
            start = self.start_client

        threading.Thread(target=start, args=args).start()

        self.frame.show()
        self.frame.closeEvent = self.closeEvent
        self.exec()

    def send_data(self):
        if self.client_socket:
            try:
                data = self.get_data()
                if data:
                    self.client_socket.send(data + Socket.DELIM)
            except Exception as e:
                # print(e)
                self.start_server()
        else:
            threading.Thread(target=self.start_server).start()

    def showEvent(self, e=0):
        self.frame.setWindowTitle(f"{self.name} {self.camera.camera_device.bio()}")
        return

        h = 30
        self.button.setGeometry(0, self.camera.height() - h - 9, 50, h)

    def start_demo(self):
        if self.demo == 1:
            return

        data = self.get_data()

        if data:
            self.set_data(data)

        if self._sss:
            time.sleep(0.0000001)
            self.start_demo()

    def start_server(self, go=0):
        self.view.hide()
        self.sock.listen(5)
        while self._sss:
            try:
                self.client_socket, address = self.sock.accept(5)

                if go:
                    self.vsend(self.client_socket)

            except Exception as e:
                # print(e)
                ...

    def start_client(self):
        self.camera.hide()
        while self._sss:
            self.vreceive()
            # time.sleep(3)
            self.sock = Socket(self, ip=self.sock.ip, port=self.sock.port)

    def set_view_image(self, image):
        if (not self.server) or self.demo == 1:
            self.view.setPixmap(QPixmap(image))

    def get_data(self) -> bytes:
        data = b""
        image = self.camera.image

        if image:
            buffer = QBuffer()
            image.save(buffer, "PNG")
            data = buffer.data().data()
            buffer.close()

        return data

    def set_data(self, data: bytes):
        image = QImage.fromData(data, "PNG")
        if not image.isNull():
            self.view.setPixmap(QPixmap(image))

    def vsend(self, socket: socket.socket = None):
        socket = socket or self.sock

        while self._sss:
            data = self.get_data()
            if data:
                data += self.DELIM
                socket.send(data)

    def vreceive(self):
        chunks = b""
        while self._sss:
            chunk = b""
            try:
                chunk = self.sock.recv(9600)
            except Exception as e:
                # print(e)
                break

            if not chunk:
                break

            chunks += chunk
            datas = []

            if self.DELIM in chunks:
                datas = chunks.split(self.DELIM)

            if datas:
                if chunks.endswith(self.DELIM):
                    chunks = b""
                else:
                    chunks = datas[-1]
                    datas = datas[:-1]

                for data in datas:
                    if data:
                        self.set_data(data)

    def closeEvent(self, e):
        self._sss = False
        if self.sock:
            self.sock.close()


if __name__ == "__main__":
    VideoFeed(demo=2, server=1)
