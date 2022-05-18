import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from tests.test_apps.mimi_wave.mimi_wave_ui.mimi_wave._mimi_wave import WaveFrames


app = QGuiApplication()


buffer = QBuffer()
buffer.open(QIODevice.WriteOnly | QIODevice.Truncate)

format = QAudioFormat()

format.setSampleRate(44400)
format.setChannelCount(1)
format.setSampleFormat(QAudioFormat.Int16)


audio_source = QAudioSource(format)
audio_sink = QAudioSink(format)


def handleStateChanged(newState):

    if newState == QAudio.State.ActiveState:
        print("Recording ...")

    elif newState == QAudio.State.StoppedState:
        print("Done ...")

    else:
        print(newState)


audio_source.stateChanged.connect(handleStateChanged)


audio_source.start(buffer)


def stopRecording():
    audio_source.stop()

    print(len(buffer.data()))

    buffer.close()
    buffer.open(QIODevice.ReadOnly)

    audio_sink.start(buffer)

    QTimer.singleShot(3000, app.quit)


QTimer.singleShot(3000, stopRecording)

app.exec()
