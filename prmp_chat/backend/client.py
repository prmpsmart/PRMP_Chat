# ----------------------------------------------------------
from .core import *
from .core import _Manager, _User_Base, _Multi_Users, _User
# ----------------------------------------------------------


# ----------------------------------------------------------
class Manager(_Manager):
    OBJ = None
    
    def add(self, tag: Tag) -> None:
        obj = self.OBJ(self.user, tag)
        super().add(obj)

class Chats:
    def __init__(self, user):
        self.user = user
        self.chats = []
        self.unread_chats = 0
        self.last_time = QDateTime.currentDateTime()

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
# ----------------------------------------------------------


# ----------------------------------------------------------
class Contact(_User_Base, Chats):

    def __init__(self, user, tag):
        _User_Base.__init__(self, id=tag.id, name=tag.name, icon=tag.icon)
        Chats.__init__(self, user)

class Contacts_Manager(_Manager): OBJ = Contact
# ----------------------------------------------------------


# ----------------------------------------------------------
class Multi_Users(_Multi_Users, Chats):

    def __init__(self, user, tag):
        _Multi_Users.__init__(self, id=tag.id, name=tag.name, icon=tag.icon)
        Chats.__init__(self, user)

        self.creator = tag.creator
        self.admins = tag.admins
        self.users = tag.users

class Group(Multi_Users): ...

class Groups_Manager(Manager): OBJ = Group

class Channel(Multi_Users): only_admin = True

class Channels_Manager(Manager): OBJ = Channel
# ----------------------------------------------------------


# ----------------------------------------------------------

# User

class User(_User):

    def __init__(self, **kwargs):
        _User.__init__(self, **kwargs)
        
        self.users = Contacts_Manager(self)
        self.groups = Groups_Manager(self)
        self.channels = Channels_Manager(self)
    
    @property
    def contacts(self): return self.users
    
    def load_data(self, tag):
        self.name = tag.name

        data = dict(users=tag.users, groups=tag.groups, channels=tag.channels)
        for name, objs in data.items():
            manager = getattr(self, name)
            for id, _dict in objs.items():
                tag = Tag(id=id, **_dict)
                manager.add(tag)
    
    def add_chat(self, tag):
        recipient = tag.recipient
        type = tag.type
        if type == TYPE.USER: self.users.add_chat(tag)
        elif type == TYPE.GROUP: self.groups.add_chat(tag)
        elif type == TYPE.CHANNEL: self.channels.add_chat(tag)
# ----------------------------------------------------------


# ----------------------------------------------------------
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
            if not self.user: self.user = User(id=id, name=name, key=key)
        
        return response

    def login(self, id='', key='', user=None):
        if not self._connect(): return 

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
                self.user = User(id=id, key=key)
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
    
    def gone_offlne(self):
        if self.user: self.user.change_status(STATUS.OFFLINE)

    def start_session(self):
        self.LOG('Listening to Server.')
        while True:
            tag = self.recv_tag()
            if tag in SOCKET.ERRORS: return self.gone_offlne()

            self.parse(tag)
    
    def parse(self, tag):
        if tag.action == ACTION.STATUS: self.recv_status(tag)
        elif tag.action == ACTION.CHAT: self.recv_chat(tag)
        elif tag.response: self.recv_response(tag)
    
    # receivers
    def recv_response(self, tag):
        action = tag.action

        if action == ACTION.ADD: ...
        elif action == ACTION.REMOVE: ...
        elif action == ACTION.CREATE: ...
        elif action == ACTION.CHANGE: ...
        elif action == ACTION.DELETE: ...
        
        print(tag)
    
    def recv_add(self, tag): ...

    def recv_remove(self, tag): ...

    def recv_create(self, tag): ...

    def recv_change(self, tag): ...

    def recv_delete(self, tag): ...

    def recv_chat(self, tag): self.user.add_chat(tag)

    def recv_start(self, tag): ...

    def recv_end(self, tag): ...

    def recv_status(self, tag):
        for id, status in tag.statuses.items():
            user = self.user.users.get(id)
            if user == None: continue

            if status == STATUS.ONLINE: user.change_status(STATUS.ONLINE)
            else:
                user.change_status(STATUS.OFFLINE)
                user.last_seen = DATETIME(status)
    
    # senders
    def send_add(self, id, type):
        tag = Tag(action=ACTION.ADD, type=type, id=id)
        self.send_tag(tag)

    def send_remove(self, id, type):
        tag = Tag(action=ACTION.REMOVE, type=type, id=id)
        self.send_tag(tag)
        
    def send_create(self, id, type, name, icon):
        tag = Tag(action=ACTION.CREATE, type=type, id=id, name=name, icon=icon)
        self.send_tag(tag)
        
    def send_change(self, id, change, type, data):
        tag = Tag(action=ACTION.CHANGE, change=change, type=type, id=id, data=data)
        self.send_tag(tag)
        
    def send_delete(self, id, type):
        tag = Tag(action=ACTION.DELETE, type=type, id=id)
        self.send_tag(tag)
        
    def send_chat(self, recipient, data, chat=CHAT.TEXT, type=TYPE.USER):
        tag = Tag(recipient=recipient, data=data, chat=chat, type=type, sender=self.user.id, action=ACTION.CHAT)
        return self.send_tag(tag)

    def send_start(self, id, type): ...
        
    def send_end(self, id, type): ...

    def send_status(self): return self.send_tag(Tag(action=ACTION.STATUS))

# ----------------------------------------------------------



