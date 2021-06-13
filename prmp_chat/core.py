import enum, json, threading, datetime, socket

class Base_All:
    def __repr__(self): return f'<{self}>'


# Enums 

class BASE_ENUM(Base_All, enum.Enum):

    def __eq__(self, other):
        if isinstance(other, str): return self.name == other.upper()
        else: return self is other
    
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
    # CHAT = 'CHAT'

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
        if 'alive' in kwargs:
            alive = kwargs['alive']
            kwargs['alive'] = SOCKET[alive]

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
            if not isinstance(v, str): v = v.value
            _dict[k] = v

        string = json.dumps(_dict)
        encoded = string.encode()
        return encoded

    @classmethod
    def decode(self, data) -> dict:
        decoded = data.decode()
        _dict = json.loads(data) if data else {}
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

            if tag.alive is SOCKET.ALIVE:
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

def DATE_TIME(date_time=None, tup=1):
    if date_time is None:
        date_time = datetime.datetime.now()
        if tup: return DATE_TIME(date_time)
        else: return date_time

    if isinstance(date_time, (tuple, list)): return datetime.datetime(*date_time)

    else: return (date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)

# Bases


class Base(Base_All):

    @property
    def className(self): return self.__class__.__name__

    def __init__(self, id, name='', date_time=None):
        self.id = id
        self.name = name
        self.date_time = date_time
    
    def __str__(self):
        add = ''
        if self.name: add = f', name={self.name}'
        return f'{self.className}(id={self.id}%s)'%add

class Multi_Users(Base):
    only_admin = False

    def __init__(self, creator, **kwargs):
        Base.__init__(self, **kwargs)
        self.creator = creator
        self.admins = {}
        self.users = {}

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
        if status is STATUS.OFFLINE: self.last_seen = DATE_TIME()



