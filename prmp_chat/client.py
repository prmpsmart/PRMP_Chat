
from .core import *



class Client_Multi_Users(Multi_Users):

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)

        self.admins = {} 
        self.users = {}
        self.chats = {}
    
    def add_chat(self, tag):
        if tag.sender in self.admins or self.only_admin is False: self.chats[len(self.chats)] = tag

class Client_Group(Client_Multi_Users): ...

class Client_Channel(Client_Multi_Users): only_admin = True


# User

class Private_Chat:
    def __init__(self, user, recipient):
        self.user = user
        self.recipient = recipient
        self.chats = {}
        self.unread_chats = []
        self.last_time = None
    
    def add_chat(self, tag):
        self.chats[len(self.chats)] = tag
        self.last_time = datetime.datetime.now()
    
    def dispense(self):
        for chat in self.unread_chats: self.add_chat(chat)

class Chats_Manager:

    def __init__(self, user):
        self.user = user
        self.private_chats = {}
        
        self.unseen_chats = []
        self.unsent_chats = []
    
    def add_chat(self, tag):
        recipient = tag.recipient
        if recipient == self.user.id: recipient = tag.sender
        
        if self.user.status is STATUS.ONLINE:
            if recipient in self.user.users:
                if recipient in self.private_chats: self.private_chats[recipient].add_chat(tag)
                else:
                    private_chat = Private_Chat(self.user, recipient)
                    private_chat.add_chat(tag)
                    self.private_chats[recipient] = private_chat

            elif recipient in self.user.groups:
                group = self.user.groups[recipient]
                group.add_chat(tag)
            elif recipient in self.user.channels:
                channel = self.user.channels[recipient]
                channel.add_chat(tag)

        elif self.user.id == recipient: self.unseen_chats.append(tag)
        else: self.unsent_chats.append(tag)
    
    def dispense(self):
        if self.unseen_chats:
            for chat in self.unseen_chats:
                self.unseen_chats.remove(chat)
                self.add_chat(chat)

        if self.unsent_chats:
            for chat in self.unsent_chats:
                self.unsent_chats.remove(chat)
                self.add_chat(chat)

class Client_User(User):
    'User on the client side.'

    def __init__(self, **kwargs):
        User.__init__(self, **kwargs)
        self.chats = Chats_Manager(self)





class Client(socket.socket):
    'Client socket for connection with the server.'
    
    def __str__(self) -> str:
        return f'Client(ip={self.ip}, port={self.port})'

    def __init__(self, ip='localhost', port=7767, user=None, LOG=print):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)

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

        action = ACTION.SIGNUP
        tag = Tag(id=id, name=name, key=key, action=action)
        soc_resp = SEND(self, tag)
        if soc_resp in SOCKETS:
            self.LOG(soc_resp)
            return soc_resp
        
        response_tag = RECV(self)
        if response_tag in SOCKETS:
            self.LOG(response_tag)
            return response_tag

        response = response_tag.response

        self.LOG(f'{action} -> RESPONSE.{response}')

        if response is RESPONSE.SUCCESSFUL:
            self.user = Client_User(id=id, name=name, key=key)
            return self.login()

    def login(self):
        if not self.connected: self._connect()
        self.LOG('LOGGING IN.')
        
        action = ACTION.LOGIN
        tag = Tag(id=self.user.id, name=self.user.name, key=self.user.key, action=action)
        
        soc_resp = SEND(self, tag)
        if soc_resp in SOCKETS: return soc_resp
        
        response_tag = RECV(self)
        if response_tag in SOCKETS: return soc_resp

        if response_tag in SOCKETS: return

        response = response_tag.response

        self.LOG(f'{action} -> RESPONSE.{response}')

        if response is RESPONSE.SUCCESSFUL:
            # starts the session
            # THREAD(self.start_session)
            ...
            self.LOG('WAITING')
            # while 1: ...
        
        return response
    
    def logout(self):
        soc_resp = SEND(self, Tag(action=ACTION.LOGOUT))
        self.close()
        return soc_resp

    def start_session(self):
        while True:
            tag = RECV(self)
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
        return SEND(self, tag)

    def send_status(self, tag): return SEND(self, Tag(action=ACTION.STATUS))

    def recv_chat(self, tag): self.user.chats_manager.add(tag)

    def recv_status(self, tag):
        statuses = tag.status
        for id, status in statuses:
            user = self.user.users_manager[id]
            if status is STATUS.ONLINE: user.status = status
            else:
                user.status = STATUS.OFFLINE
                user.last_seen = DATE_TIME(status)




