# ----------------------------------------------------------
from pickle import NONE
from .core import *
from .core import _Manager, _User, _Multi_Users
import time
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File
# ----------------------------------------------------------


# ----------------------------------------------------------
USERS_SESSIONS: dict = {}
# ----------------------------------------------------------


# ----------------------------------------------------------
class Manager(_Manager):
    
    def add(self, id: str) -> RESPONSE:
        if id in self.objects: return RESPONSE.EXIST

        response: RESPONSE = self.OBJ_M.exists(id)
        if response == RESPONSE.EXIST:
            obj = self.OBJ_M.get(id)
            super().add(obj)
            obj.add(self.user.id)
            response = RESPONSE.SUCCESSFUL
        return response

    def remove(self, id: str) -> RESPONSE:
        if id not in self: return RESPONSE.EXTINCT

        obj: Base = self.objects.get(id)
        if obj != None:
            obj.remove(self.user.id)
            super().remove(id)
            return RESPONSE.SUCCESSFUL

class User(_User):

    def __init__(self, **kwargs) -> None:
        _User.__init__(self, **kwargs)
        self.users = Users_Manager(self)
        self.groups = Groups_Manager(self)
        self.channels = Channels_Manager(self)
        self.queued_chats = []
        self.data_changed = False
    
    def dispense(self): self.queued_chats = []
    
    @property
    def data(self) -> Tag:
        users = {}
        groups = {}
        channels = {}

        for user in self.users.values(): users[user.id] = dict(name=user.name, icon=user.icon)
        for group in self.groups.values(): groups[group.id] = dict(name=group.name, icon=group.icon, creator=group.creator.id, admins=list(group.admins.keys()), users=list(group.users.keys()), only_admin=group.only_admin)
        for channel in self.channels.values(): channels[channel.id] = dict(name=channel.name, icon=channel.icon, creator=channel.creator.id, admins=list(channel.admins.keys()), users=list(channel.users.keys()))

        tag = Tag(name=self.name, users=users, groups=groups, channels=channels)

        return tag
    
    def create_group(self, **kwargs) -> RESPONSE: return self.groups.create(**kwargs)

    def create_channel(self, **kwargs) -> RESPONSE: return self.channels.create(**kwargs)
    
    def add(self, id: str) -> RESPONSE: return self.users.add(id)

    def add_group(self, id: str) -> RESPONSE: return self.groups.add(id)

    def add_channel(self, id: str) -> RESPONSE: return self.channels.add(id)
    
    def add_chat(self, tag: Tag) -> RESPONSE:
        if self.status == STATUS.ONLINE:
            session: Session = USERS_SESSIONS[self.id]
            session.client.send_tag(tag)
        else: self.queued_chats.append(tag)
# ----------------------------------------------------------


# ----------------------------------------------------------
class Managers(Mixin):
    OBJS = {}
    OBJ = None

    @classmethod
    def exists(cls, id: str) -> RESPONSE:
        id = id.lower()
        if id in cls.OBJS: return RESPONSE.EXIST
        else: return RESPONSE.EXTINCT

    @classmethod
    def get(cls, id: str): return cls.OBJS.get(id.lower())

    @classmethod
    def add(cls, id: str, obj: None): cls.OBJS[id.lower()] = obj

    @classmethod
    def create(cls, id: str, name: str, **kwargs) -> RESPONSE:
        id = id.lower()
        response = cls.exists(id)
        if response == RESPONSE.EXTINCT:
            # try:
                obj = cls.OBJ(id=id, name=name, **kwargs)
                cls.add(id, obj)
                return RESPONSE.SUCCESSFUL
            # except Exception as e:
                print(e)
                return RESPONSE.FAILED
        else: return response

    @classmethod
    def remove(cls, id) -> RESPONSE:
        id = id.lower()
        response = cls.exists(id)
        if response == RESPONSE.EXIST:
            try:
                del cls.OBJS[id]
                return RESPONSE.SUCCESSFUL
            except: return RESPONSE.FAILED
        else: return response
# ----------------------------------------------------------


# ----------------------------------------------------------
class Users(Managers):
    OBJS = {}
    OBJ = User

class Users_Manager(Manager): OBJ_M = Users
Users_Manager = Users_Manager
# ----------------------------------------------------------


# -------------MULTI_USERS----------------------------------
class Multi_Users(_Multi_Users):
    only_admin = False

    def __init__(self, creator: User, **kwargs: dict):
        _Multi_Users.__init__(self, **kwargs)
        
        self.creator = creator
        self.admins = {creator.id: creator}
    
    @property
    def objects(self): return dict(**self.admins, **self.users)

    def add(self, id: str):
        if id not in self.objects:
            user = Users.get(id)
            if user: self.users[id] = user

    def add_admin(self, id: str):
        user = self.users.pop(id)
        if (user != None) and (user.id not in self.admins): self.admins[user.id] = user

    def add_chat(self, chat: Tag):
        if chat.sender in self.admins or self.only_admin == False:
            dic: dict = self.objects
            del dic[chat.sender]

            for user in dic.values(): user.add_chat(chat)

    def remove_user(self, user: User, admin: User):
        if admin.id not in self.admin: return RESPONSE.FAILED

        id: str = user.id
        if id != self.creator.id:
            if id in self.admins: del self.admins[id]
            if id in self.users: del self.users[id]

class Multi_Users_Manager(Manager):
    OBJ_M = Managers
    

    def create(self, id: str, name: str, icon: str ='') -> RESPONSE:
        id = id.lower()
        response: RESPONSE = self.OBJ_M.create(id, name, icon=icon, creator=self.user)
        if response == RESPONSE.SUCCESSFUL:
            obj = self.OBJ_M.get(id)
            self.objects[id] = obj
        return response
# ----------------------------------------------------------


# ---------------GROUPS-------------------------------------
class Group(Multi_Users): ...

class Groups(Managers):
    OBJS = {}
    OBJ = Group

class Groups_Manager(Multi_Users_Manager): OBJ_M = Groups
# ----------------------------------------------------------


# --------------CHANNELS------------------------------------
class Channel(Multi_Users): only_admin = True

class Channels(Managers):
    OBJS = {}
    OBJ = Channel

class Channels_Manager(Multi_Users_Manager): OBJ_M = Channels
# ----------------------------------------------------------


# ----------------------------------------------------------
MANAGERS = {TYPE.USER: Users, TYPE.GROUP: Groups, TYPE.CHANNEL: Channels}
FILE_DIR = os.path.dirname(__file__)
FILE = os.path.join(FILE_DIR, 'SERVER_DATA.pc')
# ----------------------------------------------------------


# ----------------------------------------------------------
def SAVE():
    dic = dict(users=Users.OBJS, groups=Groups.OBJS, channels=Channels.OBJS)
    _file = PRMP_File(FILE, perm='w')
    _file.saveObj(dic)
    _file.save()

def LOAD():
    _file = PRMP_File(FILE)
    dic = _file.loadObj()
    if not dic: return

    Users.OBJS.update(dic['users'])
    Groups.OBJS.update(dic['groups'])
    Channels.OBJS.update(dic['channels'])
# ----------------------------------------------------------


# ----------------------------------------------------------
class Client_Socket(Sock):
    def __init__(self, sock_details: tuple):
        Sock.__init__(self, sock_details[0])

        address_port = sock_details[1]
        self.address = address_port[0]
        self.port = address_port[1]
        self.remote = self.socket.getpeername()
        
        self.user = None
    
    def __str__(self): return f'Client_Socket(address={self.address}, port={self.port})'

    def __eq__(self, other): return str(self) == str(other)

class Server(Mixin, socket.socket):
    'Server socket for creating server that waits for client connections.'

    def __str__(self): return f'Server(ip={self.ip or "localhost"}, port={self.port})'

    def __init__(self, ip: str='', port: int=7767, reuse_port: bool=True, max_client: int=3, LOG=print):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if reuse_port:
            try: self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except: ...

        self.ip = ip
        self.port = port
        self.LOG = LOG

        self.online_clients = {}
        self.max_client = max_client or 10
        self.response_server = Response_Server(self)

        # LOAD()
        # THREAD(self.saveDatas)

        self.bind((self.ip, self.port))
        self.listen(self.max_client)
    
    @property
    def sessions(self) -> int: return len(USERS_SESSIONS)

    def accept(self) -> Client_Socket: return  Client_Socket(socket.socket.accept(self))

    def set_online_clients(self) -> None:
        connections = self.online_clients.copy()

        for conn, _conn in connections.items():
            response = _conn.send_tag(Tag(alive=SOCKET.ALIVE))

            if str(response) != '18':
                _conn.user.change_status(STATUS.OFFLINE)
                del self.online_clients[conn]

        time.sleep(1)
        self.set_online_clients()
    
    def start(self) -> None:
        self.LOG('Accepting connections !')

        while True:
            client = self.accept()
            THREAD(self.response_server.add, client)
    
    def saveDatas(self) -> None:
        SAVE()

        time.sleep(5)
        self.saveDatas()

class Response_Server:

    def __init__(self, server: Server):
        self.server = server
        self.LOG = server.LOG

    def add(self, client: Client_Socket) -> None:
        # self.LOG(client, 'connected!')

        while True:
            user = None
            tag = client.recv_tag()
            
            if tag in SOCKET.ERRORS: return
            
            action = ACTION[tag.action]

            LOG = lambda val: self.LOG(f'\n{user} -> {action} -> {val}')

            if action == ACTION.SIGNUP:

                response = Users.create(*tag['id', 'name'], key=tag.key)
                
                LOG(response)
                soc_resp = client.send_tag(Tag(response=response))
                if soc_resp in SOCKET.ERRORS: return
                
                if response == RESPONSE.SUCCESSFUL: user = Users.OBJS[tag.id]

            elif action == ACTION.LOGIN:
                response = Users.exists(tag.id)

                if response == RESPONSE.EXIST:
                    user = Users.OBJS[tag.id]

                    if user.id in USERS_SESSIONS or user.status == STATUS.ONLINE: response = RESPONSE.SIMULTANEOUS_LOGIN

                    elif user.key == tag.key:
                        response = RESPONSE.SUCCESSFUL
                        client.user = user

                    else: response = RESPONSE.FALSE_KEY
                
                # LOG(response)
                soc_resp = client.send_tag(Tag(response=response))
                if soc_resp in SOCKET.ERRORS: return soc_resp

                if response == RESPONSE.SUCCESSFUL:
                    session = Session(self, client)
                    USERS_SESSIONS[user.id] = session
                    session.start_session()
                    break

    def remove(self, session) -> None:
        session: Session = session
        id = session.user.id
        if id in USERS_SESSIONS: del USERS_SESSIONS[id]

class Session:

    def __str__(self): return f'Session(client={self.client}, user={self.user})'

    def __init__(self, response_server: Response_Server, client: Client_Socket):
        self.client = client
        self.response_server = response_server
        self.user = client.user

        self.parser = Session_Parser(self)
        self.LOG = self.response_server.server.LOG

    def start_session(self) -> None:
        self.user.change_status(STATUS.ONLINE)
        self.LOG(f'Listening to {self.user}\n')

        while True:
            if self.user.queued_chats:
                for chat in self.user.queued_chats:
                    res = self.client.send_tag(chat)
                    
                    if res in SOCKET.ERRORS:
                        # means that client == offline
                        self.stop_session()
                        break
                    time.sleep(.1)
                self.user.dispense()

            tag = self.client.recv_tag()

            if tag in SOCKET.ERRORS:
                self.stop_session()
                break

            tag = self.parser.parse(tag)
            if tag:
                soc_resp = self.client.send_tag(tag)
                if soc_resp in SOCKET.ERRORS:
                    self.stop_session()
                    break

    def stop_session(self) -> None:
        self.user.change_status(STATUS.OFFLINE)

        self.LOG(f'{self.user} -> {STATUS.OFFLINE} -> {STATUS.LAST_SEEN}={self.user.last_seen}')

        self.client._close()
        self.response_server.remove(self)

class Session_Parser:

    def __init__(self, session: Session):
        self.session = session
        self.user: User = session.user
        
        self.managers = {TYPE.USER: self.user.users, TYPE.GROUP: self.user.groups, TYPE.CHANNEL: self.user.channels}
        
        self.parse_methods = {ACTION.ADD: self.add, ACTION.DELETE: self.delete, ACTION.CREATE: self.create, ACTION.REMOVE: self.remove, ACTION.CHANGE: self.change, ACTION.CHAT: self.chat, ACTION.START: self.start, ACTION.END: self.end}
        
    def add(self, tag: Tag) -> RESPONSE:
        type, id = tag['type', 'id']
        type = TYPE[type]

        if type == TYPE.ADMIN: response = RESPONSE.FAILED
        else:
            manager = self.managers[type]
            response = manager.add(id)

        return response

    def remove(self, tag: Tag) -> RESPONSE:
        type, id = tag['type', 'id']
        type = TYPE[type]

        if (type == None) or (type == TYPE.ADMIN): response = RESPONSE.FAILED
        else:
            manager = self.managers[type]
            response = EXISTS(manager, id)
            if response == RESPONSE.EXIST:
                manager.remove(id)
                response = RESPONSE.SUCCESSFUL
        return response

    def create(self, tag: Tag) -> RESPONSE:
        type, id, name, icon = tag['type', 'id', 'name', 'icon']

        if type in [TYPE.ADMIN, TYPE.USER]: response = RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            manager = self.managers[type]

            response = top_manager.create(id=id, name=name, icon=icon,  creator=self.user)
            if response == RESPONSE.SUCCESSFUL: manager.add(top_manager.OBJS[id])
        return response

    def change(self, tag: Tag) -> RESPONSE:
        id, change, type, data = tag['id', 'change', 'type', 'data']

        if change not in [TAG.ID, TAG.NAME]: return RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            response = EXISTS(top_manager, id)

            if response == RESPONSE.EXIST:
                obj = top_manager.OBJS[id]
                obj.change(**{change.lower(): data})
                response = RESPONSE.SUCCESSFUL

        return response

    def delete(self, tag: Tag) -> RESPONSE:
        type, id = tag['type', 'id']

        if type in [TYPE.ADMIN, TYPE.USER, None]: response = RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            manager = self.managers[type]

            response = top_manager.remove(id)
            if response == RESPONSE.SUCCESSFUL: manager.remove(id)

        return response
    
    def chat(self, tag: Tag) -> RESPONSE:
        recipient, data, chat, type = tag['recipient', 'data', 'chat', 'type']
        # type = [user, group, channel]
        # chat = [text, audio, video]

        top_manager = MANAGERS[type]
        response = top_manager.exists(recipient)

        if response == RESPONSE.EXIST:
            obj = top_manager.OBJS[recipient]
            tag['sender'] = self.user.id

            if chat == CHAT.TEXT: obj.add_chat(tag)
            
            response = RESPONSE.SUCCESSFUL
        return response

    def start(self, tag: Tag) -> RESPONSE:
        ...
    
    def end(self, tag: Tag) -> RESPONSE:
        ...

    def parse(self, tag: Tag) -> Tag:
        action = tag.action
        
        if action in self.parse_methods:
            func = self.parse_methods[action]
            tag = Tag(response=func(tag))
        
        elif action == ACTION.DATA: tag = self.user.data

        elif action == ACTION.STATUS:
            status = {}
            for user in self.user.users:
                if user.status == STATUS.ONLINE: stat = STATUS.ONLINE
                else: stat = user.last_seen

                status[user.id] = stat

            tag = Tag(action=ACTION.STATUS, statuses=status)

        elif action == ACTION.LOGOUT:
            self.session.stop_session()
            tag = Tag(response=RESPONSE.SUCCESSFUL)
        
        elif action in [ACTION.LOGIN, ACTION.SIGNUP]: tag = Tag(response=RESPONSE.SIMULTANEOUS_LOGIN)
        return tag
# ----------------------------------------------------------


# ----------------------------------------------------------
def server_test() -> None:
    nn = 'ade'
    ran = range(1, 5)
    
    for a in ran:
        n = nn + str(a)
        Users.create(id=n, name=n, key=n)

    ade1 = Users.OBJS['ade1']

    for a in ran:
        n = nn + str(a)
        m = 'G_'+n
        Users.OBJS[n].create_group(id=m, name=m)

    for a in ran:
        n = nn + str(a)
        m = 'C_'+n
        Users.OBJS[n].create_channel(id=m, name=m)

    for a in ran:
        n = nn + str(a)
        c = 'C_'+n
        g = 'G_'+n
        ade1.add_user(Users.OBJS[n].id)
        ade1.add_group(g)
        ade1.add_channel(c)
    
    # print(ade1.users)
    # print(ade1.data)
# ----------------------------------------------------------

