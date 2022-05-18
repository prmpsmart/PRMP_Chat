from prmp_reloader import PRMP_Reloader, os
from chat import Chat_App

# from chat import QApplication
# from chat_ui.call import Call_App as Chat_App
# from chat_ui.call import CameraCapture


# class Chat_App(QApplication):
#     def __init__(self):
#         super().__init__()

#         self.window = CameraCapture()

#     def start(self):
#         self.window.show()
#         self.exec()


if "r" in os.sys.argv:
    app = Chat_App()
    app.start()
else:
    PRMP_Reloader(Chat_App)
