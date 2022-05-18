from typing import Any, Dict, Union
from .client_database import User_DB
from .core import _Manager, _User_Base, _User
from .core import *


class Manager(_Manager):
    OBJ = None

    def add(self, tag: Tag) -> Union["Multi_Users", "Contact"]:
        id = tag.id
        if id != self.user.id:
            if self.OBJ:
                obj = self.get(id)
                if obj:
                    obj.change_data(tag)
                else:
                    obj = self.OBJ(self.user, tag)
                    super().add(obj)

                return obj


class Chats:
    def __init__(self, user: "User") -> None:
        self.user = user
        self.chats_dict = {}
        self.chats: List[Tag] = []
        self.last_time = DATETIME(num=0)

    def add_chat(self, tag: Tag) -> None:
        if tag.id not in self.chats_dict:
            self.last_time = tag.get_date_time() or DATETIME(num=0)

            tag.seen = tag.sender == self.user.id

            self.chats.append(tag)
            self.chats_dict[tag.id] = tag

    @property
    def last_chat(self) -> Tag:
        if self.chats:
            return self.chats[-1]

    def unseen_chats(self) -> List[Tag]:
        unseens = []
        for chat in self.chats:
            if not chat.seen:
                unseens.append(chat)
        return unseens

    @property
    def unseens(self) -> int:
        value = len(self.unseen_chats())
        return value

    def remove_chat(self, tag_id: str):
        if tag_id in self.chats_dict:
            tag: Tag = self.chats_dict[tag_id]
            del self.chats_dict[tag_id]
            self.chats.remove(tag)


class Contact(Chats, _User_Base):
    def __init__(self, user: "User", tag: Tag):
        _User_Base.__init__(self, id=tag.id, name=tag.name, icon=tag.icon, bio=tag.bio)
        Chats.__init__(self, user)
        self.change_status(tag.status)


class Contacts_Manager(Manager):
    OBJ = Contact

    def add_chat(self, chat: Tag) -> None:
        id = chat.sender
        if id == self.user.id:
            id = chat.recipient
        obj = self.get(id)
        if obj != None:
            obj.add_chat(chat)


class Multi_Users(Chats, Base):
    only_admin = False

    def __init__(self, user: "User", tag: Tag):
        Base.__init__(self, id=tag.id, name=tag.name, icon=tag.icon, bio=tag.bio)
        Chats.__init__(self, user)

        self.creator: str = tag.creator
        self.users = list(tag.users or [])
        self.admins = list(tag.admins or [])

    def change_data(self, tag: Tag):
        super().change_data(tag)
        self.users = list(tag.users or [])
        self.admins = list(tag.admins or [])

        DB.SAVE_USER(self.user)

    def add_user(self, id: str):
        if id not in self.users:
            self.users.append(id)

    def add_admin(self, id: str):
        if (id in self.users) and (id not in self.admins):
            self.admins.append(id)


class Group(Multi_Users):
    def __init__(self, user: "User", tag: Tag):
        super().__init__(user, tag)
        self.only_admin: bool = bool(tag.only_admin)

    def change_data(self, tag: Tag):
        super().change_data(tag)
        self.only_admin = bool(tag.only_admin)


class Groups_Manager(Manager):
    OBJ = Group


class Channel(Multi_Users):
    only_admin = True


class Channels_Manager(Manager):
    OBJ = Channel


class User(_User):
    i = False

    @classmethod
    def load_user(cls):
        return User_DB().load_user()

    @classmethod
    def i(cls):
        return "i" in os.sys.argv

    @property
    def user_db(self):
        return User_DB(self)

    def __init__(self, **kwargs):
        _User.__init__(self, **kwargs)
        self.users = Contacts_Manager(self)
        self.groups = Groups_Manager(self)
        self.channels = Channels_Manager(self)

        self.queued = {}
        self.recv_data = False
        self.pending_change_data: Tag = None

        self.pending_created_objects = {}

        self.contacts = self.users

    def set_pending_change_data(self, tag: Tag):
        self.pending_change_data = tag

    def clear_pending_change_data(self):
        self.pending_change_data = None

    def implement_change(self):
        if self.pending_change_data:
            self.change_data(self.pending_change_data)
            self.clear_pending_change_data()

            DB.SAVE_USER(self)

    def load_data(self, tag: Tag):
        data = Tag(tag.data)
        self.name = data.name or ""
        self.icon = data.raw_icon or ""
        self.bio = data.bio
        self.change_status(data.status)

        other_datas = dict(users=data.users, groups=data.groups, channels=data.channels)

        for name, objs in other_datas.items():
            manager: Manager = getattr(self, name)

            for obj in objs:
                manager.add(obj)

        self.recv_data = True
        DB.SAVE_USER(self)

        # self.user_db.save_user(self)

    def add_chat(self, tag: Tag, saved=False):
        type = tag.type
        if type == TYPE.CONTACT:
            self.users.add_chat(tag)
        elif type == TYPE.GROUP:
            self.groups.add_chat(tag)
        elif type == TYPE.CHANNEL:
            self.channels.add_chat(tag)
        else:
            return

        if tag.sender == self.id and not tag.sent:
            self.add_queued(tag)

        if not saved:
            # self.user_db.add_chat(tag)
            ...

    def add_queued(self, tag: Tag):
        if tag.id not in self.queued:
            self.queued[tag.id] = tag

    def add_user(self, user: Contact):
        super().add_user(user)
        # self.user_db.add_user(user)

    def add_group(self, group: Group):
        super().add_group(group)
        # self.user_db.add_group(group)

    def add_channel(self, channel: Channel):
        super().add_channel(channel)
        # self.user_db.add_channel(channel)

    def get_chat_object(self, id):
        return self.users[id] or self.groups[id] or self.channels[id]


class Socket(socket.socket, Sock):
    def __init__(self, *args, **kwargs):
        socket.socket.__init__(self, *args, **kwargs)
        Sock.__init__(self)


class Client:
    "Client socket for connection with the server."

    def __str__(self) -> str:
        return f"Client(ip={self.ip}, port={self.port})"

    def __init__(
        self,
        ip="127.0.0.1",
        port=7767,
        user=None,
        relogin=0,
        LOG=print,
        STATUS_LOG: Callable[[STATUS], None] = None,
        CHAT_STATUS: Callable[[Tag], None] = None,
        RECV_LOG: Callable[[Tag], None] = None,
    ):

        self.receivers = {
            ACTION.ADD: self.add_receiver,
            ACTION.ADD_ADMIN: self.add_admin_receiver,
            ACTION.ADD_MEMBER: self.add_member_receiver,
            ACTION.CHANGE: self.change_receiver,
            ACTION.CHAT: self.chat_receiver,
            ACTION.CREATE: self.create_receiver,
            ACTION.DATA: self.data_receiver,
            ACTION.ONLY_ADMIN: self.only_admin_receiver,
            ACTION.REMOVE_ADMIN: self.remove_admin_receiver,
            ACTION.REMOVE_MEMBER: self.remove_member_receiver,
            ACTION.STATUS: self.status_receiver,
        }

        self.create_socket()

        self._stop = False  # stop connection or try to relogin
        self.ip = ip
        self.port = port
        self.user = user

        self.relogin = relogin  # try to relogin after connection failure
        self.LOG = LOG  # a function or method to receive logs, defaults is print
        self.STATUS_LOG = STATUS_LOG  # a function or method to receive STATUS logs
        self.CHAT_STATUS = (
            CHAT_STATUS  # a function or method to receive CHAT TAG status
        )
        self.RECV_LOG = RECV_LOG  # a function or method to receive TAG logs

    def log(self, *args):
        if self.LOG:
            self.LOG(*args)

    def create_socket(self):
        self.socket = Socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_tag(self, tag: Tag):
        return self.socket.send_tag(tag)

    def send_action_tag(self, tag: Tag):
        GENERATE_ACTION_ID(tag)
        res = self.send_tag(tag)
        if (not isinstance(res, int)) and (
            tag.action not in [ACTION.CALL, ACTION.CALL_RESPONSE, ACTION.CALL_REQUEST]
        ):
            self.user.add_queued(tag)
        return res

    def recv_tag(self, *args, **kwargs):
        return self.socket.recv_tag(*args, **kwargs)

    def recv_tags(self):
        return self.socket.recv_tags()

    def sendall_tag(self, tag: Tag):
        return self.socket.sendall_tag(tag)

    def set_user(self, user: User):
        self.user = user

    @property
    def alive(self):
        return self.socket.alive

    @property
    def online(self):
        return self.alive and self.user and (STATUS.ONLINE == self.user.current_status)

    def _connect(self):
        # self.log('Connecting to Server\n')

        if self.alive:
            return True

        alive = self.socket._connect(self.ip, self.port)
        if not alive:
            self.create_socket()
            alive = self.socket._connect(self.ip, self.port)

        return alive

    def signup(
        self,
        id,
        key,
        name="",
        login=False,
        start=False,
    ):
        if not self._connect():
            return
        self.log("Signup Started")

        assert id and key, "Provide [id, key] or user"

        action = ACTION.SIGNUP
        tag = Tag(id=id, name=name, key=key, action=action)
        soc_resp = self.send_tag(tag)
        if soc_resp in SOCKET.ERRORS:
            self.log(soc_resp)
            return soc_resp

        response_tag = self.recv_tag()
        if response_tag in SOCKET.ERRORS:
            self.log(response_tag)
            return response_tag

        response = response_tag.response

        self.log(f"{action} -> {response}")

        if response == RESPONSE.SUCCESSFUL:
            if not self.user:
                self.user = User(id=id, name=name, key=key)
            if login:
                self.login(start=start)

        return response

    def login(self, id="", key="", start=False):
        if not self._connect():
            return SOCKET.CLOSED

        self.log("Login Started")

        id = id or self.user.id
        key = key or self.user.key

        assert id and key, "Provide [id, key] or user with valid id and key"

        action = ACTION.LOGIN
        tag = Tag(id=id, key=key, action=action)

        success = 1

        soc_resp = self.send_tag(tag)
        if soc_resp in SOCKET.ERRORS:
            success = 0
            response = soc_resp

        else:
            response_tag = self.recv_tags()
            if response_tag in SOCKET.ERRORS:
                success = 0
                response = response_tag

        if success:
            response = response_tag[0].response
            self.log(f"{action} -> {response}")

            if response == RESPONSE.SUCCESSFUL:
                self._stop = False

                if (not self.user) or (self.user.id != id):
                    self.user = User(id=id, key=key)

                self.change_status(STATUS.ONLINE)

                DB.SAVE_USER(self.user)

                if start:
                    self.start_session()

        elif self.relogin:
            self.re_login(start)

        return response

    def re_login(self, start=False):
        while self.user.status == STATUS.OFFLINE:
            if self._stop:
                return

            res = self.login(start=start)
            if res in [RESPONSE.SUCCESSFUL, RESPONSE.EXTINCT]:
                return res

            time.sleep(1)

    def start_session(self):
        self.log("Listening to Server.")

        data = b""

        if not self.user.recv_data:
            self.send_data(self.user.id)

        while not self._stop:

            if self.user.queued:
                self.send_queued_tags()

            read = self.socket.catch(self.socket.read)

            if (not read) or (read in EMPTY_TAGS):
                continue

            if read in SOCKET.ERRORS:
                self.gone_offline(read)

                if self.relogin:
                    self.log("RE-LOGIN in progress!")
                    res = self.re_login()

                    if res != RESPONSE.SUCCESSFUL:

                        return
                else:
                    return

            else:
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
                    self.parse(tag)

    def logout(self, close=True):
        soc_resp = self.send_tag(Tag(action=ACTION.LOGOUT))
        if isinstance(soc_resp, int):
            self.stop(close)
            soc_resp = RESPONSE.SUCCESSFUL
        return soc_resp

    def stop(self, close=True):
        if not self._stop:
            self.relogin = False
            if close:
                self.socket._close()
            self.gone_offline("STOP")
            self._stop = True

    def gone_offline(self, read):
        if self.user:
            self.change_status(STATUS.OFFLINE)
            self.log("Reason=", read, " -> GONE OFFLINE", self.user.str_last_seen)

    def change_status(self, status):
        self.user.change_status(status)

        if self.STATUS_LOG:
            self.STATUS_LOG(status)

    # senders
    def send_data(self, id: str, type=TYPE.CONTACT):
        tag = Tag(id=id, action=ACTION.DATA, type=type)
        return self.send_tag(tag)

    def send_chat(
        self, recipient: str, text="", data="", chat=CHAT.TEXT, type=TYPE.CONTACT
    ):
        tag = Tag(
            recipient=recipient,
            data=data,
            chat=chat,
            type=type,
            sender=self.user.id,
            action=ACTION.CHAT,
            date_time=DATETIME(),
            text=text,
        )
        return self.send_chat_tag(tag)

    def send_chat_tag(self, tag: Tag, resend=False) -> Tag:
        GENERATE_CHAT_ID(tag)
        res = self.send_tag(tag)
        tag.sent = isinstance(res, int)
        if not resend:
            self.user.add_chat(tag)
        return tag

    def send_queued_tags(self):
        queued: Dict[str, Tag] = self.user.queued.copy()

        if queued:
            for chat in queued.values():
                tag = self.send_chat_tag(chat, resend=True)
                time.sleep(1)

                if tag.sent:
                    del self.user.queued[tag.id]
                    if tag.action == ACTION.CHAT and self.CHAT_STATUS:
                        self.CHAT_STATUS(tag)
                else:
                    # self.user.user_db.chat_sent(tag)
                    ...

    # receivers
    def parse(self, tag: Tag):
        action = tag.action
        receiver = self.receivers.get(action)

        if receiver:
            receiver(tag)

        if self.RECV_LOG:
            self.RECV_LOG(tag)

    def get_type_id(self, tag: Tag) -> str:
        add_type = tag.type

        return (
            tag.user_id
            if add_type == TYPE.USER
            else tag.group_id
            if add_type == TYPE.GROUP
            else tag.channel_id
            if add_type == TYPE.CHANNEL
            else ""
        )

    def get_multi_user(self, tag: Tag) -> Multi_Users:
        type = tag.type

        manager: Manager = None

        if type == TYPE.GROUP:
            manager = self.user.groups

        elif type == TYPE.CHANNEL:
            manager = self.user.channels

        if manager:
            return manager[self.get_type_id(tag)]

    def get_add_method(self, type):
        add = None
        if type == TYPE.CONTACT:
            add = self.user.users.add
        elif type == TYPE.GROUP:
            add = self.user.groups.add
        elif type == TYPE.CHANNEL:
            add = self.user.channels.add

        return add

    def add_receiver(self, tag: Tag):
        if tag.data:
            add = self.get_add_method(tag.type)
            if add:
                tag.obj = add(Tag(values=tag.data))

    def add_admin_receiver(self, tag: Tag):
        multi_user = self.get_multi_user(tag)
        user_id = tag.user_id

        if multi_user and user_id:
            multi_user.add_admin(user_id)

    def add_member_receiver(self, tag: Tag):
        multi_user = self.get_multi_user(tag)
        print(tag)
        user_id = tag.user_id

        if multi_user and user_id:
            multi_user.add_user(user_id)

        elif user_id == self.user.id:
            data = tag.data
            if data:
                add_type = tag.type
                add = self.get_add_method(add_type)
                if add:
                    tag.obj = add(Tag(values=data))

    def change_receiver(self, tag: Tag):
        id = self.get_type_id(tag)

        if id == self.user.id:
            if tag.response == RESPONSE.SUCCESSFUL:
                self.user.implement_change()

        elif id:
            chat_object = self.user.get_chat_object(id)

            if chat_object:
                chat_object.change_data(tag)

    def chat_receiver(self, tag: Tag):
        self.user.add_chat(tag)

    def create_receiver(self, tag: Tag):
        type, response = tag["type", "response"]
        if response == RESPONSE.SUCCESSFUL:
            pending_object = self.user.pending_created_objects.get(tag.id)
            if pending_object:
                add = self.get_add_method(type)
                tag.obj = add(pending_object)

    def data_receiver(self, tag: Tag):
        if tag.response == RESPONSE.SUCCESSFUL:
            if tag.id == self.user.id:
                self.user.load_data(tag)

    def only_admin_receiver(self, tag: Tag):
        only_admin = bool(tag.user_id)
        multi_user = self.get_multi_user(tag)
        if multi_user:
            multi_user.only_admin = only_admin

    def remove_admin_receiver(self, tag: Tag):
        multi_user = self.get_multi_user(tag)
        user_id = tag.user_id

        if multi_user and user_id:
            if user_id in multi_user.admins:
                multi_user.admins.remove(user_id)

    def remove_member_receiver(self, tag: Tag):
        multi_user = self.get_multi_user(tag)
        user_id = tag.user_id

        if multi_user and user_id:
            if user_id in multi_user.admins:
                multi_user.admins.remove(user_id)
            if user_id in multi_user.users:
                multi_user.users.remove(user_id)

    def status_receiver(self, tag: Tag):
        if tag.id:
            user = self.user.users.get(tag.id)
            if user:
                user.change_status(tag.status)
        elif tag.statuses:
            for id, status in tag.statuses:
                user = self.user.users.get(id)
                if user:
                    user.change_status(status)


class DB:
    FILE_DIR = os.path.dirname(__file__)
    FILE = os.path.join(FILE_DIR, "CLIENT_DATA.pc")

    DEFAULT_SAVE_DATA = dict(
        user="", icon_set="svg", users={}, server_settings=("127.0.0.1", 7767)
    )
    SAVE_DATA = {}

    @classmethod
    def SAVE(cls):
        file = PRMP_File(cls.FILE, perm="wb")
        file.saveObj(cls.SAVE_DATA)
        file.save()
        file.close()

    @classmethod
    def LOAD(cls):
        file = PRMP_File(cls.FILE)
        save_data = file.loadObj()
        file.close()
        if isinstance(save_data, dict):
            cls.SAVE_DATA = save_data

    @classmethod
    def SAVE_USER(cls, user: User):
        users = cls.SAVE_DATA.get("users")
        id = user.id
        if isinstance(users, dict):
            users[id] = user
            cls.SAVE_DATA["users"] = users
        else:
            cls.SAVE_DATA["users"] = {id: user}

        if not User.i():
            cls.SAVE_DATA["user"] = id

        cls.SAVE()

    @classmethod
    def CLEAR_USER(cls, id: str):
        users = cls.SAVE_DATA.get("users")
        if isinstance(users, dict):
            if id in users:
                del users[id]
                cls.SAVE_DATA["users"] = users
            cls.SAVE()

    @classmethod
    def GET_USER(cls, id: str) -> User:
        users = cls.SAVE_DATA.get("users")
        if isinstance(users, dict):
            return users.get(id)

    @classmethod
    def GET_LAST_USER(cls) -> User:
        if User.i():
            return

        id: str = cls.SAVE_DATA.get("user")
        if id:
            return cls.GET_USER(id)

    @classmethod
    def GET_SERVER_SETTINGS(cls) -> tuple:
        return cls.SAVE_DATA.get("server_settings") or cls.DEFAULT_SAVE_DATA.get(
            "server_settings"
        )

    @classmethod
    def SET_SERVER_SETTINGS(cls, server_settings: tuple):
        cls.SAVE_DATA["server_settings"] = server_settings
        cls.SAVE()

    @classmethod
    def GET_ICON_SET(cls) -> str:
        icon_set = cls.SAVE_DATA.get("icon_set") or cls.DEFAULT_SAVE_DATA.get(
            "icon_set"
        )
        return icon_set

    @classmethod
    def SET_ICON_SET(cls, icon_set: str):
        cls.SAVE_DATA["icon_set"] = icon_set
        cls.SAVE()
