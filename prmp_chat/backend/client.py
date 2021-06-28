
from .core import *

class Chats_Base:
    def __init__(self, user, recipient):
        self.user = user
        self.recipient = recipient
        self.last_time = QDateTime.currentDateTime()
        self.unread_chats = 0

    def add_chat(self, tag):
        self.last_time = tag.date_time

        if tag.sender != self.user.id: self.unread_chats += 1
        else:
            if self.user.status != STATUS.ONLINE: tag.sent = False
        self.chats.append(tag)
    
    @property
    def lastChat(self):
        if self.chats: return self.chats[-1]
    
    def read(self): self.unread_chats = 0
    
class Client_Multi_Users(Chats_Base, Multi_Users):

    def __init__(self, user, id, tag):
        tag = Tag(**tag)
        Multi_Users.__init__(self, id=id, name=tag.name, icon=tag.icon)
        Chats_Base.__init__(self, user, self.id)

        self.creator = tag.creator
        self.admins = tag.admins
        self.users = tag.users

    def add_chat(self, tag):
        if tag.sender in self.admins or self.only_admin == False: self.chats.append(tag)
        self.last_time = tag.date_time
    


class Client_Group(Client_Multi_Users):
    type = 'group'


class Client_Channel(Client_Multi_Users):
    only_admin = True
    type = 'channel'


# User

class Private_Chat(Chats_Base, Base_All):
    type = 'private'

    def __init__(self, user, recipient):
        Chats_Base.__init__(self, user, recipient)
        self.chats = []
    
    @property
    def id(self): return self.recipient.id

    @property
    def icon(self): return self.recipient.icon

    @property
    def name(self): return self.recipient.name

    def __str__(self): return f'Private_Chat({self.recipient})'


class Chats_Manager(Base_All):

    def __init__(self, user):
        self.user = user
        self.private_chats = {}
        
        self.groups = self.user.groups
        self.channels = self.user.channels
    
    def add_private_chat(self, user):
        private_chat = Private_Chat(self.user, user)
        self.private_chats[user.id] = private_chat
    
    def add_chat(self, tag):
        recipient = tag.recipient
        # print(tag.type)
        
        id = tag.sender if recipient == self.user.id else tag.recipient

        if id in self.user.users: self.private_chats[id].add_chat(tag)

        elif id in self.groups:
            group = self.groups[id]
            group.add_chat(tag)
        elif id in self.channels:
            channel = self.channels[id]
            channel.add_chat(tag)

    def dispense(self):
        if self.unseen_chats:
            for chat in self.unseen_chats:
                self.unseen_chats.remove(chat)
                self.add_chat(chat)

        if self.unsent_chats:
            for chat in self.unsent_chats:
                self.unsent_chats.remove(chat)
                self.add_chat(chat)


class Other_User(User):
    this = False


class Client_User(User):
    'User on the client side.'
    this = True

    def __init__(self, **kwargs):
        User.__init__(self, **kwargs)
        self.chats = Chats_Manager(self)

        self.add_chat = self.chats.add_chat
    
    def add_user(self, user):
        super().add_user(user)
        self.chats.add_private_chat(user)
    
    def load_data(self, tag):
        users = tag.users
        groups = tag.groups
        channels = tag.channels
        self.name = tag.name

        for id, tag in users.items():
            user = Other_User(id=id, name=tag.get('name'), icon=tag.get('icon'))
            self.add_user(user)

        for id, tag in groups.items():
            group = Client_Group(self, id, tag)
            self.add_group(group)

        for id, tag in channels.items():
            channel = Client_Channel(self, id, tag)
            self.add_channel(channel)

class Socket(socket.socket, Sock):
    def __init__(self, *args, **kwargs):
        socket.socket.__init__(self, *args, **kwargs)
        Sock.__init__(self)

class Client(Socket):
    'Client socket for connection with the server.'
    
    def __str__(self) -> str:
        return f'Client(ip={self.ip}, port={self.port})'

    def __init__(self, ip='localhost', port=7767, user=None, LOG=print):
        Socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)

        self.ip = ip
        self.port = port
        self.user = user
        self.LOG = LOG
        self.connected = False
    
    def set_user(self, user): self.user = user

    def _connect(self):
        self.connected = False
        try:
            self.connect((self.ip, self.port))
            self.connected = True
        except Exception as e:
            num = e.errno
            error_message = socket.errorTab[num]
            if num == 10056: self.connected = True
        return self.connected

    def signup(self, id='', name='', key='', user=None, force=False):
        if not self._connect(): return
        self.LOG('SIGNING UP')

        self.user = user or self.user

        assert (id and name and key) or self.user, 'Provide [id, name, key] or user'

        id = id or self.user.id
        name = name or self.user.name
        key = key or self.user.key

        action = ACTION.SIGNUP
        tag = Tag(id=id, name=name, key=key, action=action)
        soc_resp = self.send_tag(tag)
        if soc_resp in SOCKET.ERRORS:
            self.LOG(soc_resp)
            return soc_resp

        response_tag = self.recv_tag()
        if response_tag in SOCKET.ERRORS:
            self.LOG(response_tag)
            return response_tag

        response = response_tag.response

        self.LOG(f'{action} -> {response}')

        if response == RESPONSE.SUCCESSFUL:
            if not self.user: self.user = Client_User(id=id, name=name, key=key)
        
        return response

    def login(self, id='', key='', user=None):
        if not self._connect(): return 

        self.LOG('LOGGING IN.')
        
        self.user = user or self.user

        assert (id and key) or self.user, 'Provide [id, key] or user'
        
        id = id or self.user.id
        key = key or self.user.key

        action = ACTION.LOGIN
        tag = Tag(id=id, key=key, action=action)
        
        soc_resp = self.send_tag(tag)
        if soc_resp in SOCKET.ERRORS: return soc_resp
        
        response_tag = self.recv_tag()
        if response_tag in SOCKET.ERRORS: return response_tag

        response = response_tag.response

        self.LOG(f'{action} -> {response}')

        if response == RESPONSE.SUCCESSFUL:
            if not self.user:
                self.user = Client_User(id=id, key=key)
                tag = Tag(id=id, key=key, action=ACTION.DATA)
                
                soc_resp = self.send_tag(tag)
                if soc_resp in SOCKET.ERRORS: return soc_resp
            
                response_tag = self.recv_tag()
                if response_tag in SOCKET.ERRORS: return response_tag

                self.user.load_data(response_tag)
            self.user.change_status(STATUS.ONLINE)
        
        return response
    
    def logout(self):
        if not self._connect(): return self.gone_offlne()

        soc_resp = self.send_tag(Tag(action=ACTION.LOGOUT))
        self.gone_offlne()
        self._close()
        return soc_resp
    
    def gone_offlne(self): self.user.change_status(STATUS.OFFLINE)

    def start_session(self):
        while True:
            tag = self.recv_tag()
            if tag in SOCKET.ERRORS: return self.gone_offlne()

            if len(tag) == 1 and 'response' in tag:
                # it's a response to a post
                ...
            else:
                self.parse(tag)
    
    def parse(self, tag):
        if tag.action == ACTION.STATUS: self.recv_status(tag)
        elif tag.action == ACTION.CHAT: self.recv_chat(tag)
    
    def send_chat(self, recipient, data, chat=CHAT.TEXT, type=TYPE.USER):
        tag = Tag(recipient=recipient, data=data, chat=chat, type=type, sender=self.user.id, action=ACTION.CHAT)
        return self.send_tag(tag)

    def send_status(self, tag): return self.send_tag(Tag(action=ACTION.STATUS))

    def recv_chat(self, tag): self.user.add_chat(tag)

    def recv_status(self, tag):
        statuses = tag.status
        for id, status in statuses:
            user = self.user.users[id]
            if status == STATUS.ONLINE: user.status = status
            else:
                user.status = STATUS.OFFLINE
                user.last_seen = DATETIME(status)




