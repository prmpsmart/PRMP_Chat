# ----------------------------------------------------------
from .core import _Manager, _User_Base, _Multi_Users, _User
from .core import *
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File
# ----------------------------------------------------------

FILE_DIR = os.path.dirname(__file__)
FILE = os.path.join(FILE_DIR, 'CLIENT_DATA.pc')

def SAVE(user):
    _file = PRMP_File(FILE, perm='w')
    _file.saveObj(user)
    _file.save()

def LOAD():
    return
    _file = PRMP_File(FILE)
    user = _file.loadObj()
    return user

# ----------------------------------------------------------
class Manager(_Manager):
    OBJ = None
    
    def add(self, tag: Tag) -> None:
        if tag.id == self.user.id: return
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
    def last_chat(self):
        if self.chats: return self.chats[-1]
    
    def read(self): self.unread_chats = 0
# ----------------------------------------------------------


# ----------------------------------------------------------
class Contact(_User_Base, Chats):

    def __init__(self, user, tag):
        _User_Base.__init__(self, id=tag.id, name=tag.name, icon=tag.icon)
        Chats.__init__(self, user)

class Contacts_Manager(Manager):
    OBJ = Contact
    
    def add_chat(self, chat: Tag) -> None:
        id = chat.sender
        obj = self.get(id)
        if obj != None: obj.add_chat(chat)
# ----------------------------------------------------------


# ----------------------------------------------------------
class Multi_Users(_Multi_Users, Chats):

    def __init__(self, user, tag):
        _Multi_Users.__init__(self, id=tag.id, name=tag.name, icon=tag.icon)
        Chats.__init__(self, user)

        self.creator = tag.creator
        self._admins = tag.admins
        self._users = tag.users

class Group(Multi_Users):
    
    def __init__(self, user, tag):
        super().__init__(user, tag)
        self.only_admin = tag.only_admin

class Groups_Manager(Manager): OBJ = Group

class Channel(Multi_Users): only_admin = True

class Channels_Manager(Manager): OBJ = Channel
# ----------------------------------------------------------


# ----------------------------------------------------------
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
        self.icon = tag.icon

        data = dict(users=tag.users, groups=tag.groups, channels=tag.channels)
        for name, objs in data.items():
            manager = getattr(self, name)
            for id, _dict in objs.items():
                tag = Tag(id=id, **_dict)
                manager.add(tag)
    
    def add_chat(self, tag):
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

class Client:
    'Client socket for connection with the server.'
    
    def __str__(self) -> str:
        return f'Client(ip={self.ip}, port={self.port})'

    def __init__(self, ip='localhost', port=7767, user=None, relogin=0, LOG=print):
        
        self.create_socket()
        self._stop = False
        self.ip = ip
        self.port = port
        self.user = user
        
        self.relogin = relogin
        self.LOG = LOG
    
    def create_socket(self):
        self.socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_tag = self.socket.send_tag
        self.recv_tag = self.socket.recv_tag
        self.recv_tags = self.socket.recv_tags
        self.sendall_tag = self.socket.sendall_tag
        # self._stop = False
    
    def set_user(self, user): self.user = user

    @property
    def alive(self): return self.socket.alive

    def _connect(self):
        if self.alive: return True
        alive = self.socket._connect(self.ip, self.port)
        if not alive:
            self.create_socket()
            alive = self.socket._connect(self.ip, self.port)
        return alive

    def signup(self, id='', name='', key='', user=None, force=False):
        if not self._connect(): return
        self.LOG('Signup Started')

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
        if not self._connect(): return SOCKET.CLOSED
        # self.LOG('Login Started')
        if self.user and self.user.status == STATUS.ONLINE: return RESPONSE.SIMULTANEOUS_LOGIN

        self.user = user or self.user

        assert (id and key) or self.user, 'Provide [id, key] or user'
        
        id = id or self.user.id
        key = key or self.user.key

        action = ACTION.LOGIN
        tag = Tag(id=id, key=key, action=action)
        
        soc_resp = self.send_tag(tag)
        if soc_resp in SOCKET.ERRORS: return soc_resp
        
        response_tag = self.recv_tags()
        if response_tag in SOCKET.ERRORS: return response_tag

        response = response_tag[0].response

        self.LOG(f'{action} -> {response}')

        if response == RESPONSE.SUCCESSFUL:
            if not self.user: self.user = User(id=id, key=key)
            self.restore_data()
            self.user.change_status(STATUS.ONLINE)
        return response
    
    def logout(self):
        soc_resp = self.send_tag(Tag(action=ACTION.LOGOUT))
        if isinstance(soc_resp, int):
            self.stop()
            soc_resp = RESPONSE.SUCCESSFUL
        return soc_resp
    
    def stop(self):
        self._stop = True
        self.socket._close()
        self.gone_offline()
    
    def gone_offline(self):
        if self.user:
            self.user.change_status(STATUS.OFFLINE)
            self.LOG('GONE OFFLINE', self.user.str_last_seen)

    def start_session(self):
        self.LOG('Listening to Server.')
        self.send_status()
        while True:
        # while self.user.status == STATUS.ONLINE:
            if self._stop: return

            tags = self.recv_tags()
            if tags in SOCKET.ERRORS:
                self.gone_offline()
                res = ''
                if self.relogin:
                    self.LOG('RE-LOGIN in progress!')
                    res = self.re_login()
                
                if res not in  [RESPONSE.SUCCESSFUL, RESPONSE.SIMULTANEOUS_LOGIN]: return
            for tag in tags: self.parse(tag)
    
    def re_login(self):
        while self.user.status == STATUS.OFFLINE:
            if self._stop: return

            res = self.login()
            if res in [RESPONSE.SUCCESSFUL, RESPONSE.SIMULTANEOUS_LOGIN]: return res
            # elif res == SOCKET.CLOSED: self.create_socket()
            time.sleep(1)
    
    def parse(self, tag):
        action = tag.action
        if action == ACTION.STATUS: self.recv_status(tag)
        elif action == ACTION.CHAT: self.recv_chat(tag)
        elif action == ACTION.DATA: self.recv_data(tag)
        elif action == ACTION.ADD: self.recv_add(tag)
        elif action == ACTION.REMOVE: self.recv_remove(tag)
        elif action == ACTION.CREATE: self.recv_create(tag)
        elif action == ACTION.CHANGE: self.recv_change(tag)
        elif action == ACTION.DELETE: self.recv_delete(tag)
    
    def restore_data(self):
        if self.user: return self.send_data(self.user.id)

    # senders
    def send_data(self, id, type=TYPE.USER):
        tag = Tag(id=id, action=ACTION.DATA, type=type)
        return self.send_tag(tag)

    def send_add(self, id, type):
        tag = Tag(action=ACTION.ADD, type=type, id=id)
        return self.send_tag(tag)

    def send_remove(self, id, type):
        tag = Tag(action=ACTION.REMOVE, type=type, id=id)
        return self.send_tag(tag)
        
    def send_create(self, id, type, name, icon):
        tag = Tag(action=ACTION.CREATE, type=type, id=id, name=name, icon=icon)
        return self.send_tag(tag)
        
    def send_change(self, id, change, type, data):
        tag = Tag(action=ACTION.CHANGE, change=change, type=type, id=id, data=data)
        return self.send_tag(tag)
        
    def send_delete(self, id, type):
        tag = Tag(action=ACTION.DELETE, type=type, id=id)
        return self.send_tag(tag)
        
    def send_chat(self, recipient, data, chat=CHAT.TEXT, type=TYPE.USER):
        tag = Tag(recipient=recipient, data=data, chat=chat, type=type, sender=self.user.id, action=ACTION.CHAT)
        return self.send_tag(tag)

    def send_start(self, id, type): ...
        
    def send_end(self, id, type): ...

    def send_status(self): return self.send_tag(Tag(action=ACTION.STATUS))

    # receivers
    def recv_data(self, tag):
        # print(tag)
        if tag.response == RESPONSE.SUCCESSFUL:
            if tag.id == self.user.id: self.user.load_data(tag)

    def recv_add(self, tag): ...

    def recv_remove(self, tag): ...

    def recv_create(self, tag): ...

    def recv_change(self, tag): ...

    def recv_delete(self, tag): ...

    def recv_chat(self, tag):
        print(tag)
        self.user.add_chat(tag)

    def recv_start(self, tag): ...

    def recv_end(self, tag): ...

    def recv_status(self, tag):
        print(tag)
        if tag.id:
            obj = self.user.users.get(tag.id)
            if obj: obj.change_status(tag.status)
        elif tag.statuses:
            for id, status in tag.statuses:
                user = self.user.users.get(id)
                if user == None: continue
                user.change_status(status)
# ----------------------------------------------------------

