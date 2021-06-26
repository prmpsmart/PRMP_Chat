import enum, json, threading, socket, os
from PySide6.QtCore import QDateTime

class Base_All:
    def __repr__(self): return f'<{self}>'



# Enums 

class BASE_ENUM(enum.Enum):

    def __str__(self): return self.name

    def __eq__(self, other):
        if isinstance(other, str): return self.name == other.upper()
        else: return self is other

    def __neq__(self, other):
        if isinstance(other, str): return self.name != other.upper()
        else: return self is not other
    
    def __repr__(self): return f'<{self}>'

    def __hash__(self): return hash(self.name)

class TAG(BASE_ENUM):
    'Enum of Tags.'

    ACTION = 'ACTION'
    CHAT_COLOR = 'CHAT_COLOR'
    CHAT = 'CHAT'
    RESPONSE = 'RESPONSE'
    SENDER = 'SENDER'
    RECIPIENT = 'RECIPIENT'
    SENDER_TYPE = 'SENDER_TYPE'
    # RECIPIENT_TYPE = 'RECIPIENT_TYPE'
    ID = 'ID'
    KEY = 'KEY'
    NAME = 'NAME'
    DATA = 'DATA'
    STATUS = 'STATUS'
    DATE_TIME = 'DATE_TIME'
    LAST_SEEN = 'LAST_SEEN'
    RESPONSE_TO = 'RESPONSE_TO'

class ACTION(BASE_ENUM):
    'Enum of Actions.'

    ADD = 'ADD'
    REMOVE = 'REMOVE'
    CREATE = 'CREATE'
    DELETE = 'DELETE'
    CHANGE = 'CHANGE'
    
    DATA = 'DATA'

    CHAT = 'CHAT'
    START = 'START'
    END = 'END'
    STATUS = 'STATUS'

    SIGNUP = 'SIGNUP'
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'

class CHAT(BASE_ENUM):
    'Enum of Chats.'

    TEXT = 'TEXT'
    AUDIO = 'AUDIO'
    VIDEO = 'VIDEO'

class STATUS(BASE_ENUM):
    'Enum of Status.'

    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'
    LAST_SEEN = 'LAST_SEEN'

class RESPONSE(BASE_ENUM):
    'Enum of Responses.'

    SUCCESSFUL = 'SUCCESSFUL'
    FAILED = 'FAILED'
    LOGIN_FAILED = 'LOGIN_FAILED'
    SIMULTANEOUS_LOGIN = 'SIMULTANEOUS_LOGIN'
    EXIST = 'EXIST'
    EXTINCT = 'EXTINCT'
    FALSE_KEY = 'FALSE_KEY'

class ID(BASE_ENUM):
    'Enum of IDs.'

    USER_ID = 'USER_ID'
    GROUP_ID = 'GROUP_ID'
    CHANNEL_ID = 'CHANNEL_ID'
    CHAT_ID = 'CHAT_ID'

class TYPE(BASE_ENUM):
    'Enum of Types.'

    ADMIN = 'ADMIN'
    USER = 'USER'
    GROUP = 'GROUP'
    CHANNEL = 'CHANNEL'

class SOCKET(BASE_ENUM):
    'Enums of Socket responses'

    RESET = 'RESET'
    CLOSED = 'CLOSED'
    ALIVE = 'ALIVE'

class Tag(Base_All, dict):

    def __init__(self, **kwargs):
        if 'action' in kwargs:
            action = kwargs['action']
            kwargs['action'] = ACTION[action]
        if 'response' in kwargs:
            response = kwargs['response']
            kwargs['response'] = RESPONSE[response]
        if 'chat' in kwargs:
            chat = kwargs['chat']
            kwargs['chat'] = CHAT[chat]
        if 'type' in kwargs:
            type = kwargs['type']
            kwargs['type'] = TYPE[type]
        if 'alive' in kwargs:
            alive = kwargs['alive']
            kwargs['alive'] = SOCKET[alive]
        if 'date_time' in kwargs:
            date_time = kwargs['date_time']
            if isinstance(date_time, int): kwargs['date_time'] = DATE_TIME(date_time)

        dict.__init__(self, **kwargs)

    def __str__(self) -> str:
        return f'Tag({self.kwargs})'
    
    @property
    def dict(self) -> dict:
        return dict(**self)

    @property
    def encode(self) -> bytes:
        _dict = {}

        for k, v in self.items():
            if k == 'date_time': v = DATE_TIME(v)
            elif isinstance(v, BASE_ENUM): v = v.value
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

SOCKETS = (SOCKET.RESET, SOCKET.CLOSED)

class Sock(Base_All):

    def __init__(self, socket=None):
        self.socket = socket or self
        self.shutdown = self.socket.shutdown
    
    def _close(self):
        self.socket.shutdown(0)
        self.socket.close()
    
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

def DATE_TIME(date_time=None, _int=1):
    if date_time is None:
        date_time = QDateTime.currentDateTime()
        if _int: return DATE_TIME(date_time)
        else: return date_time

    if isinstance(date_time, int): return QDateTime.fromSecsSinceEpoch(date_time)

    else: return date_time.toSecsSinceEpoch()

def TIME(dateTime): return dateTime.toString("HH:mm:ss")
def DATE(dateTime): return dateTime.toString("yyyy-MM-dd")

# Bases


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

        self.key = key
        self.status = None
        self.last_seen = None
        
        self.users = {}
        self.groups = {}
        self.channels = {}
    
    def change_status(self, status):
        self.status = status
        if status == STATUS.OFFLINE: self.last_seen = DATE_TIME()
    
    def add_user(self, user):
        if user.id not in self.users: self.users[user.id] = user
    def add_group(self, group):
        if group.id not in self.groups: self.groups[group.id] = group
    def add_channel(self, channel):
        if channel.id not in self.channels: self.channels[channel.id] = channel

