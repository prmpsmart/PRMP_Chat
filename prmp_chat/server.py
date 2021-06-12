
from .core import *
import time

# for chats in Multi_Users, as the server receives chat directed to this Multi_User object, it sends the chat to all it users
# This object just holds the users together, it does not save chats.

class Group(Multi_Users): ...

class Channel(Multi_Users): only_admin = True

class Server_User(User):
    'User on the server side.'

    def __init__(self, **kwargs):
        User.__init__(self, **kwargs)
        self.queued_chats = []



# Server Managers

class Managers:
    OBJS = {}
    OBJ = None

    @classmethod
    def exists(cls, id):
        if id in cls.OBJS: return RESPONSE.EXIST
        else: return RESPONSE.EXTINCT

    @classmethod
    def create(cls, id, name, **kwargs):
        response = cls.exists(id)
        if response is RESPONSE.EXTINCT:
            try:
                obj = cls.OBJ(id=id, name=name, **kwargs)
                cls.OBJS[id] = obj
                return RESPONSE.SUCCESSFUL
            except: return RESPONSE.FAILED
        else: return response

    @classmethod
    def delete(cls, id):
        response = cls.exists(id)
        if response is RESPONSE.EXIST:
            try:
                del cls.OBJS[id]
                return RESPONSE.SUCCESSFUL
            except: return RESPONSE.FAILED
        else: return response

class Users(Managers):
    OBJ = Server_User

class Groups(Managers):
    OBJ = Group

class Channels(Managers):
    OBJ = Channel

MANAGERS = {TYPE.USER: Users, TYPE.GROUP: Groups, TYPE.CHANNEL: Channels}



class Session_Parser:

    def __init__(self, client_handler):
        self.client_handler = client_handler
        self.user = client_handler.user
        
        self.managers = {TYPE.USER: self.user.users, TYPE.GROUP: self.user.groups, TYPE.CHANNEL: self.user.channels}
        
        self.parse_methods = {ACTION.ADD: self.add, ACTION.REMOVE: self.remove, ACTION.CREATE: self.create, ACTION.DELETE: self.delete, ACTION.CHANGE: self.change, ACTION.CHAT: self.chat, ACTION.START: self.start, ACTION.END: self.end}
        
    def add(self, tag):
        type, id = tag['type', 'id']
        type = TYPE[type]

        if type is TYPE.ADMIN: ...
        else:
            top_manager = MANAGERS[type]
            response = top_manager.exists(id)

            if response is RESPONSE.EXIST:
                obj = top_manager.OBJS[id]
                manager = self.managers[type]

                response = EXISTS(manager, id)
                if response is RESPONSE.EXTINCT:
                    manager.add(obj)
                    response = RESPONSE.SUCCESSFUL
            return response

    def remove(self, tag):
        type, id = tag['type', 'id']
        type = TYPE[type]

        if type is TYPE.ADMIN: ...
        else:
            manager = self.managers[type]

            response = EXISTS(manager, id)
            if response is RESPONSE.EXIST:
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
            if response is RESPONSE.SUCCESSFUL: manager.add(top_manager.OBJS[id])
            return response

    def change(self, tag):
        id, change, type, data = tag['id', 'change', 'type', 'data']

        if change not in [TAG.ID, TAG.NAME]: return RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            response = EXISTS(top_manager, id)

            if response is RESPONSE.EXIST:
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
            if response is RESPONSE.SUCCESSFUL: manager.delete(id)

            return response
    
    def chat(self, tag):
        recipient, data, chat, type = tag['recipient', 'data', 'chat', 'type']
        top_manager = MANAGERS[type]
        response = top_manager.exists(recipient)

        if response is RESPONSE.EXIST:
            obj = top_manager[recipient]
            tag['sender'] = self.user.id

            obj.chat(tag)
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

        elif action is ACTION.STATUS:
            status = {}
            for user in self.user.users_manager:
                if user.status is STATUS.ONLINE: stat = STATUS.ONLINE
                else: stat = DATE_TIME(user.last_seen)

                status[user.id] = stat

            tag = Tag(action=ACTION.STATUS, status=status)

        elif action is ACTION.LOGOUT:
            self.client_handler.stop_session()
            tag = Tag(response=RESPONSE.SUCCESSFUL)
        
        tag['date'] = DATE_TIME()
        
        return tag

class Session:

    def __init__(self, response_server, client, client_address, user):
        self.client = client
        self.client_address = client_address
        self.user = user
        self.user.status = STATUS.ONLINE
        self.response_server = response_server
        self.LOG = self.response_server.server.LOG

        self.parser = Session_Parser(self)

        self.start_session()
    
    def start_session(self):
        self.user.change_status(STATUS.ONLINE)

        while True:

            self.LOG(f'Listening to {self.user}')#, end='\r')

            tag = RECV(self.client)

            if tag in SOCKETS:
                # means that client is offline
                self.stop_session()
                break

            tag = self.parser.parse(tag)
            soc_resp = SEND(self.client, tag)
            
            if soc_resp in SOCKETS:
                # means that client is offline
                self.stop_session()
                break

    def stop_session(self):
        self.user.change_status(STATUS.OFFLINE)

        self.LOG(f'{self.client_address} -> {STATUS.OFFLINE} -> {STATUS.LAST_SEEN}={self.user.last_seen}')

        self.response_server.remove(self)

class Response_Server:

    def __init__(self, server):
        self.server = server
        self.LOG = server.LOG

        self.address_client_map = {}
        self.user_client_map = {}
        self.address_user_map = {}

    def add(self, client, client_address, from_signup=False):
        tag = RECV(client)
        
        if tag in SOCKETS: return
        
        action = ACTION[tag.action]

        LOG = lambda val: self.LOG(f'{client_address} -> ACTION.{action} -> RESPONSE.{val}')

        if not from_signup: self.LOG(client_address, 'connected!')

        if action is ACTION.SIGNUP:

            response = Users.create(*tag['id', 'name'], key=tag.key)
            
            if response is RESPONSE.SUCCESSFUL:
                user = Users.OBJS[tag.id]
                self.add(client, client_address, from_signup=1)

            LOG(response)
            soc_resp = SEND(client, Tag(response=response))
            if soc_resp in SOCKETS: return

        elif action is ACTION.LOGIN:
            response = Users.exists(tag.id)

            if response is RESPONSE.EXIST:
                user = Users.OBJS[tag.id]

                if user.id in self.user_client_map or user.status is STATUS.ONLINE: response = RESPONSE.SIMULTANEOUS_LOGIN

                elif user.key == tag.key:
                    response = RESPONSE.SUCCESSFUL

                    self.address_client_map[client_address] = client
                    self.address_user_map[client_address] = user.id
                    self.user_client_map[user.id] = client

                else: response = RESPONSE.FALSE_KEY
            
            LOG(response)
            soc_resp = SEND(client, Tag(response=response))
            if soc_resp in SOCKETS: return soc_resp

            if response is RESPONSE.SUCCESSFUL: Session(self, client, client_address, user)

    def remove(self, cl_in):
        self.address_client_map[cl_in.client_address].close()

        del self.address_client_map[cl_in.client_address]
        del self.address_user_map[cl_in.client_address]
        del self.user_client_map[cl_in.user.id]

        client = self.address_client_map[cl_in.client_address]
        client_address = cl_in.client_address
        self.server.remove((client, client_address))

class Server(socket.socket):
    'Server socket for creating server that waits for client connections.'
    
    def __str__(self) -> str:
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
        self._online_clients = []
        self.online_clients = 0

        self.max_client = max_client or 10
        self.response_server = Response_Server(self)

        self.bind((self.ip, self.port))
        self.listen(self.max_client)
    
    def set_online_clients(self):
        o_c = []
        on_cl = self._online_clients.copy()

        for online_client in on_cl:
            response = SEND(online_client[0], Tag(alive=SOCKET.ALIVE))

            if str(response) == '18': o_c.append(online_client)
            else: self._online_clients.remove(online_client)

        self._online_clients = o_c
        self.online_clients = len(o_c)

        time.sleep(.5)
        self.set_online_clients()
    
    def start(self):
        self.LOG('Accepting connections !')
        THREAD(self.set_online_clients)

        while True:
            client, address = self.accept()
            self._online_clients.append((client, address))
            
            THREAD(self.response_server.add, client, address)

            self.LOG(f'TOTAL OF {self.online_clients+1} CLIENTS ARE ONLINE')
    
    def remove(self, client):
        if client in self._online_clients: self.online_clients.remove(client)






