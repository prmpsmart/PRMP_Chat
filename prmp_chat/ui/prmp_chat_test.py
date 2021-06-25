from prmp_chat.backend.core import ACTION
import sys
from prmp_chat.backend.client import *

from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QIcon

dt = QDateTime.currentDateTime()


account = QIcon(":/chat_room/images/account.png")
emoji = QIcon(":/chat_room/images/emoji_people.png")
back = QIcon(":/chat_room/images/back.png")


selfUser = Client_User(id='prmpsmart', name='Apata Miracle', key='princerm', icon=account)
# selfUser.change_status(STATUS.ONLINE)

user1 = Other_User(id='omolewa', name='Aderemi Goodness', icon=account)
user2 = Other_User(id='adelove', name='Aderemi Loveth', icon=back)

chat1 = Tag(action=ACTION.CHAT, sender=user1.id, recipient=selfUser.id, data='I love you very much', date_time=dt)
chat3 = Tag(action=ACTION.CHAT, sender=user2.id, recipient=selfUser.id, data='I love you ', date_time=dt)
chat5 = Tag(action=ACTION.CHAT, sender=user2.id, recipient=selfUser.id, data='I love.', date_time=dt.addDays(2))


chat2 = Tag(action=ACTION.CHAT, sender=selfUser.id, recipient=user1.id, data='I love you  much', date_time=dt)
chat4 = Tag(action=ACTION.CHAT, sender=selfUser.id, recipient=user2.id, data='I very much love you', date_time=dt)

selfUser.add_user(user1)
selfUser.add_user(user2)

for a in [chat1, chat2, chat3, chat4, chat5]:
    selfUser.add_chat(a)

for a in range(5):
    a = str(a)
    selfUser.add_user(Other_User(id=user1.id+a, name=user1.name+a))






chm = selfUser.chats


# print(len(chm.unseen_chats))
# print(len(chm.unsent_chats))

USER = selfUser






