from PySide6.QtCore import QTimer, QTimerEvent, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtMultimedia import (
    QMediaDevices,
    QCamera,
    QImageCapture,
    QMediaCaptureSession,
)


class Camera:
    def __init__(self, receiver=None, fps=24, cam=0, mirror=0):
        self.receiver = receiver
        self.fps = 0

        self.mirror = mirror

        self.camera_device = QMediaDevices.videoInputs()[cam]
        self.camera = QCamera(self.camera_device)

        self.image_capture = QImageCapture(self.camera)
        self.image_capture.imageCaptured.connect(self.image_captured)

        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        self.timer = QTimer()
        self.timer.timeout.connect(self.image_capture.capture)

        self.set_fps(fps)

    def set_fps(self, fps):
        if fps:
            self.fps = 1000 / fps
            self.timer.setInterval(self.fps)

    def image_captured(self, id: int, image: QImage):
        if self.mirror:
            image.mirror(1, 0)

        if self.receiver:
            self.receiver(image)

    def start(self):
        self.camera.start()
        self.timer.start()

    def stop(self):
        self.camera.stop()

    def isActive(self):
        return self.camera.isActive()


class MimiCamera(QLabel):
    def __init__(
        self,
        parent=None,
        fps=50,
        cam=0,
        min_size=(640, 480),
        start=False,
        output=False,
        receiver=None,
    ):
        super().__init__(parent)
        self.output = output
        self.receiver = receiver

        self.camera = Camera(self.image_captured, fps=fps, cam=cam, mirror=1)

        self.image: QImage = None
        self.timerId = 0

        if min_size:
            self.setMinimumSize(*min_size)

        if start:
            self.start()
            ...

    def image_captured(self, image: QImage):
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

    def set_fps(self, fps):
        if fps:
            self.fps = 1000 / fps

    def start(self):
        self.camera.start()

    def stop(self):
        if self.timerId:
            self.killTimer(self.timerId)

    def set_image(self, image: QImage):
        self.setPixmap(QPixmap(image))

    def timerEvent(self, event: QTimerEvent) -> None:
        self.image_capture.capture()

    def show_status_message(self, message):
        print(message)

    def closeEvent(self, event):
        if self.camera.isActive():
            self.camera.stop()
        event.accept()

    hideEvent = closeEvent

    def capture_error(self, id: int, error: QImageCapture.Error, error_string: str):
        self.show_status_message(error_string)

    def camera_error(self, error: QCamera.Error, error_string: str):
        self.show_status_message(error_string)


if __name__ == "__main__":
    app = QApplication()
    mimi = MimiCamera(start=1, output=1)
    mimi.show()
    app.exec()
