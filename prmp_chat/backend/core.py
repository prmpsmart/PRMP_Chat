import json, threading, socket, os
from PySide6.QtCore import QDateTime

class Base_All:
    def __repr__(self): return f'<{self}>'


# constants

class CONSTANT:

    def __init__(self, name, children=[]):
        self.NAME = name.upper()
        self.CHILDREN = {}

        for child in children:
            if isinstance(child, str): child = CONSTANT(child)
            self.CHILDREN[child.name] = child
    
    def __len__(self): return len(self.children)

    @property
    def list(self): return list(self.children.values())
    
    def __str__(self): return self.name
    def __hash__(self): return hash(self.name)
    def __getitem__(self, name):
        if isinstance(name, str):
            name = name.upper()
            f = self.__dict__.get(name)
            if f == None: f = self.__dict__['CHILDREN'].get(name)
            return f
        elif isinstance(name, (int, slice)): return self.list[name]
        elif isinstance(name, (list, tuple)):
            litu = []
            for na in name: litu.append(self[na])
            return litu

    __call__ = __getattr__ = __getitem__

    def __eq__(self, other): return str(other).upper() == self.name


CHAT = CONSTANT('CHAT', ['TEXT', 'AUDIO', 'VIDEO'])
STATUS = CONSTANT('STATUS', ['ONLINE', 'OFFLINE', 'LAST_SEEN'])
SOCKET = CONSTANT('SOCKET', ['RESET', 'CLOSED', 'ALIVE'])
SOCKET.ERRORS = SOCKET['reset', 'closed']
RESPONSE = CONSTANT('RESPONSE', ['SUCCESSFUL', 'FAILED', 'LOGIN_FAILED', 'SIMULTANEOUS_LOGIN', 'EXIST', 'EXTINCT', 'FALSE_KEY'])
ID = CONSTANT('ID', ['USER_ID', 'GROUP_ID', 'CHANNEL_ID', 'CHAT_ID'])
TYPE = CONSTANT('TYPE', ['ADMIN', 'USER', 'GROUP', 'CHANNEL'])
ACTION = CONSTANT('ACTION', ['ADD', 'REMOVE', 'CREATE', 'DELETE', 'CHANGE', 'DATA', CHAT, 'START', 'END', STATUS, 'SIGNUP', 'LOGIN', 'LOGOUT'])
TAG = CONSTANT('TAG', [ACTION, 'CHAT_COLOR', CHAT, RESPONSE, 'SENDER', 'RECIPIENT', 'SENDER_TYPE', ID, 'KEY', 'NAME', 'DATA', STATUS, 'DATE_TIME', 'LAST_SEEN', 'RESPONSE_TO'])


class Tag(Base_All, dict):

    def __init__(self, **kwargs):
        if 'DATE_TIME' in kwargs:
            date_time = kwargs['DATE_TIME']
            if isinstance(date_time, int): kwargs['DATE_TIME'] = DATETIME(date_time)

        dict.__init__(self, **kwargs)

    def __str__(self) -> str:
        return f'Tag({self.kwargs})'
    
    @property
    def dict(self): return dict(**self)

    @property
    def encode(self) -> bytes:
        _dict = {}

        for k, v in self.items():
            if k == TAG.DATE_TIME: v = DATETIME(v)
            elif isinstance(v, CONSTANT): v = v.name
            _dict[k] = v

        string = json.dumps(_dict)
        encoded = string.encode()
        return encoded

    @classmethod
    def decode(self, data) -> dict:
        decoded = data.decode()
        _dict = json.loads(decoded) if data else {}
        return Tag(**_dict)
    
    @property
    def kwargs(self) -> str:
        _str = ''
        for k, v in self.items(): _str += f'{k}="{v}", '
        _str = ''.join(_str[:-2])
        return _str

    def __getattr__(self, attr): return self.get(attr.upper()) or self.get(attr.lower())
    
    def __getitem__(self, attr):
        if isinstance(attr, tuple):
            tup = []
            for at in attr:
                t = self.get(str(at).upper()) or self.get(str(at).lower())
                tup.append(t)
            return tup
        elif isinstance(attr, list):
            tup = {}
            for at in attr:
                t = self.get(str(at).upper()) or self.get(str(at).lower())
                tup[at.upper()] = t
            return tup
        elif isinstance(attr, str): return self.get(attr.upper())

# socket's send and recv


class Sock(Base_All):

    def __init__(self, socket=None):
        self.socket = socket or self
        self.shutdown = self.socket.shutdown
    
    def _close(self):
        try:
            self.socket.shutdown(0)
            self.socket.close()
        except Exception as e:
            ...
    
    def catch(self, func):
        try: return func()

        except ConnectionResetError:
            # An existing connection was forcibly closed by the remote client.
            # The terminal of the client socket was terminated.] or closed.
            return SOCKET.RESET

        except OSError:
            # An operation was attempted on something that is not a socket.
            # The client socket call close()
            return SOCKET.CLOSED

    def recv_tag(self, buffer=1024):
        def func():
            encoded = self.socket.recv(buffer)
            if not encoded: raise OSError
            
            tag = Tag.decode(encoded)

            if tag.alive == SOCKET.ALIVE:
                print('SERVER CHECK', tag, end='\r')
                return func(buffer)
            return tag
        return self.catch(func)

    def send_tag(self, tag): return self.catch(lambda:self.socket.send(tag.encode))

    def sendall_tag(self, tag):
        def func(): return self.socket.sendall(tag.encode)
        return self.catch(func)


def EXISTS(manager, obj): return RESPONSE.EXIST if obj in manager else RESPONSE.EXTINCT


def THREAD(func, *args, **kwargs): threading.Thread(target=func, args=args, kwargs=kwargs).start()

def DATETIME(date_time=None, _int=1):
    if date_time == None:
        date_time = QDateTime.currentDateTime()
        if _int: return DATETIME(date_time)
        else: return date_time

    if isinstance(date_time, int): return QDateTime.fromSecsSinceEpoch(date_time)

    else: return date_time.toSecsSinceEpoch()

def TIME(dateTime): return dateTime.toString("HH:mm:ss")
def DATE(dateTime): return dateTime.toString("yyyy-MM-dd")

# Bases
# 

class Base(Base_All):

    @property
    def className(self): return self.__class__.__name__

    def __init__(self, id, name='', icon=None, date_time=None):
        self.id = id
        self.icon = icon
        self.name = name
        self.date_time = date_time or QDateTime.currentDateTime()
    
    def __str__(self):
        add = ''
        if self.name: add = f', name={self.name}'
        return f'{self.className}(id={self.id}%s)'%add

class Multi_Users(Base):
    only_admin = False

    def __init__(self, creator=None, **kwargs):
        Base.__init__(self, **kwargs)
        self.creator = creator
        self.admins = {creator.id: creator} if creator else {}
        self.users = {}
        self.chats = []
        self.last_time = ''
    
    def add_user(self, user):
        if user.id not in self.users: self.users[user.id] = user

    def add_admin(self, admin):
        if admin.id not in self.admins: self.admins[admin.id] = admin
    
    def add_chat(self, chat): self.chats.append(chat)

class User(Base):

    def __init__(self, key='', **kwargs):
        Base.__init__(self, **kwargs)
        self.change_status(STATUS.OFFLINE)

        self.key = key
        self.last_seen = None
        
        self.users = {}
        self.groups = {}
        self.channels = {}
    
    def change_status(self, status):
        self.status = str(status)
        if status == STATUS.OFFLINE: self.last_seen = DATETIME()
    
    def add_user(self, user):
        if user.id not in self.users: self.users[user.id] = user
    def add_group(self, group):
        if group.id not in self.groups: self.groups[group.id] = group
    def add_channel(self, channel):
        if channel.id not in self.channels: self.channels[channel.id] = channel

