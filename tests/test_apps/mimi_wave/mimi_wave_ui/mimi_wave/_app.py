import socket, threading, time
from threading import Thread
from ._mimi_wave import *


def THREAD(func):
    Thread(target=func).start()


class EasySocket:
    def __init__(self, ip=None, port=None, sock: socket.socket = None, server=False):
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
        self.sock.connect((host, port))

    def bind(self, host, port):
        self.sock.bind((host, port))

    def send(self, data):
        return self.sock.send(data)

    def recv(self, read):
        return self.sock.recv(read)

    def accept(self, time=3):
        if time:
            self.sock.settimeout(time)
        return self.sock.accept()

    def listen(self, *args):
        return self.sock.listen(*args)

    def close(self):
        try:
            self.sock.setblocking(False)
            self.sock.shutdown(0)
            self.sock.close()
        except:
            ...

    def __del__(self):
        del self.sock


class _WaveApp:
    def __init__(self, windowClass: "_WaveWidget"):

        self.window = windowClass(self)

        self.start()

    def start(self):
        ...

    def closing(self):
        ...


class _Widget:
    def __init__(self, *args, **kwargs):
        ...


class _WaveWidget:
    DELIM = b"<<>>"

    def __init__(self, app: _WaveApp, title="Wave Widget", geo=()):
        self.app = app
        self._title = title
        self._geo = geo
        self.sock: EasySocket = None

        self.wave_player = WavePlayer(callback=self.playing)
        self.wave_player.pause()
        self.frames: WaveFrames = None

        self._frames_details: _Widget = None
        self._play_recording: _Widget = None
        self._server_port: _Widget = None

    def setup(self):

        self.TITLE(self._title)
        if self._geo:
            self.GEOMETRY(self._geo)

        self.SET_TEXT(self._frames_details, "Frame | Size")
        self.SET_TEXT(self._play_recording, "Play Recording")
        self.CONNECT(self._play_recording, self.play_recording)
        self.DISABLE(self._play_recording)

    def INFO(self, title, text):
        ...

    def GEOMETRY(self, geo: tuple):
        ...

    def CONNECT(self, widget, func):
        ...

    def SET_TEXT(self, widget, text):
        ...

    def GET_TEXT(self, widget) -> str:
        ...

    def GET_INT(self, widget) -> int:
        ...

    def TITLE(self, title):
        ...

    def DISABLE(self, widget):
        ...

    def ENABLE(self, widget):
        ...

    def update_frames_details(self, frames: WaveFrames):
        frames = frames or WaveFrames()

        count = frames.frame_count
        size = frames.size
        text = f"{count} F | {size} B"
        self.SET_TEXT(self._frames_details, text)

    def playing(self, state: WaveState = None, error: WaveError = None, **kwargs):
        if state:
            if state != WaveState.Complete:
                self.SET_TEXT(self._play_recording, "Stop Playing")

            else:
                self.SET_TEXT(self._play_recording, "Play Recording")
                self.wave_player.pause()
        elif error:
            print(error)

    def play_recording(self, extra=True):
        if self.frames and self.wave_player._pause and extra:
            self.wave_player.resume()
            self.wave_player.play(frames=self.frames, block=0)
        else:
            self.wave_player.pause()

    def get_port(self):
        port = self.GET_INT(self._server_port)
        if 6000 <= port <= 9000:
            return port
        else:
            self.INFO("Invalid Port", "The port should be from 6000 and 9000")

    def closing(self) -> None:
        self.wave_player.close()

        if self.sock:
            self.sock.close()

        self.app.closing()
