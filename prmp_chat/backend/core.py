from typing import Callable
import json, threading, socket, os, time, hashlib
from typing import List
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File, base64


# DATETIME--------------------------------------------------
_DATETIME_ = 0
try:
    from PySide6.QtCore import QDateTime as DateTime

    OFFLINE_FORMAT = "OFFLINE | dd/MM/yyyy | HH:mm:ss"

except:
    from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime as DateTime

    OFFLINE_FORMAT = "OFFLINE | %d/%m/%Y | %H:%M:%S"
    _DATETIME_ = 1


def THREAD(target, *args, **kwargs):
    threading.Thread(target=target, args=args, kwargs=kwargs).start()


def DATETIME(date_time=None, num=1):
    if date_time == None:
        date_time = DateTime.now() if _DATETIME_ else DateTime.currentDateTime()
        if num:
            return DATETIME(date_time)
        else:
            return date_time

    if isinstance(date_time, int) and date_time >= 0:
        return (
            DateTime.fromtimestamp(date_time)
            if _DATETIME_
            else DateTime.fromMSecsSinceEpoch(date_time)
            # else DateTime.fromSecsSinceEpoch(date_time)
        )

    else:
        return (
            int(date_time.timestamp())
            if _DATETIME_
            else date_time.toMSecsSinceEpoch()
            # else date_time.toSecsSinceEpoch()
        )


def TIME(dateTime: DateTime) -> str:
    return (
        dateTime.strftime("%d/%m/%Y") if _DATETIME_ else dateTime.toString("dd/MM/yyyy")
    )


def DATE(dateTime: DateTime) -> str:
    return (
        dateTime.strftime("%H:%M:%S") if _DATETIME_ else dateTime.toString("HH:mm:ss")
    )


def EXISTS(manager, obj):
    return RESPONSE.EXIST if obj in manager else RESPONSE.EXTINCT


def ATTRS(object, attrs=[]):
    dict = object.__dict__
    res = []
    for at in attrs:
        res.append(dict.get(at))
    return res


def GENERATE_ID(column):
    id = "|".join([str(a) for a in column])
    # return id

    id_byt = id.encode()
    return B64_ENCODE(id_byt)

    id_digest = hashlib.sha224(id_byt).hexdigest()
    return id_digest


def GENERATE_ACTION_ID(tag):
    if tag.id:
        return

    raw_id = tag["action", "date_time", "type", "id"]

    dt = raw_id[1]
    if not isinstance(dt, int):
        raw_id[1] = str(DATETIME(dt))

    # everytime this function is called, this makes it give different id, no matter how identical the tag might be.
    raw_id.append(str(DATETIME()))

    tag.id = GENERATE_ID(raw_id)


def GENERATE_CHAT_ID(tag):
    if tag.id:
        return

    raw_id = tag["sender", "recipient", "date_time", "type", "chat"]

    dt = raw_id[2]
    if not isinstance(dt, int):
        raw_id[2] = str(DATETIME(dt))

    # everytime this function is called, this makes it give different id, no matter how identical the tag might be.
    raw_id.append(str(DATETIME()))

    tag.id = GENERATE_ID(raw_id)


def GENERATE_MEMBER_ID(tag, manager_id, manager_type):
    tag.unique_id = GENERATE_ID([tag.id, manager_id, manager_type])


def B64_ENCODE(data: bytes) -> str:
    encoded = base64.b64encode(data)
    str_decoded = encoded.decode()
    return str_decoded


def B64_DECODE(str_decoded: str) -> bytes:
    str_encoded = str_decoded.encode()
    data = base64.b64decode(str_encoded)
    return data


def GET_TYPE_ID(tag, name=False):
    id_names = {
        TYPE.USER: "user_id",
        TYPE.GROUP: "group_id",
        TYPE.CHANNEL: "channel_id",
    }

    id_name = id_names.get(tag.type)

    id = tag[id_name]

    if name:
        return id_name, id

    return id


class Mixin:
    @property
    def className(self):
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<{self}>"


class CONSTANT(Mixin):
    def __init__(self, name: str, objects: list = []):
        self._NAME = name.upper()
        self.OBJECTS = {}

        for obj in objects:
            self.add(obj)

    def add(self, obj):
        if isinstance(obj, str):
            obj = CONSTANT(obj)
        self.OBJECTS[obj._NAME] = obj

    def __len__(self):
        return len(self.OBJECTS)

    @property
    def list(self):
        return list(self.OBJECTS.values())

    def __str__(self):
        return self._NAME

    def __hash__(self):
        return hash(self._NAME)

    def __getitem__(self, name):
        if isinstance(name, (str, CONSTANT)):
            name = str(name).upper()
            f = self.__dict__.get(name)
            if f == None:
                f = self.OBJECTS.get(name)
            return f
        elif isinstance(name, (list, tuple)):
            litu = []
            for na in name:
                litu.append(self[na])
            return litu
        else:
            return self.list[name]

    __call__ = __getattr__ = __getitem__

    def __eq__(self, other):
        return str(other).upper() == self._NAME

    def __getstate__(self):
        return {"_NAME": self._NAME, "OBJECTS": list(self.OBJECTS.keys())}

    def __setstate__(self, state):
        self._NAME = state["_NAME"]
        self.OBJECTS = {}
        for k in state["OBJECTS"]:
            self.OBJECTS[k] = CONSTANT(k)

    def __bool__(self):
        return True


SOCKET = CONSTANT("SOCKET", objects=["ALIVE", "CLOSED", "RESET"])
SOCKET.ERRORS = SOCKET["CLOSED", "RESET"]

CHAT = CONSTANT("CHAT", objects=["AUDIO", "IMAGE", "TEXT", "VIDEO"])
CALL = CONSTANT("CALL", objects=["AUDIO", "VIDEO"])
STATUS = CONSTANT("STATUS", objects=["ONLINE", "OFFLINE"])

RESPONSE = CONSTANT(
    "RESPONSE",
    objects=[
        "ACCEPTED",
        "ADMIN_ONLY",
        "DECLINED",
        "EXIST",
        "EXTINCT",
        "FAILED",
        "FALSE_KEY",
        "LOGIN_FAILED",
        "SIMULTANEOUS_LOGIN",
        "SUCCESSFUL",
    ],
)
ID = CONSTANT("ID", objects=["CHANNEL_ID", "GROUP_ID", "USER_ID"])
TYPE = CONSTANT("TYPE", objects=["CHANNEL", "CONTACT", "USER", "GROUP"])
ACTION = CONSTANT(
    "ACTION",
    objects=[
        "ADD",
        "ADD_ADMIN",
        "ADD_MEMBER",
        CALL,
        "CALL_REQUEST",
        "CALL_RESPONSE",
        CHAT,
        "CREATE",
        "DELETE",
        "DATA",
        "CHANGE",
        "LOGIN",
        "LOGOUT",
        "ONLY_ADMIN",
        "REMOVE",
        "REMOVE_ADMIN",
        "REMOVE_MEMBER",
        "SIGNUP",
        STATUS,
    ],
)

TAG = CONSTANT(
    "TAG",
    objects=[
        ACTION,
        "ADMIN",
        "BIO",
        CALL,
        CHAT,
        "CHAT_COLOR",
        "CREATOR",
        "DATA",
        "DATE_TIME",
        "ICON",
        ID,
        "KEY",
        "MOBILE",
        "NAME",
        "RECIPIENT",
        RESPONSE,
        "RESPONSE_TO",
        "SENDER",
        STATUS,
        "TEXT",
        TYPE,
    ],
)


class Base(Mixin):
    def __init__(
        self,
        id: str,
        name: str = "",
        icon: str = "",
        date_time: DateTime = None,
        bio="",
    ):
        self.id = id
        self.name = name
        self.icon = icon
        self.bio = bio
        self.date_time = date_time or DATETIME(num=0)

    def get_name(self):
        return self.name or self.id

    def __str__(self):
        add = ""
        if self.name:
            add = f", name={self.name}"
        return f"{self.className}(id={self.id}{add})"

    @property
    def data(self):
        tag = Tag(
            name=self.name,
            id=self.id,
            icon=self.icon,
            bio=self.bio,
        )

        return tag

    def change_data(self, tag: "Tag"):
        name, icon, bio = tag["name", "icon", "bio"]
        if name:
            self.name = name
        if icon:
            self.icon = icon
        if bio:
            self.bio = bio


class Tag(Mixin, dict):
    DELIMITER = b"<TAG>"
    # upper() of kwargs is the default lookup

    # default values
    # action, type, id, text, chat

    def __init__(self, values={}, **kwargs) -> None:
        _dict = values.copy()
        _dict.update(kwargs)

        if not _dict.get("date_time"):
            _dict["date_time"] = DATETIME(num=0)

        _kwargs = {}

        for k, v in _dict.items():

            if k == "data":
                if isinstance(v, bytes):
                    v = B64_ENCODE(v)

            if k in TAG.list:  # k in TAG.objects
                k = TAG[k]
                if v in k.list:  # v in objects of one of the TAG's objects
                    v = k[v]

            elif k == TAG.ID:
                v = v.lower()

            elif k == TAG.DATE_TIME:
                v = DATETIME(v)

            elif isinstance(v, dict):
                v = Tag(v)

            elif isinstance(v, (list, tuple)):
                vals = []
                for v_ in v:
                    val = v_
                    if isinstance(v_, dict):
                        val = Tag(v_)
                    vals.append(val)
                v = tuple(vals)

            _kwargs[k] = v
            if isinstance(v, Base):
                _kwargs[k] = v.id

        dict.__init__(self, _kwargs)

    def __str__(self):
        return f"{self.className}({self.kwargs})"

    @property
    def dict(self) -> dict:
        _dict = {}
        for k, v in self.items():
            k = str(k)
            if isinstance(v, CONSTANT):
                v = str(v)
            elif isinstance(v, DateTime):
                v = DATETIME(v)
            elif isinstance(v, Tag):
                v = v.dict
            elif isinstance(v, tuple):
                vals = []
                for v_ in v:
                    val = v_
                    if isinstance(v_, Tag):
                        val = v_.dict
                    vals.append(val)
                v = tuple(vals)
            _dict[k] = v
        return _dict

    @property
    def encode(self):
        string = json.dumps(self.dict)
        encoded = string.encode() + self.DELIMITER
        return encoded

    @classmethod
    def decode_dict(cls, _dict):
        tag = cls(_dict)

        return tag

    @classmethod
    def decode(cls, data) -> dict:
        if (cls.DELIMITER) in data:
            data = data.replace(cls.DELIMITER, b"")
        if not data:
            data = b"{}"
        _dict = json.loads(data)
        return cls(**_dict)

    @classmethod
    def decodes(cls, data) -> list:
        decodes = data.split(cls.DELIMITER)
        tags = []

        for tag in decodes:
            if tag:
                tags.append(cls.decode(tag))

        return tags

    @property
    def kwargs(self) -> str:
        _str = ""
        for k, v in self.items():
            if v == "":
                v = '""'
            elif v == b"":
                v = b'""'
            _str += f"{k}={v}, "
        _str = "".join(_str[:-2])
        return _str

    def __getattr__(self, attr):
        d = self.get(attr)
        if d == None:
            d = self.get(attr.upper())
        if d == None:
            d = self.get(attr.lower())
        return d

    def __getitem__(self, attr):
        if isinstance(attr, tuple):
            tup = []
            for at in attr:
                t = self[str(at)]
                tup.append(t)
            return tup
        elif isinstance(attr, list):
            tup = {}
            for at in attr:
                t = self[str(at)]
                tup[at] = t
            return tup
        elif isinstance(attr, str):
            res = self.get(attr.upper())
            if res == None:
                res = self.get(attr.lower())
            return res

    def __setattr__(self, attr, val):
        self[attr.upper()] = val

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    def get_date_time(self):
        if isinstance(self.date_time, int):
            return DATETIME(self.date_time)
        return self.date_time

    def delete(self, attr):
        dict = self.dict
        if attr in dict:
            del dict[attr]
        elif attr.upper() in dict:
            del dict[attr.upper()]
        self.clear()
        self.update(dict)

    @property
    def raw_data(self):
        data = self.data
        if data:
            return B64_DECODE(data)

    @property
    def raw_icon(self):
        icon = self.icon
        if icon:
            return B64_DECODE(icon)


EMPTY_TAG = Tag()
EMPTY_TAGS = [EMPTY_TAG, []]


class _User_Base(Base):
    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)
        self._status = ""
        self.change_status(STATUS.OFFLINE)
        self.last_seen = None

    @property
    def data(self):
        tag = super().data
        tag.status = self.status

        return tag

    @property
    def status(self):
        return str(self._status)

    @property
    def current_status(self):
        if self.status == STATUS.ONLINE:
            return self.status
        else:
            return DATETIME(self.last_seen)

    @property
    def int_last_seen(self) -> int:
        return DATETIME(self.last_seen)

    @property
    def str_last_seen(self) -> str:
        if self.last_seen:
            return self.last_seen.toString(OFFLINE_FORMAT)

    def change_status(self, status) -> None:
        if status == STATUS.ONLINE:
            self._status = status
        else:
            self._status = STATUS.OFFLINE
            last = status if isinstance(status, int) else 0
            self.last_seen = DATETIME(last, num=0)

    def __getstate__(self):
        dic = self.__dict__.copy()
        dic["_status"] = STATUS.OFFLINE
        return dic


class _User(_User_Base):
    def __init__(self, key: str = "", **kwargs):
        _User_Base.__init__(self, **kwargs)
        self.key = key
        self.users = None
        self.groups = None
        self.channels = None

    def change_data(self, tag: Tag):
        super().change_data(tag)
        key = tag.key
        if key:
            self.key = key

    def add_user(self, user: _User_Base) -> None:
        self.users.add(user)

    def add_group(self, group: "Multi_Users") -> None:
        self.groups.add(group)

    def add_channel(self, channel: "Multi_Users") -> None:
        self.channels.add(channel)


class _Manager:
    def __init__(self, user: _User):
        self.user = user
        self._objects = {}
        self.get = self._objects.get

    def add(self, obj: _User_Base) -> None:
        if obj.id == self.user.id:
            return

        _obj = self.get(obj.id)
        if _obj == None:
            self._objects[obj.id] = obj

    def remove(self, id: str) -> None:
        obj: _User_Base = self.get(id)
        if obj:
            del self._objects[id]

    def add_chat(self, chat: Tag) -> None:
        obj = self.get(chat.recipient)
        if obj != None:
            obj.add_chat(chat)

    def __len__(self):
        return len(self._objects)

    @property
    def objects(self):
        return list(self._objects.values())

    @property
    def ids(self):
        return list(self._objects.keys())

    def __getitem__(self, name):
        if isinstance(name, str):
            f = self.__dict__.get(name)
            if f == None:
                f = self.__dict__["_objects"].get(name)
            return f
        # elif isinstance(name, (int, slice)): return self.list[name]
        elif isinstance(name, (list, tuple)):
            litu = []
            for na in name:
                litu.append(self[na])
            return litu

        elif isinstance(name, (int, slice)):
            return self.objects[name]


class Sock(Mixin):
    buffer_size = 1048576

    def __init__(self, socket: socket.socket = None):
        self.socket = socket or self
        self.state = SOCKET.CLOSED
        # self.shutdown = self.socket.shutdown

    @property
    def _alive(self) -> bool:
        return self.state == SOCKET.ALIVE

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
                except:
                    self.state = SOCKET.CLOSED
        return self.alive

    def _close(self) -> None:
        self.state = SOCKET.CLOSED
        try:
            self.socket.shutdown(0)
        except Exception as e:
            ...
        try:
            self.socket.close()
        except Exception as e:
            ...

    def catch(self, func):
        try:
            result = func()
            self.state = SOCKET.ALIVE
            return result

        except ConnectionResetError as e:
            # An existing connection was forcibly closed by the remote client.
            # The terminal of the client socket was terminated.] or closed.
            self.state = SOCKET.RESET
            return SOCKET.RESET

        except OSError as e:
            # An operation was attempted on something that is not a socket.
            # The client socket call close()
            self.state = SOCKET.CLOSED
            return SOCKET.CLOSED

    def read(self):
        return self.socket.recv(self.buffer_size)

    def recv_tag(self, many=False) -> Tag:
        fn = Tag.decodes if many else Tag.decode

        def func():
            encoded = self.read()
            if not encoded:
                raise IOError("pipe is empty, other channel has been disconnected!")
            tag = fn(encoded)
            return tag

        return self.catch(func)

    def recv_tags(self) -> List[Tag]:
        return self.recv_tag(many=True)

    def send_tag(self, tag: Tag) -> int:
        return self.catch(lambda: self.socket.send(tag.encode))

    @property
    def alive(self) -> bool:
        self.catch(lambda: self.socket.send(Tag.DELIMITER))
        return self._alive

    def sendall_tag(self, tag: Tag) -> int:
        def func():
            return self.socket.sendall(tag.encode)

        return self.catch(func)
