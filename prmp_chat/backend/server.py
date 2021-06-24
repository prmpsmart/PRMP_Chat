
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

    def __str__(self): return f'Session(client={self.client}, user={self.user})'

    def __init__(self, response_server, client):
        self.client = client
        self.user = client.user

        self.user.status = STATUS.ONLINE

        self.response_server = response_server
        self.LOG = self.response_server.server.LOG

        self.parser = Session_Parser(self)

        self.start_session()
    
    def start_session(self):
        self.user.change_status(STATUS.ONLINE)

        while True:

            self.LOG(f'Listening to {self.user}')#, end='\r')

            tag = self.client.recv_tag()

            if tag in SOCKETS:
                # means that client is offline
                self.stop_session()
                break

            tag = self.parser.parse(tag)
            soc_resp = self.client.send_tag(tag)
            
            if soc_resp in SOCKETS:
                # means that client is offline
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

        self.sessions = {}
        self.users = {}
        self.users_sessions = {}

    def add(self, client, from_signup=False):
        tag = client.recv_tag()
        
        if tag in SOCKETS: return
        
        action = ACTION[tag.action]

        LOG = lambda val: self.LOG(f'{client} -> ACTION.{action} -> RESPONSE.{val}')

        if not from_signup: self.LOG(client, 'connected!')

        if action is ACTION.SIGNUP:

            response = Users.create(*tag['id', 'name'], key=tag.key)
            
            LOG(response)
            soc_resp = client.send_tag(Tag(response=response))
            if soc_resp in SOCKETS: return
            
            if response is RESPONSE.SUCCESSFUL:
                user = Users.OBJS[tag.id]
                self.add(client, from_signup=1)

        elif action is ACTION.LOGIN:
            response = Users.exists(tag.id)

            if response is RESPONSE.EXIST:
                user = Users.OBJS[tag.id]

                if user.id in self.users or user.status is STATUS.ONLINE: response = RESPONSE.SIMULTANEOUS_LOGIN

                elif user.key == tag.key:
                    response = RESPONSE.SUCCESSFUL
                    client.user = user

                else: response = RESPONSE.FALSE_KEY
            
            LOG(response)
            soc_resp = client.send_tag(Tag(response=response))
            if soc_resp in SOCKETS: return soc_resp

            if response is RESPONSE.SUCCESSFUL:
                session = Session(self, client)

                self.sessions[str(session)] = session
                self.users[user.id] = user
                self.users_sessions[user.id] = session

    def remove(self, session):

        if str(session) in self.sessions: del self.sessions[str(session)]
        id = session.user.id
        if id in self.users: del self.users[id]
        if id in self.users_sessions: del self.users_sessions[id]

        self.server.remove(session.client)


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

        self.connections = {}

        self.max_client = max_client or 10
        self.response_server = Response_Server(self)

        self.bind((self.ip, self.port))
        self.listen(self.max_client)
    
    @property
    def sessions(self): return len(self.response_server.sessions)

    @property
    def connected(self): return len(self.connections)
    
    def accept(self): return  Client_Socket(socket.socket.accept(self))

    def set_online_clients(self):
        connections = self.connections.copy()

        for conn, _conn in connections.items():
            response = _conn.send(Tag(alive=SOCKET.ALIVE))

            if str(response) != '18': del self.connections[conn]

        time.sleep(1)
        self.set_online_clients()
    
    def start(self):
        self.LOG('Accepting connections !')
        # THREAD(self.set_online_clients)

        while True:
            client = self.accept()

            self.connections[str(client)] = client
            
            # self.response_server.add(client)
            THREAD(self.response_server.add, client)

            self.LOG(f'TOTAL OF {self.connected} CLIENTS ARE ONLINE')

    def remove(self, client):
        if str(client) in self.connections: del self.connections[str(client)]
        self.LOG(f'TOTAL OF {self.connected} CLIENTS ARE ONLINE')






