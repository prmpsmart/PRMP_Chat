
from .core import *
import time
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File

# for chats in Multi_Users, as the server receives chat directed to this Multi_User object, it sends the chat to all it users
# This object just holds the users together, it does not save chats.


SESSIONS = {}
USERS = {}
USERS_SESSIONS = {}


class Server_Multi_Users(Multi_Users):
    only_admin = False

    def __init__(self, **kwargs):
        Multi_Users.__init__(self, **kwargs)

    def add_chat(self, chat):
        if chat.sender in self.admins or self.only_admin == False:
            dic = dict(**self.admins, **self.chats)
            del dic[chat.sender]

            for user in dic.values(): user.add_chat(chat)
    
    def remove(self, tag):
        id = tag.id
        if id != self.creator.id:
            if id in self.admins: del self.admins[id]
            if id in USERS: del USERS[id]
        

class Group(Server_Multi_Users): ...

class Channel(Server_Multi_Users): only_admin = True

class Server_User(User):
    'User on the server side.'

    def __init__(self, **kwargs):
        User.__init__(self, **kwargs)
        self.queued_chats = []
    
    def dispense(self, socket):
        ...
    
    def data(self):
        users = {}
        groups = {}
        channels = {}

        for user in USERS.values(): users[user.id] = dict(name=user.name, icon=user.icon)
        for group in self.groups.values(): groups[group.id] = dict(name=group.name, icon=group.icon, creator=group.creator.id, admins=list(group.admins.keys()), users=list(group.users.keys()), only_admin=group.only_admin)
        for channel in self.channels.values(): channels[channel.id] = dict(name=channel.name, icon=channel.icon, creator=channel.creator.id, admins=list(channel.admins.keys()), users=list(channel.users.keys()))

        tag = Tag(users=users, groups=groups, channels=channels)

        return tag
    
    def create_group(self, id, name, icon=''):
        response = Groups.create(id, name, icon=icon, creator=self)
        if response == RESPONSE.SUCCESSFUL: self.groups[id] = Groups.OBJS[id]
        return response

    def create_channel(self, id, name, icon=''):
        response = Channels.create(id, name, icon=icon, creator=self)
        if response == RESPONSE.SUCCESSFUL: self.channels[id] = Channels.OBJS[id]
        return response
    
    def add_user(self, id):
        response = Users.exists(id)
        if response == RESPONSE.EXIST:
            user = Users.OBJS[id]
            user.add_user(self)
            super().add_user(user)
        return response

    def add_group(self, id):
        response = Groups.exists(id)
        if response == RESPONSE.EXIST:
            group = Groups.OBJS[id]
            group.add_user(self)
            super().add_group(group)
        return response

    def add_channel(self, id):
        response = Channels.exists(id)
        if response == RESPONSE.EXIST: 
            channel = Channels.OBJS[id]
            channel.add_user(self)
            super().add_channel(channel)
        return response
    
    def add_chat(self, tag):
        if self.status == STATUS.ONLINE: ...
        else: self.queued_chats.append(tag)


# Server Managers

class Managers(Base_All):
    OBJS = {}
    OBJ = None

    @classmethod
    def exists(cls, id):
        if id in cls.OBJS: return RESPONSE.EXIST
        else: return RESPONSE.EXTINCT

    @classmethod
    def create(cls, id, name, **kwargs):
        response = cls.exists(id)
        if response == RESPONSE.EXTINCT:
            try:
                obj = cls.OBJ(id=id, name=name, **kwargs)
                cls.OBJS[id] = obj
                return RESPONSE.SUCCESSFUL
            except: return RESPONSE.FAILED
        else: return response

    @classmethod
    def delete(cls, id):
        response = cls.exists(id)
        if response == RESPONSE.EXIST:
            try:
                del cls.OBJS[id]
                return RESPONSE.SUCCESSFUL
            except: return RESPONSE.FAILED
        else: return response


class Users(Managers):
    OBJS = {}
    OBJ = Server_User

class Groups(Managers):
    OBJS = {}
    OBJ = Group

class Channels(Managers):
    OBJS = {}
    OBJ = Channel

MANAGERS = {TYPE.USER: Users, TYPE.GROUP: Groups, TYPE.CHANNEL: Channels}


FILE_DIR = os.path.dirname(__file__)
FILE = os.path.join(FILE_DIR, 'SERVER_DATA.pc')


def SAVE():
    dic = dict(USERS=Users.OBJS, GROUPS=Groups.OBJS, CHANNELS=Channels.OBJS)
    _file = PRMP_File(FILE, perm='w')
    _file.saveObj(dic)
    _file.save()

def LOAD():
    _file = PRMP_File(FILE)
    dic = _file.loadObj()
    if not dic: return

    Users.OBJS.update(dic['USERS'])
    Groups.OBJS.update(dic['GROUPS'])
    Channels.OBJS.update(dic['CHANNELS'])




class Client_Socket(Sock):
    def __init__(self, sock_details):
        Sock.__init__(self, sock_details[0])

        address_port = sock_details[1]
        self.address = address_port[0]
        self.port = address_port[1]
        self.remote = self.socket.getpeername()
        
        self.user = None
    
    def __str__(self): return f'Client_Socket(address={self.address}, port={self.port})'

    def __eq__(self, other): return str(self) == str(other)

class Session_Parser:

    def __init__(self, client_handler):
        self.client_handler = client_handler
        self.user = client_handler.user
        
        self.managers = {TYPE.USER: self.user.users, TYPE.GROUP: self.user.groups, TYPE.CHANNEL: self.user.channels}
        
        self.parse_methods = {ACTION.ADD: self.add, ACTION.REMOVE: self.remove, ACTION.CREATE: self.create, ACTION.DELETE: self.delete, ACTION.CHANGE: self.change, ACTION.CHAT: self.chat, ACTION.START: self.start, ACTION.END: self.end}
        
    def add(self, tag):
        type, id = tag['type', 'id']
        type = TYPE[type]

        if type == TYPE.ADMIN: response = RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            response = top_manager.exists(id)

            if response == RESPONSE.EXIST:
                obj = top_manager.OBJS[id]
                manager = self.managers[type]

                response = EXISTS(manager, id)
                if response == RESPONSE.EXTINCT:
                    manager.add(obj)
                    response = RESPONSE.SUCCESSFUL
        return response

    def remove(self, tag):
        type, id = tag['type', 'id']
        type = TYPE[type]

        if type == TYPE.ADMIN: response = RESPONSE.FAILED
        else:
            manager = self.managers[type]

            response = EXISTS(manager, id)
            if response == RESPONSE.EXIST:
                manager.remove(id)
                response = RESPONSE.SUCCESSFUL
        return response

    def create(self, tag):
        type, id, name = tag['type', 'id', 'name']

        if type in [TYPE.ADMIN, TYPE.USER]: response = RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            manager = self.managers[type]

            response = top_manager.create(id, name, creator=self.user)
            if response == RESPONSE.SUCCESSFUL: manager.add(top_manager.OBJS[id])
        return response

    def change(self, tag):
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

    def delete(self, tag):
        type, id = tag['type', 'id']
        if type in [TYPE.ADMIN, TYPE.USER]: response = RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            manager = self.managers[type]

            response = top_manager.delete(id)
            if response == RESPONSE.SUCCESSFUL: manager.delete(id)

        return response
    
    def chat(self, tag):
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

    def start(self, tag):
        ...
    
    def end(self, tag):
        ...

    def parse(self, tag):
        action = tag.action
        
        if action in self.parse_methods:
            func = self.parse_methods[action]
            tag = Tag(response=func(tag))
        
        elif action == ACTION.DATA: tag = self.user.data()

        elif action == ACTION.STATUS:
            status = {}
            for user in self.user.users_manager:
                if user.status == STATUS.ONLINE: stat = STATUS.ONLINE
                else: stat = DATE_TIME(user.last_seen)

                status[user.id] = stat

            tag = Tag(action=ACTION.STATUS, status=status)

        elif action == ACTION.LOGOUT:
            self.client_handler.stop_session()
            tag = Tag(response=RESPONSE.SUCCESSFUL)
        
        elif action in [ACTION.LOGIN, ACTION.SIGNUP]: tag = Tag(response=RESPONSE.SIMULTANEOUS_LOGIN)
        
        # tag['date_time'] = DATE_TIME()
        
        return tag

class Session:

    def __str__(self): return f'Session(client={self.client}, user={self.user})'

    def __init__(self, response_server, client):
        self.client = client
        self.user = client.user

        self.user.status = STATUS.ONLINE

        self.response_server = response_server
        self.LOG = self.response_server.server.LOG

        self.parser = Session_Parser(self)

    def start_session(self):
        self.user.change_status(STATUS.ONLINE)

        self.LOG(f'Listening to {self.user}')#, end='\r')
        while True:

            tag = self.client.recv_tag()

            if tag in SOCKETS:
                # means that client == offline
                self.stop_session()
                break

            tag = self.parser.parse(tag)
            soc_resp = self.client.send_tag(tag)
            
            if soc_resp in SOCKETS:
                # means that client == offline
                self.stop_session()
                break

    def stop_session(self):
        self.user.change_status(STATUS.OFFLINE)

        self.LOG(f'{self.client.address} -> {STATUS.OFFLINE} -> {STATUS.LAST_SEEN}={self.user.last_seen}')

        self.client._close()
        self.response_server.remove(self)

class Response_Server:

    def __init__(self, server):
        self.server = server
        self.LOG = server.LOG

    def add(self, client):
        self.LOG(client, 'connected!')

        while True:
            tag = client.recv_tag()
            
            if tag in SOCKETS: return
            
            action = ACTION[tag.action]

            LOG = lambda val: self.LOG(f'{client} -> {action} -> {val}')

            if action == ACTION.SIGNUP:

                response = Users.create(*tag['id', 'name'], key=tag.key)
                
                LOG(response)
                soc_resp = client.send_tag(Tag(response=response))
                if soc_resp in SOCKETS: return
                
                if response == RESPONSE.SUCCESSFUL: user = Users.OBJS[tag.id]

            elif action == ACTION.LOGIN:
                response = Users.exists(tag.id)

                if response == RESPONSE.EXIST:
                    user = Users.OBJS[tag.id]

                    if user.id in USERS or user.status == STATUS.ONLINE: response = RESPONSE.SIMULTANEOUS_LOGIN

                    elif user.key == tag.key:
                        response = RESPONSE.SUCCESSFUL
                        client.user = user

                    else: response = RESPONSE.FALSE_KEY
                    print(user.key)
                
                LOG(response)
                soc_resp = client.send_tag(Tag(response=response))
                if soc_resp in SOCKETS: return soc_resp

                if response == RESPONSE.SUCCESSFUL:
                    session = Session(self, client)

                    SESSIONS[str(session)] = session
                    USERS[user.id] = user
                    USERS_SESSIONS[user.id] = session

                    session.start_session()
                    
                    break

    def remove(self, session):
        str_sess = str(session)
        
        if str_sess in SESSIONS: del SESSIONS[str_sess]
        id = session.user.id
        
        if id in USERS: del USERS[id]

        if id in USERS_SESSIONS: del USERS_SESSIONS[id]



class Server(Base_All, socket.socket):
    'Server socket for creating server that waits for client connections.'

    def __str__(self):
        return f'Server(ip={self.ip or "localhost"}, port={self.port})'

    def __init__(self, ip='', port=7767, reuse_port=True, max_client=3, LOG=print):
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
    def sessions(self): return len(self.response_server.sessions)

    def accept(self): return  Client_Socket(socket.socket.accept(self))

    def set_online_clients(self):
        connections = self.online_clients.copy()

        for conn, _conn in connections.items():
            response = _conn.send_tag(Tag(alive=SOCKET.ALIVE))

            if str(response) != '18':
                _conn.user.change_status(STATUS.OFFLINE)
                del self.online_clients[conn]

        time.sleep(1)
        self.set_online_clients()
    
    def start(self):
        self.LOG('Accepting connections !')

        while True:
            client = self.accept()
            THREAD(self.response_server.add, client)
    
    def saveDatas(self):
        # print('saving', end='\r')
        SAVE()

        time.sleep(500)
        self.saveDatas()



def server_test():
    nn = 'ade'
    for a in range(10):
        n = nn + str(a)
        Users.create(id=n, name=n, key=n)

    ade0 = Users.OBJS['ade0']

    for a in range(3):
        n = nn + str(a)
        m = 'G_'+n
        Users.OBJS[n].create_group(id=m, name=m)

    for a in range(3):
        n = nn + str(a)
        m = 'C_'+n
        Users.OBJS[n].create_channel(id=m, name=m)

    for a in range(1, 3):
        n = nn + str(a)
        c = 'C_'+n
        g = 'G_'+n
        ade0.add_user(Users.OBJS[n].id)
        ade0.add_group(g)
        ade0.add_channel(c)

    # # LOAD()
    # # print(Groups.OBJS)

    # # print(ade2.groups)
    # # print(ade2.channels)
    tag = ade0.data()
    # print(tag)
    en = tag.encode
    # print(len(en))
    tag = Tag.decode(en)
    # print(tag)



