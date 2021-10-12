# ----------------------------------------------------------
import json, threading, socket, os, time
from typing import List
from PySide6.QtCore import QDateTime
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File
# ----------------------------------------------------------
OFFLINE_FORMAT = 'OFFLINE | dd/MM/yy | HH:mm:ss'

# ----------------------------------------------------------
def THREAD(func, *args, **kwargs): threading.Thread(target=func, args=args, kwargs=kwargs).start()

def DATETIME(date_time=None, num=1):
    if date_time == None:
        date_time = QDateTime.currentDateTime()
        if num: return DATETIME(date_time)
        else: return date_time

    if isinstance(date_time, int) and date_time > 0: return QDateTime.fromMSecsSinceEpoch(date_time)

    else: return date_time.toMSecsSinceEpoch()

def TIME(dateTime: QDateTime) -> str: return dateTime.toString("HH:mm:ss")

def DATE(dateTime: QDateTime) -> str: return dateTime.toString("yyyy-MM-dd")

def EXISTS(manager, obj): return RESPONSE.EXIST if obj in manager else RESPONSE.EXTINCT# ----------------------------------------------------------


# ----------------------------------------------------------
class Mixin:
    @property
    def className(self): return self.__class__.__name__

    def __repr__(self) -> str: return f'<{self}>'
# ----------------------------------------------------------


# ----------------------------------------------------------
class CONSTANT(Mixin):

    def __init__(self, name: str, objects: list=[]):
        self._NAME = name.upper()
        self.OBJECTS = {}

        for obj in objects: self.add(obj)
    
    def add(self, obj):
        if isinstance(obj, str): obj = CONSTANT(obj)
        self.OBJECTS[obj._NAME] = obj
    
    def __len__(self): return len(self.OBJECTS)

    @property
    def list(self): return list(self.OBJECTS.values())
    
    def __str__(self): return self._NAME
    
    def __hash__(self): return hash(self._NAME)
    
    def __getitem__(self, name):
        if isinstance(name, (str, CONSTANT)):
            name = str(name).upper()
            f = self.__dict__.get(name)
            if f == None: f = self.OBJECTS.get(name)
            return f
        elif isinstance(name, (list, tuple)):
            litu = []
            for na in name: litu.append(self[na])
            return litu
        else: return self.list[name]

    __call__ = __getattr__ = __getitem__
    
    def __eq__(self, other): return str(other).upper() == self._NAME

    def __getstate__(self):
        return {'_NAME': self._NAME, 'OBJECTS': list(self.OBJECTS.keys())}
    
    def __setstate__(self, state):
        self._NAME = state['_NAME']
        self.OBJECTS = {}
        for k in state['OBJECTS']: self.OBJECTS[k] = CONSTANT(k)

SOCKET = CONSTANT('SOCKET', objects=['RESET', 'CLOSED', 'ALIVE'])
SOCKET.ERRORS = SOCKET['RESET', 'CLOSED']

CHAT = CONSTANT('CHAT', objects=['TEXT', 'AUDIO', 'IMAGE', 'VIDEO'])
STATUS = CONSTANT('STATUS', objects=['ONLINE', 'OFFLINE', 'LAST_SEEN'])

RESPONSE = CONSTANT('RESPONSE', objects=['SUCCESSFUL', 'FAILED', 'LOGIN_FAILED', 'SIMULTANEOUS_LOGIN', 'EXIST', 'EXTINCT', 'FALSE_KEY'])
ID = CONSTANT('ID', objects=['USER_ID', 'GROUP_ID', 'CHANNEL_ID', 'CHAT_ID'])
TYPE = CONSTANT('TYPE', objects=['ADMIN', 'CONTACT', 'GROUP', 'CHANNEL'])
ACTION = CONSTANT('ACTION', objects=['ADD', 'REMOVE', 'CREATE', 'DELETE', 'CHANGE', 'DATA', CHAT, 'START', 'END', STATUS, 'SIGNUP', 'LOGIN', 'LOGOUT', 'QUEUED'])
TAG = CONSTANT('TAG', objects=[ACTION, 'CHAT_COLOR', CHAT, RESPONSE, 'SENDER', 'RECIPIENT', 'SENDER_TYPE', ID, 'KEY', 'NAME', 'DATA', STATUS, 'DATE_TIME', 'LAST_SEEN', 'RESPONSE_TO', 'EXT', TYPE, 'TEXT'])

# ----------------------------------------------------------


# ----------------------------------------------------------
class Tag(Mixin, dict):
    DELIMITER = b'<TAG>'
    # upper() of kwargs is the default lookup

    def __init__(self, **kwargs) -> None:

        for a, b in kwargs.items():
            if isinstance(b, Base): kwargs[a] = b.id

        dict.__init__(self, **kwargs)

    def __str__(self): return f'{self.className}({self.kwargs})'
    
    @property
    def dict(self) -> dict:
        _dict = {}
        for k, v in self.items():
            k = str(k)
            if isinstance(v, CONSTANT): v = str(v)
            elif isinstance(v, QDateTime): v = DATETIME(v)
            elif isinstance(v, Tag): v = v.dict
            # elif isinstance(v, Base): v = v.id
            _dict[k] = v
        return _dict

    @property
    def encode(self):
        string = json.dumps(self.dict)
        encoded = string.encode() + self.DELIMITER
        return encoded
    
    @classmethod
    def decode(cls, data) -> dict:
        if (cls.DELIMITER) in data: data = data.replace(cls.DELIMITER, b'')

        _dict = json.loads(data)
        
        tag = cls()
        for k, v in _dict.items():
            if k in TAG.list:
                k = TAG[k]
                if v in k.list: v = k[v]
            if k == TAG.ID: v = v.lower()
            elif k == TAG.DATE_TIME: v = DATETIME(v)
            # elif isinstance(v, dict): v = Tag.decode(json.dumps(v).encode())
            tag[k] = v
        return tag

    @classmethod
    def decodes(cls, data) -> list:
        decodes = data.split(cls.DELIMITER)
        tags = []
        
        for tag in decodes:
            if tag: tags.append(cls.decode(tag))

        return tags
    
    @property
    def kwargs(self) -> str:
        _str = ''
        for k, v in self.items(): _str += f'{k}={v}, '
        _str = ''.join(_str[:-2])
        return _str

    def __getattr__(self, attr):
        d = self.get(attr)
        if d == None: d = self.get(attr.upper())
        if d == None: d = self.get(attr.lower())
        return d
    
    def __getitem__(self, attr):
        if isinstance(attr, tuple):
            tup = []
            for at in attr:
                t = self[str(at).upper()] or self[str(at).lower()]
                tup.append(t)
            return tup
        elif isinstance(attr, list):
            tup = {}
            for at in attr:
                t = self.get(str(at).upper()) or self.get(str(at).lower())
                tup[at] = t
            return tup
        elif isinstance(attr, str): return self.get(attr.upper())

    def __setattr__(self, attr, val): self[attr.upper()] = val

    def __getstate__(self): return self.__dict__
    def __setstate__(self, state): self.__dict__.update(state)

    def get_date_time(self):
        if isinstance(self.date_time, int): return DATETIME(self.date_time)
        return self.date_time

    def delete(self, attr):
        dict = self.dict
        if attr in dict: del dict[attr]
        elif attr.upper() in dict: del dict[attr.upper()]
        self.clear()
        self.update(dict)
# ----------------------------------------------------------


# ----------------------------------------------------------
class Base(Mixin):

    def __init__(self, id: str, name: str='', icon: str=None, date_time: QDateTime=None):
        self.id = id
        self.name = name
        self.icon = icon
        self.ext = ''
        self.date_time = date_time or QDateTime.currentDateTime()
    
    def __str__(self):
        add = ''
        if self.name: add = f', name={self.name}'
        return f'{self.className}(id={self.id}{add})'


class _User_Base(Base):
    
    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)
        self._status = ''
        self.change_status(STATUS.OFFLINE)
        self.last_seen = None
    
    @property
    def status(self): return str(self._status)

    @property
    def current_status(self):
        if self.status == STATUS.ONLINE: return self.status
        else: return DATETIME(self.last_seen)
    
    @property
    def int_last_seen(self) -> int: return DATETIME(self.last_seen)

    @property
    def str_last_seen(self) -> str:
        if self.last_seen: return self.last_seen.toString(OFFLINE_FORMAT)

    def change_status(self, status) -> None:
        if status == STATUS.ONLINE: self._status = status
        else:
            last_seen = None
            if status == STATUS.OFFLINE: self._status = status
            else:
                # status is int from the server
                self._status = STATUS.OFFLINE
                last_seen = status
            self.last_seen = DATETIME(last_seen, num=0)

class _Multi_Users(Base):
    only_admin = False

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)
        self.creator: _User = None
        self._admins = {}
        self._users = {}
        self.last_time: QDateTime = None
        self.chats = None
    
    def add_admin(self, admin_id: str):
        if admin_id in self._users: self._admins[admin_id] = self._users[admin_id]
    
    def add(self, user): self._users[user.id] = user

    @property
    def ids(self) -> list: return list(self._users.keys())

    @property
    def users(self) -> list: return list(self._users.values())

    @property
    def objects(self) -> list: return self.users

    @property
    def _objects(self) -> dict: return self._users.copy()
    
    @property
    def admin_ids(self) -> list: return list(self._admins.keys())

    @property
    def admins(self) -> list: return list(self._admins.values())

    def add_chat(self, chat) -> None: self.chats.append(chat)

class _User(_User_Base):

    def __init__(self, key: str='', **kwargs):
        _User_Base.__init__(self, **kwargs)
        self.change_status(STATUS.OFFLINE)

        self.key = key
        self.users = None
        self.groups = None
        self.channels = None
    
    def add_user(self, user: _User_Base) -> None:  self.users.add(user)

    def add_group(self, group: _Multi_Users) -> None: self.groups.add(group)
    
    def add_channel(self, channel: _Multi_Users) -> None: self.channels.add(channel)

class _Manager:
    
    def __init__(self, user: _User):
        self.user = user
        self._objects = {}
        self.get = self._objects.get

    def add(self, obj: _User_Base) -> None:
        if obj.id == self.user.id: return
        
        _obj = self.get(obj.id)
        if _obj == None: self._objects[obj.id] = obj

    def remove(self, id: str) -> None:
        obj: _User_Base = self.get(id)
        if obj != None: del self._objects[id]
    
    def add_chat(self, chat: Tag) -> None:
        obj = self.get(chat.recipient)
        if obj != None: obj.add_chat(chat)

    def __len__(self): return len(self._objects)
    
    @property
    def objects(self): return list(self._objects.values())

    @property
    def ids(self): return list(self._objects.keys())

    def __getitem__(self, name):
        if isinstance(name, str):
            f = self.__dict__.get(name)
            if f == None: f = self.__dict__['_objects'].get(name)
            return f
        # elif isinstance(name, (int, slice)): return self.list[name]
        elif isinstance(name, (list, tuple)):
            litu = []
            for na in name: litu.append(self[na])
            return litu
        
        else: return self.objects[:]

# ----------------------------------------------------------


# ----------------------------------------------------------
class Sock(Mixin):

    def __init__(self, socket: socket.socket=None):
        self.socket = socket or self
        self.state = SOCKET.CLOSED
        # self.shutdown = self.socket.shutdown
    
    @property
    def alive(self): return self.state == SOCKET.ALIVE

    def _connect(self, ip, port):
        try:
            self.socket.connect((ip, port))
            self.state = SOCKET.ALIVE
        except Exception as e:
            num = e.errno
            # error_message = socket.errorTab[num]
            if num == 10056:
                try:
                    self.socket.send(Tag.DELIMITER)
                    self.socket.state = SOCKET.ALIVE
                except: self.state = SOCKET.CLOSED
        return self.alive

    def _close(self) -> None:
        try:
            self.state = SOCKET.CLOSED
            self.socket.shutdown(0)
            self.socket.close()
        except Exception as e:
            ...
    
    def catch(self, func):
        try:
            result = func()
            self.state = SOCKET.ALIVE
            return result

        except ConnectionResetError:
            # An existing connection was forcibly closed by the remote client.
            # The terminal of the client socket was terminated.] or closed.
            self.state = SOCKET.RESET
            return SOCKET.RESET

        except OSError:
            # An operation was attempted on something that is not a socket.
            # The client socket call close()
            self.state = SOCKET.CLOSED
            return SOCKET.CLOSED
    
    def recv_tag(self, buffer: int=1048576, many=False) -> Tag:
        fn = Tag.decodes if many else Tag.decode
        def func():
            encoded = self.socket.recv(buffer)
            if not encoded: raise OSError
            tag = fn(encoded)
            return tag
        return self.catch(func)

    def recv_tags(self) -> List[Tag]: return self.recv_tag(many=True)

    def send_tag(self, tag: Tag) -> int: return self.catch(lambda: self.socket.send(tag.encode))

    def sendall_tag(self, tag: Tag) -> int:
        def func(): return self.socket.sendall(tag.encode)
        return self.catch(func)
# ----------------------------------------------------------