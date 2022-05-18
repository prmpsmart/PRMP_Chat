from typing import Union, List, Dict
from .core import _Manager, _User
from .core import *
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File


USERS_SESSIONS: Dict[str, "Session"] = {}
CLIENTS_SOCKETS: List["CLIENTS_SOCKETS"] = []


def remove_client(client):
    if client in CLIENTS_SOCKETS:
        CLIENTS_SOCKETS.remove(client)


class Manager(_Manager):
    def add(self, id: str) -> RESPONSE:
        if (id in self.ids) or (id == self.user.id):
            return RESPONSE.EXIST

        response: RESPONSE = self.OBJ_M.exists(id)
        if response == RESPONSE.EXIST:
            obj = self.OBJ_M.get(id)
            super().add(obj)
            obj.add(self.user.id)
            response = RESPONSE.SUCCESSFUL
        return response

    def remove(self, id: str) -> RESPONSE:
        if id not in self.ids:
            return RESPONSE.EXTINCT

        obj: Base = self.get(id)
        if obj != None:
            obj.remove(id)
            super().remove(id)
            return RESPONSE.SUCCESSFUL


class User(_User):
    def __init__(self, **kwargs) -> None:
        _User.__init__(self, **kwargs)
        self.users = Users_Manager(self)
        self.groups = Groups_Manager(self)
        self.channels = Channels_Manager(self)

        self.queued = []
        self.responses = []
        self.detail_changed_objects = {}

    @property
    def core_data(self):
        return super().data

    @property
    def data(self) -> Tag:
        tag = Tag(
            self.core_data,
            users=[user.core_data for user in self.users.objects],
            groups=[group.data for group in self.groups.objects],
            channels=[channel.data for channel in self.channels.objects],
        )

        return tag

    def create_group(self, **kwargs) -> RESPONSE:
        return self.groups.create(**kwargs)

    def create_channel(self, **kwargs) -> RESPONSE:
        return self.channels.create(**kwargs)

    def add(self, id: str) -> RESPONSE:
        return self.users.add(id)

    def add_group(self, id: str) -> RESPONSE:
        return self.groups.add(id)

    def add_channel(self, id: str) -> RESPONSE:
        return self.channels.add(id)

    def remove(self, multi_user: "Multi_Users") -> RESPONSE:
        if isinstance(multi_user, Group):
            return self.remove_group(multi_user.id)
        else:
            return self.remove_channel(multi_user.id)

    def remove_group(self, id: str) -> RESPONSE:
        self.add_queued(
            Tag(
                action=ACTION.REMOVE_MEMBER,
                type=TYPE.GROUP,
                group_id=id,
                user_id=self.id,
            )
        )
        return self.groups.remove(id)

    def remove_channel(self, id: str) -> RESPONSE:
        self.add_queued(
            Tag(
                action=ACTION.REMOVE_MEMBER,
                type=TYPE.CHANNEL,
                channel_id=id,
                user_id=self.id,
            )
        )
        return self.channels.remove(id)

    def add_queued(self, tag):
        self.queued.append(tag)

    add_chat = add_queued

    def add_response(self, tag):
        self.responses.append(tag)

    def change_detail(self, tag: Tag) -> None:
        name, key, bio, icon = tag["name", "key", "bio", "icon"]

        if name:
            self.name = name
        if key:
            self.key = key
        if bio:
            self.bio = bio
        if icon:
            self.icon = icon

        user: User = None
        for user in self.users:
            user.add_to_detail_changed_objects(self.id, tag)

    def add_to_detail_changed_objects(self, id: str, tag: Tag):
        part_of_user = self.users[id] or self.groups[id] or self.channels[id]

        if part_of_user:
            self.detail_changed_objects[id] = tag

    def add_multi_user_action(self, id: str, tag: Tag):
        part_of_user = self.users[id] or self.groups[id] or self.channels[id]

        if part_of_user:
            self.add_response(tag)


class Managers(Mixin):
    OBJS = {}
    OBJ = None

    @classmethod
    def exists(cls, id: str) -> RESPONSE:
        id = id.lower()
        if id in cls.OBJS:
            return RESPONSE.EXIST
        else:
            return RESPONSE.EXTINCT

    @classmethod
    def get(cls, id: str):
        return cls.OBJS.get(id.lower())

    @classmethod
    def add(cls, id: str, obj: None):
        cls.OBJS[id.lower()] = obj

    @classmethod
    def create(cls, id: str, name: str, **kwargs) -> RESPONSE:
        id = id.lower()
        response = cls.exists(id)
        if response == RESPONSE.EXTINCT:
            obj = cls.OBJ(id=id, name=name, **kwargs)
            cls.add(id, obj)
            return RESPONSE.SUCCESSFUL
        else:
            return response

    @classmethod
    def remove(cls, id) -> RESPONSE:
        id = id.lower()
        response = cls.exists(id)
        if response == RESPONSE.EXIST:
            if id in cls.OBJS:
                del cls.OBJS[id]
                return RESPONSE.SUCCESSFUL
            else:
                return RESPONSE.FAILED
        else:
            return response


class Users(Managers):
    OBJS = {}
    OBJ = User


class Users_Manager(Manager):
    OBJ_M = Users


class Multi_Users(Base):
    def __init__(self, creator: User, only_admin=False, **kwargs):
        Base.__init__(self, **kwargs)
        self._admins = {}
        self._users = {}
        self.last_time: DateTime = None
        self.chats = None

        self.creator = creator
        self.only_admin = bool(only_admin)
        self.add(creator)
        self.add_admin(creator.id)

    @property
    def data(self) -> Tag:
        tag = Tag(
            name=self.name,
            id=self.id,
            icon=self.icon,
            bio=self.bio,
            creator=self.creator.id,
            admins=self.admin_ids,
            users=[user.id for user in self.objects],
            only_admin=self.only_admin,
        )

        return tag

    def add_admin(self, admin_id: str) -> None:
        if admin_id in self._users:
            self._admins[admin_id] = self._users[admin_id]

    def remove_admin(self, admin_id: str) -> None:
        if admin_id in self._admins:
            del self._admins[admin_id]

    def add(self, obj: Union[User, str]) -> None:
        user: User = Users.get(obj) if isinstance(obj, str) else obj

        if user:
            self._users[user.id] = user
            self.add_to_user(user)

    def add_to_user(self, user):
        ...

    @property
    def ids(self) -> list:
        return list(self._users.keys())

    @property
    def user_ids(self) -> list:
        return self.ids

    @property
    def users(self) -> List["_User"]:
        return list(self._users.values())

    @property
    def objects(self) -> List["_User"]:
        return self.users

    @property
    def _objects(self) -> dict:
        return self._users.copy()

    @property
    def admin_ids(self) -> List[str]:
        return list(self._admins.keys())

    @property
    def admins(self) -> List["_User"]:
        return list(self._admins.values())

    def add_chat(self, chat: Tag):
        sender = chat.sender
        if (sender in self.admin_ids) or (self.only_admin == False):
            dic = self._objects
            for id, user in dic.items():
                if id != sender:
                    user.add_chat(chat)

    def broadcast_action(self, tag):
        user: User = None
        for user in self.users:
            user.add_multi_user_action(self.id, tag)

    def change_detail(self, tag: Tag) -> None:
        name, bio, icon = tag["name", "bio", "icon"]

        if name:
            self.name = name
        if bio:
            self.bio = bio
        if icon:
            self.icon = icon

        user: User = None
        for user in self.users:
            user.add_to_detail_changed_objects(self.id, tag)

    def remove_user(self, user: User, admin: User):
        if admin.id != self.id and admin.id not in self.admin_ids:
            return RESPONSE.FAILED

        return self.remove(user.id)

    def remove(self, id: str):
        if id in self.admin_ids:
            return RESPONSE.FAILED

        if id != self.creator.id:
            if id in self.ids:
                user: User = self._users[id]
                user.remove(self)
                del self._users[id]
                return RESPONSE.SUCCESSFUL
        else:
            return RESPONSE.FAILED


class Multi_Users_Manager(Manager):
    OBJ_M = Managers

    def create(self, id: str, name: str, icon: str = "", bio: str = "") -> RESPONSE:
        id = id.lower()
        response: RESPONSE = self.OBJ_M.create(
            id, name, icon=icon, bio=bio, creator=self.user
        )
        if response == RESPONSE.SUCCESSFUL:
            obj = self.OBJ_M.get(id)
            self._objects[id] = obj
        return response


class Group(Multi_Users):
    def add_to_user(self, user: User):
        user.groups.add(self.id)


class Groups(Managers):
    OBJS = {}
    OBJ = Group


class Groups_Manager(Multi_Users_Manager):
    OBJ_M = Groups


class Channel(Multi_Users):
    def __init__(self, creator: User, **kwargs: dict):
        super().__init__(creator, only_admin=True, **kwargs)

    def add_to_user(self, user):
        user.channels.add(self.id)


class Channels(Managers):
    OBJS = {}
    OBJ = Channel


class Channels_Manager(Multi_Users_Manager):
    OBJ_M = Channels


class Client_Socket(Sock):
    TAG = Tag

    def __init__(self, sock_details: tuple):
        Sock.__init__(self, sock_details[0])

        address_port = sock_details[1]
        self.address = address_port[0]
        self.port = address_port[1]
        self.remote = self.socket.getpeername()

        self.user: "User" = None

    def __str__(self):
        return f"Client_Socket(address={self.address}, port={self.port})"

    def __eq__(self, other):
        return str(self) == str(other)


class Server(Mixin, socket.socket):
    "Server socket for creating server that waits for client connections."

    def __str__(self):
        return f'Server(ip={self.ip or "localhost"}, port={self.port})'

    def __init__(
        self,
        ip: str = "",
        port: int = 7767,
        reuse_port: bool = True,
        max_client: int = 3,
        LOG: Callable = print,
        ERROR_LOG: Callable = print,
    ):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if reuse_port:
            try:
                self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except:
                ...

        self.ip = ip
        self.port = port
        self.LOG = LOG
        self.ERROR_LOG = ERROR_LOG

        self.online_clients = {}
        self.max_client = max_client or 10
        self.response_server = Response_Server(self)

        # LOAD()
        # THREAD(self.saveDatas)

        self._stop = False

        self.bind((self.ip, self.port))
        self.listen(self.max_client)

    @property
    def sessions(self) -> int:
        return len(USERS_SESSIONS)

    def accept(self) -> Client_Socket:
        return Client_Socket(socket.socket.accept(self))

    def start(self) -> None:
        self.LOG("Accepting connections !\n")

        self._stop = False

        while not self._stop:
            try:
                client = self.accept()
                THREAD(self.response_server.add, client)
            except Exception as e:
                self.ERROR_LOG(e)
                break

    def saveDatas(self) -> None:
        SAVE()

        time.sleep(5)
        self.saveDatas()

    def stop(self):
        self._stop = True

        self._close()

        users_sessions = USERS_SESSIONS.copy()
        for id, user_session in users_sessions.items():
            user_session.client._close()
            del USERS_SESSIONS[id]
        USERS_SESSIONS.clear()

        clients_sockets = CLIENTS_SOCKETS.copy()
        for client_socket in clients_sockets:
            client_socket._close()
            remove_client(client_socket)
        CLIENTS_SOCKETS.clear()

    def _close(self):
        try:
            self.close()
        except Exception as e:
            self.ERROR_LOG(e)
        try:
            self.shutdown()
        except Exception as e:
            self.ERROR_LOG(e)


class Response_Server:
    def __init__(self, server: Server):
        self.server = server
        self.LOG = server.LOG

    def add(self, client: Client_Socket) -> None:
        self.LOG(client, " connected!")
        CLIENTS_SOCKETS.append(client)

        while not self.server._stop:
            user = None
            tag = client.recv_tag()

            if tag in SOCKET.ERRORS:
                remove_client(client)
                client._close()
                return

            action = tag.action

            if action == ACTION.SIGNUP:

                response = Users.create(*tag["id", "name"], key=tag.key)

                tag.response = response
                soc_resp = client.send_tag(tag)
                if soc_resp in SOCKET.ERRORS:
                    remove_client(client)
                    client._close()
                    return

            elif action == ACTION.LOGIN:
                response = Users.exists(tag.id)

                if response == RESPONSE.EXIST:
                    user = Users.OBJS[tag.id]

                    if user.id in USERS_SESSIONS:
                        response = RESPONSE.SIMULTANEOUS_LOGIN

                    elif user.key == tag.key:
                        response = RESPONSE.SUCCESSFUL
                        client.user = user

                    else:
                        response = RESPONSE.FALSE_KEY

                tag.response = response
                soc_resp = client.send_tag(tag)

                if soc_resp in SOCKET.ERRORS:
                    remove_client(client)
                    client._close()
                    return soc_resp

                if response == RESPONSE.SUCCESSFUL:

                    client.user.change_status(STATUS.ONLINE)
                    session = Session(self, client)
                    USERS_SESSIONS[user.id] = session
                    session.start_session()
                    break

    def remove(self, session) -> None:
        session: Session = session
        id = session.user.id
        if id in USERS_SESSIONS:
            del USERS_SESSIONS[id]


class Session:
    def __str__(self):
        return f"Session(client={self.client}, user={self.user})"

    def __init__(self, response_server: Response_Server, client: Client_Socket):
        self.client = client
        self.response_server = response_server
        self.user = client.user
        self._stop = False

        self.LOG: Callable = self.response_server.server.LOG
        self.parser = Session_Parser(self)

    def broadcast_status(self):
        for id in self.user.users.ids:
            if id in USERS_SESSIONS:
                session = USERS_SESSIONS[id]
                session.client.send_tag(
                    Tag(action=STATUS, id=self.user.id, status=self.user.current_status)
                )

    def send_statuses(self) -> RESPONSE:
        statuses = []
        for user in self.user.users.objects:
            statuses.append((user.id, user.current_status))
        tag = Tag(action=ACTION.STATUS, statuses=statuses)

        return self.client.send_tag(tag)

    def send_detail_changed_objects(self):
        detail_changed_objects: dict = self.user.detail_changed_objects.copy()

        self.LOG(f"Sending {len(detail_changed_objects)} Detail Changed Objects\n")

        if detail_changed_objects:
            for id, tag in detail_changed_objects.items():
                # tag.user_id = id
                # tag.action = ACTION.CHANGE
                res = self.client.send_tag(tag)

                if res in SOCKET.ERRORS:
                    return res

                del self.user.detail_changed_objects[id]
                time.sleep(0.1)

    def send_queued(self):
        queued: List[Tag] = self.user.queued.copy()

        self.LOG(f"Sending {len(queued)} Queued Chats\n")

        if queued:
            for chat in queued:
                res = self.client.send_tag(chat)

                if res in SOCKET.ERRORS:
                    return res

                self.user.queued.remove(chat)
                time.sleep(1)

    def send_responses(self):
        responses: List[Tag] = self.user.responses.copy()

        self.LOG(f"Sending {len(responses)} Responses\n")

        if responses:
            for response in responses:
                res = self.client.send_tag(response)

                if res in SOCKET.ERRORS:
                    return res

                self.user.responses.remove(response)
                time.sleep(0.1)

    def start_session(self) -> None:
        THREAD(self.start_session_sender)
        self.start_session_receiver()

    def start_session_sender(self) -> None:
        self.broadcast_status()
        self.send_statuses()

        while not self.stop:

            if self.user.detail_changed_objects:
                self.send_detail_changed_objects()

            if self.user.queued:
                self.send_queued()

            if self.user.responses:
                self.send_responses()

    @property
    def stop(self):
        return self._stop or self.response_server.server._stop

    def start_session_receiver(self) -> None:
        self.LOG(f"Listening to {self.user}\n")

        data = b""

        while not self.stop:

            read = self.client.catch(self.client.read)

            if read in EMPTY_TAGS:
                continue

            if (not read) or read in SOCKET.ERRORS:
                self.stop_session()
                return

            data += read
            ready_data = []

            if Tag.DELIMITER in data:
                datas = data.split(Tag.DELIMITER)

                if data.endswith(Tag.DELIMITER):
                    data = b""
                    ready_data = datas
                else:
                    data = datas[-1]
                    ready_data = datas[:-1]

            for rdata in ready_data:
                tag = Tag.decode(rdata)
                tag = self.parser.parse(tag)

                if tag:
                    self.user.add_response(tag)

    def stop_session(self) -> None:
        self._stop = True
        self.user.change_status(STATUS.OFFLINE)

        self.LOG(
            f"{self.user} -> {STATUS.OFFLINE} -> {STATUS.LAST_SEEN} = {self.user.str_last_seen}"
        )

        self.response_server.remove(self)
        self.broadcast_status()
        self.client._close()


class Session_Parser:
    def __init__(self, session: Session):
        self.session = session
        self.LOG = session.LOG
        self.user: User = session.user

        self.managers = {
            TYPE.CONTACT: self.user.users,
            TYPE.USER: self.user.users,
            TYPE.GROUP: self.user.groups,
            TYPE.CHANNEL: self.user.channels,
        }

        self.parse_methods = {
            ACTION.ADD: self.add,
            ACTION.ADD_ADMIN: self.add_admin,
            ACTION.ADD_MEMBER: self.add_member,
            ACTION.CALL: self.call,
            ACTION.CALL_REQUEST: self.call_request,
            ACTION.CALL_RESPONSE: self.call_response,
            ACTION.CHANGE: self.change,
            ACTION.CHAT: self.chat,
            ACTION.CREATE: self.create,
            ACTION.DATA: self.data,
            ACTION.DELETE: self.delete,
            ACTION.ONLY_ADMIN: self.only_admin,
            ACTION.REMOVE: self.remove,
            ACTION.REMOVE_ADMIN: self.remove_admin,
            ACTION.REMOVE_MEMBER: self.remove_member,
        }

    def parse(self, tag: Tag) -> Tag:
        action = tag.action
        if action in self.parse_methods:
            func = self.parse_methods[action]
            tag = func(tag)
        elif action == ACTION.LOGOUT:
            self.session.client._close()
            return
        elif action in [ACTION.LOGIN, ACTION.SIGNUP]:
            tag = Tag(response=RESPONSE.SIMULTANEOUS_LOGIN)
        else:
            tag = None
        return tag

    def add(self, tag: Tag) -> Tag:
        type = tag.type
        manager = self.managers[type]
        multi_managers: Multi_Users_Manager = MANAGERS[type]

        if type == TYPE.CONTACT:
            id = tag.user_id

            if Users.exists(id) == RESPONSE.EXIST:
                manager.add(id)

                user: User = Users.get(id)
                tag.data = user.core_data

                user.users.add(self.user.id)
                user.add_queued(
                    Tag(**tag[["action", "type"]], data=self.user.core_data)
                )

                response = RESPONSE.SUCCESSFUL
            else:
                response = RESPONSE.EXTINCT

            tag.response = response
            return tag

        elif type in [TYPE.GROUP, TYPE.CHANNEL]:
            id_name, id = GET_TYPE_ID(tag, 1)

            if multi_managers.get(id):  # a user wants to join a group or channel
                multi: Multi_Users = multi_managers.get(id)
                if isinstance(multi, Group) and multi.only_admin:
                    response = RESPONSE.ADMIN_ONLY

                else:
                    multi.add(self.user.id)
                    tag.data = multi.data
                    response = RESPONSE.SUCCESSFUL
                    multi.broadcast_action(
                        Tag(
                            action=ACTION.ADD_MEMBER,
                            type=type,
                            user_id=self.user.id,
                            **{id_name: id},
                        )
                    )

            else:
                response = RESPONSE.EXTINCT

            tag.response = response
            return tag

    def add_admin(self, tag: Tag) -> Tag:
        user_id = tag.user_id
        multi_user = GET_MULTI_USER(tag)
        if user_id and multi_user:
            multi_user.add_admin(user_id)
            multi_user.broadcast_action(tag)

    def add_member(self, tag: Tag) -> Tag:
        user: User = Users.get(tag.user_id)
        id_name, id = GET_TYPE_ID(tag, 1)
        if user:
            multi_user = GET_MULTI_USER(tag)

            multi_user.add(user)
            multi_user.broadcast_action(tag)

            user.add_queued(
                Tag(
                    data=multi_user.data,
                    type=tag.type,
                    action=ACTION.ADD,
                    **{id_name: id},
                )
            )

    def call(self, tag: Tag):
        recipient = tag.recipient
        user: User = self.user.users[recipient]

        if user:
            user.add_queued(tag)

    call_response = call_request = call

    def change(self, tag: Tag) -> Tag:
        type, data = tag["type", "data"]
        id_name, id = GET_TYPE_ID(tag, 1)

        data = Tag(tag.data, **{id_name: id}, action=tag.action)
        data.type = type

        if type == TYPE.USER:
            self.user.change_detail(data)
            response_tag = Tag(
                **tag[["action", "type"]], **{id_name: id}, response=RESPONSE.SUCCESSFUL
            )

            return response_tag

        elif type in [TYPE.GROUP, TYPE.CHANNEL]:
            managers = MANAGERS[type]
            multi_user: Multi_Users = managers.get(id)
            multi_user.change_detail(data)

    def chat(self, tag: Tag):
        recipient, type = tag["recipient", "type"]
        top_manager = MANAGERS[type]
        response = top_manager.exists(recipient)

        if response == RESPONSE.EXIST:
            obj: Union[User, Group, Channel] = top_manager.OBJS[recipient]
            tag["sender"] = self.user.id
            obj.add_chat(tag)
            response = RESPONSE.SUCCESSFUL

    def create(self, tag: Tag) -> Tag:

        type, name, icon, bio = tag["type", "name", "icon", "bio"]

        id_name, id = GET_TYPE_ID(tag, 1)
        if not id:
            return

        if not CHECK_ID(id):
            multi_managers: Multi_Users_Manager = MANAGERS[type]

            response = multi_managers.create(
                id=id, name=name, icon=icon, bio=bio, creator=self.user
            )

        else:
            response = RESPONSE.EXIST

        tag = Tag(id=tag.id, response=response, action=tag.action, type=type)
        tag[id_name] = id

        return tag

    def data(self, tag: Tag):
        id = tag.id
        if id == self.user.id:
            tag.update(
                response=RESPONSE.SUCCESSFUL, action=ACTION.DATA, data=self.user.data
            )
            return tag

    def delete(self, tag: Tag) -> Tag:
        type, id = tag["type", "id"]

        if type in [TYPE.ADMIN, TYPE.CONTACT, None]:
            response = RESPONSE.FAILED
        else:
            top_manager = MANAGERS[type]
            manager = self.managers[type]

            response = top_manager.remove(id)
            if response == RESPONSE.SUCCESSFUL:
                manager.remove(id)
        tag.response = response
        return tag

    def only_admin(self, tag: Tag) -> Tag:
        user_id = tag.user_id

        multi_user = GET_MULTI_USER(tag)
        if user_id != None and multi_user:
            multi_user.only_admin = bool(user_id)
            multi_user.broadcast_action(tag)

    def remove(self, tag: Tag) -> Tag:
        type, id = tag["type", "id"]
        type = TYPE[type]

        if (type == None) or (type == TYPE.ADMIN):
            response = RESPONSE.FAILED
        else:
            manager = self.managers[type]
            response = EXISTS(manager, id)
            if response == RESPONSE.EXIST:
                manager.remove(id)
                response = RESPONSE.SUCCESSFUL
        tag.response = response
        return tag

    def remove_admin(self, tag: Tag) -> Tag:
        user_id = tag.user_id
        multi_user = GET_MULTI_USER(tag)
        if user_id and multi_user:
            if user_id in multi_user.admin_ids:
                multi_user.remove_admin(user_id)
                multi_user.broadcast_action(tag)

    def remove_member(self, tag: Tag) -> Tag:
        user: User = Users.get(tag.user_id)
        if user:
            multi_user = GET_MULTI_USER(tag)
            if user.id in multi_user.user_ids and user.id not in multi_user.admin_ids:
                multi_user.broadcast_action(tag)
                multi_user.remove_user(user, self.user)


def server_test() -> None:
    nn = "ade"
    ran = range(1, 5)

    for a in ran:
        n = nn + str(a)
        Users.create(id=n, name=n, key=n)

    ade1: User = Users.get("ade1")
    for a in ran:
        n = f"ade{a}"
        m = "G_" + n
        k = "C_" + n
        ade1.create_group(id=m, name=m)
        ade1.create_channel(id=k, name=k)

    for a in ran:
        n = f"ade{a}"
        u = Users.get(n)
        c = Channels.get("C_" + n)
        g = Groups.get("G_" + n)

        for r in ran:
            j = nn + str(r)
            one = a == 1 and r == 2
            two = a == 2 and r == 1
            if not (one or two):
                u.add_user(j)
            c.add(j)
            g.add(j)

    Channels.get("c_ade2").add_admin("ade3")

    Groups.create(
        id="apata", name="Apata Group", creator=Users.get("ade2"), only_admin=0
    )
    Users.create(id="apata_m", name="Apata Miracle", key="apata")

    print(Users.OBJS)


MANAGERS = {
    TYPE.USER: Users,
    TYPE.CONTACT: Users,
    TYPE.GROUP: Groups,
    TYPE.CHANNEL: Channels,
}


def GET_MULTI_USER(tag: Tag) -> Multi_Users:
    managers = MANAGERS.get(tag.type)
    if managers:
        return managers.get(GET_TYPE_ID(tag))


def CHECK_ID(id: str) -> Union[User, Multi_Users]:
    return Users.get(id) or Groups.get(id) or Channels.get(id)


FILE_DIR = os.path.dirname(__file__)
FILE = os.path.join(FILE_DIR, "SERVER_DATA.pc")


def SAVE():
    dic = dict(users=Users.OBJS, groups=Groups.OBJS, channels=Channels.OBJS)
    _file = PRMP_File(FILE, perm="w")
    _file.saveObj(dic)
    _file.save()


def LOAD():
    _file = PRMP_File(FILE)
    dic = _file.loadObj()
    if not dic:
        return

    Users.OBJS.update(dic["users"])
    Groups.OBJS.update(dic["groups"])
    Channels.OBJS.update(dic["channels"])
