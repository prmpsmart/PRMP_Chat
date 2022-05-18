import sys

sys.path.append("prmp_chat")
from prmp_chat.chat_ui.extras import *


app = QApplication()


def output(image: QImage):
    print(image)


w = ImageChooser(output, None, app)
w.show()

app.exec()
