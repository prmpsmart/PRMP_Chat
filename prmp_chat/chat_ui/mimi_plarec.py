from typing import Callable, Union
from wave import Wave_read, Wave_write
from enum import Enum
from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtMultimedia import QAudio, QAudioSink, QAudioSource, QAudioFormat

__author__ = "PRMPSmart - Mimi Peach"
__all__ = ["PlaRec", "Recorder", "Player"]


class Mode(Enum):
    Input = 1
    Output = 0


class PlaRec:
    def __str__(self) -> str:
        return self.__class__.__name__

    def __init__(
        self,
        mode: Mode,
        stateReceiver: Callable[[QAudio.State], None] = None,
        log=False,
        **kwargs,
    ) -> None:
        """
        mode - True for input and False for output
        """

        self.byteArray = QByteArray()
        self.audio: Union[QAudioSource, QAudioSink] = None
        self.__mode: Mode = None
        self.stateReceiver = stateReceiver
        self.log = log
        self.state: QAudio.State = QAudio.State.StoppedState

        self.setMode(mode)
        self.createAudio(**kwargs)

    @property
    def mode(self):
        return self.__mode

    def setMode(self, mode: Mode):
        assert isinstance(mode, Mode)

        if mode != self.__mode:
            self.__mode = mode
            if self.audio:
                self.createAudio(
                    rate=self.rate,
                    channels=self.channels,
                    format=self.format,
                )

    def createAudio(self, **kwargs):
        audio_format = self.getAudioFormat(**kwargs)

        audioClass = QAudioSource if self.isInput else QAudioSink
        self.audio: Union[QAudioSource, QAudioSink] = audioClass(audio_format)
        self.audio.stateChanged.connect(self.stateChanged)

    def getAudioFormat(
        self,
        rate: int = 44400,
        channels: int = 1,
        format: QAudioFormat.SampleFormat = QAudioFormat.Int16,
    ) -> None:
        audio_format = QAudioFormat()
        audio_format.setSampleRate(rate)
        audio_format.setChannelCount(channels)
        audio_format.setSampleFormat(format)

        return audio_format

    @property
    def audio_format(self) -> QAudioFormat:
        return self.audio.format()

    @property
    def isInput(self) -> bool:
        return self.__mode == Mode.Input

    @property
    def rate(self) -> int:
        return self.audio_format.sampleRate()

    @property
    def sampleWidth(self) -> int:
        if self.format == QAudioFormat.UInt8:
            return 1
        elif self.format == QAudioFormat.Int16:
            return 2
        elif self.format == QAudioFormat.Int32:
            return 3
        elif self.format == QAudioFormat.Float:
            return 4
        elif self.format == QAudioFormat.NSampleFormats:
            return 5
        else:
            return 0

    @classmethod
    def getFormatFromWidth(cls, width) -> QAudioFormat.SampleFormat:
        if width == 1:
            return QAudioFormat.UInt8
        elif width == 2:
            return QAudioFormat.Int16
        elif width == 3:
            return QAudioFormat.Int32
        elif width == 4:
            return QAudioFormat.Float
        elif width == 5:
            return QAudioFormat.NSampleFormats
        else:
            return QAudioFormat.Unknown

    @property
    def channels(self) -> int:
        return self.audio_format.channelCount()

    @property
    def format(self) -> QAudioFormat.SampleFormat:
        return self.audio_format.sampleFormat()

    @property
    def data(self) -> bytes:
        return self.byteArray.data()

    def duration(self, bytes: bytes = b"") -> int:
        size = len(bytes)
        rate = self.rate
        dura = size / rate / 2
        return dura

    @property
    def bytes(self) -> bytes:
        return self.data

    def reset(self):
        self.audio.reset()

    def resume(self):
        self.audio.resume()

    def suspend(self):
        self.audio.suspend()

    def start(self, byteArray: QByteArray = None, new: bool = False) -> QByteArray:
        byteArray = byteArray or self.byteArray
        buffer = QBuffer(byteArray)

        openMode = QIODevice.ReadWrite

        if new:
            buffer.setData(b"")

        elif self.isInput:
            openMode = QIODevice.Append

        buffer.open(openMode)

        if self.isInput:
            self.audio.start(buffer)
            return byteArray

        else:
            self.audio.start(buffer)

    def stop(self):
        self.audio.stop()

    def setVolume(self, volume: int):
        self.audio.setVolume(volume)

    @property
    def active(self):
        return self.state == QAudio.State.ActiveState

    @property
    def volume(self) -> int:
        self.audio.volume()

    def stateChanged(self, newState: QAudio.State):
        self.state = newState

        if newState == QAudio.State.ActiveState:
            if self.log:
                print(f"{self} Session Started ...")

        elif newState == QAudio.State.IdleState:
            ...

        elif newState == QAudio.State.SuspendedState:
            if self.log:
                print(f"{self} Session Suspended")

        elif newState == QAudio.State.StoppedState:

            if self.log:
                print(f"{self} Session Ended ...")

        if self.stateReceiver:
            self.stateReceiver(newState)


class Recorder(PlaRec):
    def __init__(self, **kwargs) -> None:
        super().__init__(mode=Mode.Input, **kwargs)

    def record(self, byteArray: QByteArray = None, **kwargs) -> QByteArray:
        return self.start(byteArray=byteArray, **kwargs)

    def save(self, file: str):
        data = self.data
        if data:
            wave_write = Wave_write(file)
            wave_write.setnchannels(self.channels)
            wave_write.setsampwidth(self.sampleWidth)
            wave_write.setframerate(self.rate)
            wave_write.writeframes(data)
            wave_write.close()


class Player(PlaRec):
    def __init__(self, **kwargs) -> None:
        super().__init__(mode=Mode.Output, **kwargs)

    def play(self, data: bytes = b"", byteArray: QByteArray = None, file: str = ""):
        if file:
            wave_read = Wave_read(file)
            channels = wave_read.getnchannels()
            sampleWidth = wave_read.getsampwidth()
            rate = wave_read.getframerate()
            data = wave_read.readframes(wave_read.getnframes())
            wave_read.close()

            self.createAudio(
                channels=channels,
                format=self.getFormatFromWidth(sampleWidth),
                rate=rate,
            )

        if data:
            self.byteArray.setRawData(data, len(data))

        self.start(byteArray=byteArray)


if __name__ == " __main__":
    app = QGuiApplication()

    recorder = Recorder(log=1)
    byteArray = recorder.record()

    def quit(state):
        print(state)
        if state != QAudio.State.ActiveState:
            app.quit()

    player = Player(stateReceiver=quit, log=1)

    def record():
        recorder.stop()

        player.play(byteArray=byteArray)

    QTimer.singleShot(5000, record)

    app.exec()
