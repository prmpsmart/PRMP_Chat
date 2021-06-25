
from .core import *



class Client_Multi_Users(Multi_Users):

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)

        self.admins = {} 
        self.users = {}
        self.chats = {}
    
    def add_chat(self, tag):
        if tag.sender in self.admins or self.only_admin is False: self.chats[len(self.chats)] = tag

class Client_Group(Client_Multi_Users): type = 'group'

class Client_Channel(Client_Multi_Users):
    only_admin = True
    type = 'channel'


# User



class Private_Chat(Base_All):
    type = 'private'

    def __init__(self, user, recipient):
        self.user = user
        self.recipient = recipient
        self.chats = []
        self.unread_chats = 0
        self.last_time = QDateTime.currentDateTime()
    
    @property
    def id(self): return self.recipient.id

    @property
    def icon(self): return self.recipient.icon

    @property
    def name(self): return self.recipient.name

    @property
    def lastChat(self):
        if self.chats: return self.chats[-1]
    
    def add_chat(self, tag):
        self.last_time = QDateTime.currentDateTime()

        if tag.sender == self.recipient.id: self.unread_chats += 1
        else:
            if self.user.status is not STATUS.ONLINE: tag.sent = False
        self.chats.append(tag)
    
    def read(self): self.unread_chats = 0
    
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
        self.connect((self.ip, self.port))
        self.connected = True

    def signup(self, id, name, key, force=False):
        if not self.connected: self._connect()
        self.LOG('SIGNING UP')

        action = ACTION.SIGNUP
        tag = Tag(id=id, name=name, key=key, action=action)
        soc_resp = self.send_tag(tag)
        if soc_resp in SOCKETS:
            self.LOG(soc_resp)
            return soc_resp

        response_tag = self.recv_tag()
        if response_tag in SOCKETS:
            self.LOG(response_tag)
            return response_tag

        response = response_tag.response

        self.LOG(f'{action} -> {response}')

        if response is RESPONSE.SUCCESSFUL:
            self.user = Client_User(id=id, name=name, key=key)


    def login(self, id, key):
        if not self.connected: self._connect()
        self.LOG('LOGGING IN.')
        
        action = ACTION.LOGIN
        tag = Tag(id=id, key=key, action=action)
        
        soc_resp = self.send_tag(tag)
        print('send')
        if soc_resp in SOCKETS: return soc_resp
        
        response_tag = self.recv_tag()
        print('recv')
        if response_tag in SOCKETS: return soc_resp

        response = response_tag.response

        self.LOG(f'{action} -> {response}')
        
        return response
    
    def logout(self):
        soc_resp = self.send_tag(Tag(action=ACTION.LOGOUT))
        self._close()
        return soc_resp

    def start_session(self):
        while True:
            tag = self.recv_tag()
            if tag in SOCKETS: return

            if len(tag) == 1 and 'response' in tag:
                # it's a response to a post
                ...
            else:
                self.parse(tag)
    
    def parse(self, tag):
        if tag.action is ACTION.STATUS: self.recv_status(tag)

        elif tag.action is ACTION.CHAT: self.recv_chat(tag)
    
    def send_chat(self, recipient, data, chat, type):
        tag = Tag(recipient=recipient, data=data, chat=chat, type=type)
        return self.send_tag(tag)

    def send_status(self, tag): return self.send_tag(Tag(action=ACTION.STATUS))

    def recv_chat(self, tag): self.user.chats_manager.add(tag)

    def recv_status(self, tag):
        statuses = tag.status
        for id, status in statuses:
            user = self.user.users_manager[id]
            if status is STATUS.ONLINE: user.status = status
            else:
                user.status = STATUS.OFFLINE
                user.last_seen = DATE_TIME(status)




