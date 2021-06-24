from core.chats import *
import file, sys
from PySide6.QtCore import (
    QAbstractListModel,
    QMargins,
    QPoint,
    QRectF,
    Qt,
    QSize,
    QRect,
    QDateTime,
    
)
from PySide6.QtGui import (
    QColor,
    QTextDocument,
    QTextOption,
    QFont,
    QFontMetrics,
    QStandardItem,
    QStandardItemModel,
    QPalette,
    QIcon,
    QPixmap
)

# from PySide6.QtGui

from PySide6.QtWidgets import *





class Demo(QWidget):
    def __init__(self, a):
        super().__init__()
                
        rect = a.screens()[0].availableGeometry()
        s = 500
        ss = s/2
        geo = QRect(int(rect.width()/2-ss), int(rect.height()/2-ss), s, s)
        self.setGeometry(geo)
        self.setMinimumWidth(s)

        layoutMain = QVBoxLayout(self)
        chatList = ChatList(self)

        account = QIcon(":/chat_room/images/account.png")
        emoji = QIcon(":/chat_room/images/emoji_people.png")
        back = QIcon(":/chat_room/images/back.png")

        currentDateTime = QDateTime.currentDateTime()

        chatList.addChat(emoji, "currentDateTime", currentDateTime, "This is some text of a war, p", 20)
        chatList.addChat(emoji, "ctDateTime", currentDateTime, "This is some text of a warning message", 30000)
        chatList.addChat(back, "cunteTime", currentDateTime, "This is some text of an error message somes is some text of an error message some")
        chatList.addChat(account, "good", currentDateTime, "This is some text of an info message", 500)
        
        layoutMain.addWidget(chatList);
        self.resize(640, 480)


class MainWindow(QMainWindow):

    def __init__(self, a) -> None:
        super().__init__()
        
        l = QVBoxLayout()

        self.message_input = QLineEdit("Enter messiui oiu age here")

        # Buttons for from/to messages.
        self.btn1 = QPushButton("<")
        self.btn2 = QPushButton(">")

        self.messages = ChatRoomList(self)
        
        self.btn1.pressed.connect(lambda: self.messages._model.add_message(1, self.message_input.text()))
        self.btn2.pressed.connect(lambda: self.messages._model.add_message(0, self.message_input.text()))

        for a in range(4):
            self.messages._model.add_message(a%2, self.message_input.text())
            break

        l.addWidget(self.messages)
        l.addWidget(self.message_input)
        hh = QHBoxLayout()
        hh.addWidget(self.btn1)
        hh.addWidget(self.btn2)
        l.addLayout(hh)
        
        self.w = QWidget()
        self.w.setLayout(l)
        self.setCentralWidget(self.w)




a = QApplication(sys.argv)
window = Demo(a)
# window = MainWindow()
window.show()
a.exec_()


