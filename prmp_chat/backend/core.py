# ----------------------------------------------------------
import json, threading, socket, os
from PySide6.QtCore import QDateTime
# ----------------------------------------------------------


# ----------------------------------------------------------
class Mixin:
    @property
    def className(self): return self.__class__.__name__

    def __repr__(self) -> str: return f'<{self}>'
# ----------------------------------------------------------


# ----------------------------------------------------------
class CONSTANT(Mixin):

    def __init__(self, name: str, objects: list=[]):
        self.NAME = name.upper()
        self.OBJECTS = {}

        for obj in objects:
            if isinstance(obj, str): obj = CONSTANT(obj)
            self.OBJECTS[obj.NAME] = obj
    
    def __len__(self): return len(self.OBJECTS)

    @property
    def list(self): return list(self.OBJECTS.values())
    
    def __str__(self): return self.NAME
    
    def __hash__(self): return hash(self.NAME)
    
    def __getitem__(self, name):
        if isinstance(name, str):
            name = name.upper()
            f = self.__dict__.get(name)
            if f == None: f = self.__dict__['OBJECTS'].get(name)
            return f
        elif isinstance(name, (list, tuple)):
            litu = []
            for na in name: litu.append(self[na])
            return litu
        else: return self.list[name]

    __call__ = __getattr__ = __getitem__

    def __eq__(self, other): return str(other).upper() == self.NAME

CHAT = CONSTANT('CHAT', ['TEXT', 'AUDIO', 'VIDEO'])
STATUS = CONSTANT('STATUS', ['ONLINE', 'OFFLINE', 'LAST_SEEN'])
SOCKET = CONSTANT('SOCKET', ['RESET', 'CLOSED', 'ALIVE'])
SOCKET.ERRORS = SOCKET['reset', 'closed']
RESPONSE = CONSTANT('RESPONSE', ['SUCCESSFUL', 'FAILED', 'LOGIN_FAILED', 'SIMULTANEOUS_LOGIN', 'EXIST', 'EXTINCT', 'FALSE_KEY'])
ID = CONSTANT('ID', ['USER_ID', 'GROUP_ID', 'CHANNEL_ID', 'CHAT_ID'])
TYPE = CONSTANT('TYPE', ['ADMIN', 'USER', 'GROUP', 'CHANNEL'])
ACTION = CONSTANT('ACTION', ['ADD', 'REMOVE', 'CREATE', 'DELETE', 'CHANGE', 'DATA', CHAT, 'START', 'END', STATUS, 'SIGNUP', 'LOGIN', 'LOGOUT'])
TAG = CONSTANT('TAG', [ACTION, 'CHAT_COLOR', CHAT, RESPONSE, 'SENDER', 'RECIPIENT', 'SENDER_TYPE', ID, 'KEY', 'NAME', 'DATA', STATUS, 'DATE_TIME', 'LAST_SEEN', 'RESPONSE_TO'])
# ----------------------------------------------------------


# ----------------------------------------------------------
class Tag(Mixin, dict):

    def __init__(self, **kwargs) -> None:
        if 'id' in kwargs:
            id = kwargs['id']
            kwargs['id'] = id.lower()
        if 'ID' in kwargs:
            ID = kwargs['ID']
            kwargs['ID'] = ID.lower()
        if 'date_time' in kwargs:
            date_time = kwargs['date_time']
            if isinstance(date_time, int): kwargs['date_time'] = DATETIME(date_time)
        if 'DATE_TIME' in kwargs:
            date_time = kwargs['DATE_TIME']
            if isinstance(date_time, int): kwargs['DATE_TIME'] = DATETIME(date_time)

        dict.__init__(self, **kwargs)

    def __str__(self): return f'Tag({self.kwargs})'
    
    @property
    def dict(self) -> dict: return dict(**self)

    @property
    def encode(self) -> bytes:
        _dict = {}

        for k, v in self.items():
            if k in [TAG.DATE_TIME, STATUS, STATUS.LAST_SEEN]: v = DATETIME(v)
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

    def __setattr__(self, attr, val): self[attr] = val
# ----------------------------------------------------------


# ----------------------------------------------------------
def EXISTS(manager, obj) -> RESPONSE: return RESPONSE.EXIST if obj in manager else RESPONSE.EXTINCT

def THREAD(func, *args, **kwargs): threading.Thread(target=func, args=args, kwargs=kwargs).start()

def DATETIME(date_time=None, _int=1):
    if date_time == None:
        date_time = QDateTime.currentDateTime()
        if _int: return DATETIME(date_time)
        else: return date_time

    if isinstance(date_time, int): return QDateTime.fromSecsSinceEpoch(date_time)

    else: return date_time.toSecsSinceEpoch()

def TIME(dateTime: QDateTime) -> str: return dateTime.toString("HH:mm:ss")

def DATE(dateTime: QDateTime) -> str: return dateTime.toString("yyyy-MM-dd")
# ----------------------------------------------------------


# ----------------------------------------------------------
class Base(Mixin):

    def __init__(self, id: str, name: str='', icon: str=None, date_time: QDateTime=None):
        self.id = id
        self.icon = icon
        self.name = name
        self.date_time = date_time or QDateTime.currentDateTime()
    
    def __str__(self):
        add = ''
        if self.name: add = f', name={self.name}'
        return f'{self.className}(id={self.id}%s)'%add

class _User_Base(Base):
    
    def __init__(self, key: str='', **kwargs):
        Base.__init__(self, **kwargs)
        self.change_status(STATUS.OFFLINE)
        self.last_seen = None

class _Multi_Users(Base):
    only_admin = False

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)
        self.creator: _User = None
        self.admins = {}
        self.users = {}
        self.last_time: QDateTime = None
    
    def add_chat(self, chat) -> None: self.chats.append(chat)

class _User(_User_Base):

    def __init__(self, key='', **kwargs):
        Base.__init__(self, **kwargs)
        self.change_status(STATUS.OFFLINE)

        self.key = key
        self.users = None
        self.groups = None
        self.channels = None
    
    def change_status(self, status: STATUS) -> None:
        self.status = str(status)
        if status == STATUS.OFFLINE: self.last_seen = DATETIME()

    def add_user(self, user: _User_Base) -> None:  self.users.add(user)

    def add_group(self, group: _Multi_Users) -> None: self.groups.add(group)
    
    def add_channel(self, channel: _Multi_Users) -> None: self.channels.add(channel)

class _Manager:
    
    def __init__(self, user: _User):
        self.user = user
        self.objects = {}
        self.get = self.objects.get

    def add(self, obj: Base) -> None:
        _obj = self.objects.get(obj.id)
        if _obj == None: self.objects[obj.id] = obj

    def remove(self, id: str) -> None:
        obj: Base = self.objects.get(id)
        if obj != None: del self.objects[id]

    def add_chat(self, chat: Tag) -> None:
        id: str = chat.recipient
        obj = self.objects.get(id)
        if obj != None: obj.add_chat(chat)
    
    def __len__(self): return len(self.objects)
    
    @property
    def list(self): return list(self.objects.values())

    def __getitem__(self, name):
        if isinstance(name, str):
            f = self.__dict__.get(name)
            if f == None: f = self.__dict__['objects'].get(name)
            return f
        elif isinstance(name, (int, slice)): return self.list[name]
        elif isinstance(name, (list, tuple)):
            litu = []
            for na in name: litu.append(self[na])
            return litu

# ----------------------------------------------------------


# ----------------------------------------------------------
class Sock(Mixin):

    def __init__(self, socket: socket.socket=None):
        self.socket = socket or self
        self.shutdown = self.socket.shutdown
    
    def _close(self) -> None:
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

    def recv_tag(self, buffer=1024) -> Tag:
        def func():
            encoded = self.socket.recv(buffer)
            if not encoded: raise OSError
            
            tag = Tag.decode(encoded)

            if tag.alive == SOCKET.ALIVE:
                print('SERVER CHECK', tag, end='\r')
                return func(buffer)
            return tag
        return self.catch(func)

    def send_tag(self, tag): return self.catch(lambda: self.socket.send(tag.encode))

    def sendall_tag(self, tag):
        def func(): return self.socket.sendall(tag.encode)
        return self.catch(func)
# ----------------------------------------------------------