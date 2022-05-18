"""PySide6 Multimedia Camera Example"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *


class MimiCamera(QLabel):
    def __init__(
        self,
        name,
        parent=None,
        fps=24,
        cam=0,
        min_size=(640, 480),
        start=False,
        output=False,
        receiver=None,
    ):
        super().__init__(parent)
        self.name = name
        self.fps = 0
        self.set_fps(fps)
        self.output = output
        self.receiver = receiver

        self.camera_device = QMediaDevices.videoInputs()[cam]

        self.camera = QCamera(self.camera_device)
        self.camera.errorOccurred.connect(self.camera_error)

        self.image_capture = QImageCapture(self.camera)
        self.image_capture.imageCaptured.connect(self.image_captured)
        self.image_capture.errorOccurred.connect(self.capture_error)

        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        self.image: QImage = None
        self.timerId = 0

        if min_size:
            self.setMinimumSize(*min_size)

        if start:
            self.start()

    def set_fps(self, fps):
        if fps:
            self.fps = 1000 / fps

    def start(self):
        self.timerId = self.startTimer(self.fps)
        self.camera.start()

    def stop(self):
        if self.timerId:
            self.killTimer(self.timerId)

    def image_captured(self, id: int, image: QImage):
        image.mirror(1, 0)
        image = image.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.image = image
        if self.output:
            self.set_image(image)

        if self.receiver:
            self.receiver(image)

    def set_image(self, image: QImage):
        self.setPixmap(QPixmap(image))

    def timerEvent(self, event: QTimerEvent) -> None:
        res = self.image_capture.capture()

    def show_status_message(self, message):
        print(message)

    def closeEvent(self, event):
        if self.camera and self.camera.isActive():
            self.camera.stop()
        event.accept()

    def capture_error(self, id: int, error: QImageCapture.Error, error_string: str):
        self.show_status_message(error_string)

    def camera_error(self, error: QCamera.Error, error_string: str):
        self.show_status_message(error_string)
