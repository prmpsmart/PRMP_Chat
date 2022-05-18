from prmp_sql.bases import Columns
from prmp_sql.database import DataBase
from prmp_sql.operators import AND, EQUAL, CONSTANT
from prmp_sql.shortcuts import WHERE_EQUAL
from prmp_sql.statements import (
    SELECT,
    INSERT,
    CREATE_TABLE,
    Column,
    UPDATE,
    WHERE,
    VALUES,
    MULTI_VALUES,
)
from prmp_sql.constraints import UNIQUE
from prmp_sql.clauses import SET
from prmp_sql.datatypes import *

import os

from .core import (
    DateTime,
    ATTRS,
    DATETIME,
    GENERATE_MEMBER_ID,
    CONSTANT as core_CONSTANT,
    Tag,
)


class User_DB:
    path = os.path.join(os.path.dirname(__file__), "CLIENT_DATA.db")
    user_id = ""
    loaded_server_settings = False

    # @property
    # def path(self):
    #     return os.path.join(os.path.dirname(__file__), f"CLIENT_DATA-{self.user.id}.db")

    @staticmethod
    def column_names(columns):
        return [column.column for column in columns]

    def __init__(self, user=None):
        self.user = user
        self.db = DataBase(self.path)
        self.db.init()
        self.user_details_columns = [
            VARCHAR("id"),
            VARCHAR("name"),
            BLOB("key"),
            BLOB("icon"),
            VARCHAR("bio"),
            BOOLEAN("recv_data"),
            INT("contacts"),
            INT("groups"),
            INT("channels"),
            INT("unsents"),
            INT("date_time"),
            INT("last_seen"),
        ]

        self.objects_columns = [
            VARCHAR("object_id"),
            VARCHAR("name"),
            BLOB("icon"),
            VARCHAR("bio"),
            VARCHAR("object_type"),
            VARCHAR("creator"),
            INT("total_members"),
        ]
        self.chats_columns = [
            VARCHAR("chat_id"),
            VARCHAR("sender"),
            VARCHAR("recipient"),
            INT("date_time"),
            VARCHAR("type"),
            VARCHAR("chat"),
            VARCHAR("text"),
            BLOB("data"),
            BOOLEAN("sent"),
            VARCHAR("path"),
        ]
        self.members_columns = [
            VARCHAR("unique_id"),
            VARCHAR("member_id"),
            VARCHAR("name"),
            BLOB("icon"),
            VARCHAR("bio"),
            BOOLEAN("admin"),
            VARCHAR("manager_id"),
            VARCHAR("manager_type"),
            BOOLEAN("is_contact"),
        ]

        self.other_settings_columns = [VARCHAR("name"), VARCHAR("settings")]

        self.create_tables()

    def create_tables(self):
        user_details = CREATE_TABLE(
            "user_details",
            UNIQUE(self.user_details_columns[0]),
            *self.user_details_columns[1:],
            check_exist=True,
        )
        objects = CREATE_TABLE(
            "objects",
            UNIQUE(self.objects_columns[0]),
            *self.objects_columns[1:],
            check_exist=True,
        )
        chats = CREATE_TABLE(
            "chats",
            UNIQUE(self.chats_columns[0]),
            *self.chats_columns[1:],
            check_exist=True,
        )
        members = CREATE_TABLE(
            "members",
            UNIQUE(self.members_columns[0]),
            *self.members_columns[1:],
            check_exist=True,
        )
        other_settings = CREATE_TABLE(
            "other_settings",
            UNIQUE(self.other_settings_columns[0]),
            *self.other_settings_columns[1:],
            check_exist=True,
        )

        tables = user_details, chats, members, objects, other_settings
        for table in tables:
            self.db.exec(table, quiet=1)
        self.db.commit()

    def save_user(self, user):
        if User_DB.user_id != user.id:
            self.load_user(just_id=1)

        columns = self.column_names(self.user_details_columns)

        values = ATTRS(
            user,
            attrs=columns[:6],
        )

        int_values = [
            len(a)
            for a in ATTRS(
                user,
                attrs=columns[6:10],
            )
        ]

        int_values.extend(
            [
                DATETIME(a)
                for a in ATTRS(
                    user,
                    attrs=columns[-2:],
                )
            ]
        )
        values.extend(int_values)

        v3 = values[3]

        # exit()
        values = [CONSTANT(a) for a in values]
        values[3] = Column("?")

        where = None

        if User_DB.user_id:
            multi_values = list(zip(columns, values))
            statement = UPDATE(
                "user_details",
                SET(*multi_values),
                where=WHERE_EQUAL("id", User_DB.user_id),
            )
        else:
            statement = INSERT("user_details", values=VALUES(*values))

        User_DB.user_id = user.id
        self.db.exec(statement, dry=0, parameters=[v3], quiet=1)

        self.save_objects(user)
        self.save_members(user)
        self.db.commit()

    def load_user(self, just_id=False):
        statement = SELECT("*", "user_details")
        result = self.db.exec(statement, quiet=1)

        if result and isinstance(result, list):
            result = result[0]

            columns = [a.column for a in self.user_details_columns]

            ints = columns[5:10]
            times = columns[-2:]

            details = dict(zip(columns[:5], result))
            ints = dict(zip(columns[5:10], result[5:10]))
            times = dict(zip(columns[-2:], result[-2:]))

            from backend.client import User

            result = user = User(**details)
            user.recv_data = bool(ints["recv_data"])

            user.date_time = DATETIME(times["date_time"])
            user.last_seen = DATETIME(times["last_seen"])
            User_DB.user_id = user.id

            # TODO loading of the other contacts, groups, channels
            if not just_id:
                self.load_objects(user)
                self.load_chats(user)

        return result

    def save_objects(self, user):
        for type_ in ["contact", "channel", "group"]:
            manager = getattr(user, type_ + "s")
            types_datas = []
            for member_manager in manager.objects:
                data = (
                    member_manager.id,
                    member_manager.name,
                    member_manager.icon,
                    member_manager.bio,
                    type_,
                    getattr(user, "creator", ""),
                    getattr(user, "objects", 0),
                )
                types_datas.append(data)

            statement = INSERT("objects", values=MULTI_VALUES(*types_datas))
            r = self.db.exec(statement, quiet=1)
            print(r)

    def load_objects(self, user):
        for object_type in ["contact", "group", "channel"]:
            statement = SELECT(
                "*", "objects", where=WHERE_EQUAL("object_type", object_type)
            )
            results = self.db.exec(statement, quiet=1)

            if isinstance(results, list):

                from .client import Manager

                manager: Manager = getattr(user, object_type + "s")
                OBJ = manager.OBJ

                column_names = self.column_names(self.objects_columns)
                column_names[0] = "id"

                for result in results:
                    tag = Tag(dict(zip(column_names, result)))

                    needed_tag = Tag(tag[["id", "name", "icon", "bio", "creator"]])

                    if object_type != "contact":
                        needed_tag.users = self.load_members(
                            needed_tag.id, OBJ.__name__
                        )

                    obj = OBJ(user, needed_tag)
                    manager.add(obj)

    def add_chat(self, tag):
        columns_names = self.column_names(self.chats_columns)

        columns_names[0] = "id"
        columns_values = tag[tuple(columns_names)]

        columns_names = self.column_names(self.chats_columns)

        sorted_columns_values = []
        for cn in columns_values:
            v = cn
            if isinstance(cn, core_CONSTANT):
                v = str(cn)
            elif isinstance(cn, DateTime):
                v = DATETIME(cn)
            elif cn == None:
                v = ""
            sorted_columns_values.append(v)

        statement = INSERT("chats", values=VALUES(*sorted_columns_values))

        res = self.db.exec(statement, quiet=1)
        if "UNIQUE constraint failed" in res:
            statement = UPDATE(
                "chats",
                set=SET(*sorted_columns_values[1:], columns=columns_names[1:]),
                where=WHERE_EQUAL("chat_id", tag.id),
            )

            self.db.exec(statement, quiet=1)

        self.db.commit()

    def chat_sent(self, tag):
        sent = tag.sent

        if not sent:
            return

        statement = UPDATE(
            "chats",
            set=SET(("sent", sent)),
            where=WHERE_EQUAL("chat_id", tag.id),
        )

        self.db.exec(statement, quiet=1)
        self.db.commit()

    def load_chats(self, user):

        contacts_chats_statement = SELECT("*", "chats")

        results = self.db.exec(contacts_chats_statement, quiet=1)

        column_names = self.column_names(self.chats_columns)
        column_names[0] = "id"

        for result in results:
            dict_result = dict(zip(column_names, result))
            dict_result["sent"] = bool(dict_result["sent"])

            chat_tag = Tag(**dict_result)
            sender, recipient = chat_tag["sender", "recipient"]

            user.add_chat(chat_tag, saved=1)

    def save_members(self, user):
        values = []

        def get_values(member_manager):
            columns = self.column_names(self.members_columns)

            _values = []

            for member in member_manager.objects:
                GENERATE_MEMBER_ID(
                    member,
                    member_manager.id,
                    member_manager.className,
                )
                id = member.id
                col_name = member["unique_id", "id", "admin"]

                contact = (id in member_manager.user.contacts.ids) or (
                    id == member_manager.user.id
                )
                if not contact:
                    new_col = member["name", "icon", "bio"]
                else:
                    new_col = ["", "", ""]

                col_name[2:2] = new_col

                col_name.extend([member_manager.id, member_manager.className, contact])

                _values.append(tuple(col_name))
            return _values

        for manager in [user.channels, user.groups]:
            for member_manager in manager:
                values.extend(get_values(member_manager))

        statement = INSERT("members", values=MULTI_VALUES(*values))

        r = self.db.exec(statement, quiet=1)
        print(r)

    def load_members(self, manager_id, manager_type):
        and_ = AND(
            EQUAL("manager_id", CONSTANT(manager_id)),
            EQUAL("manager_type", CONSTANT(manager_type)),
        )
        and_.parenthesis = False

        statement = SELECT(
            "*",
            "members",
            where=WHERE_EQUAL("manager_id", manager_id),
        )

        results = self.db.exec(statement, quiet=1)
        columns = self.column_names(self.members_columns)

        col_names = columns[:6]
        col_names[1] = "id"

        tags = []

        for result in results:
            tag = Tag(dict(zip(col_names, result[:6])))
            tag.admin = bool(tag.admin)
            tags.append(tag)

        return tags

    def add_user(self, user):
        print(user, self)

    def add_group(self, group):
        ...

    def add_channel(self, channel):
        ...

    def load_server_settings(self):
        statement = SELECT(
            "settings",
            "other_settings",
            where=WHERE_EQUAL("name", "server_settings"),
        )

        result = self.db.exec(statement, quiet=1) or {}

        if result:
            result = result[0][0]
            result = dict(zip(["ip", "port"], result.split(";")))
            result["port"] = int(result["port"])

        User_DB.loaded_server_settings = True
        return result

    def save_server_settings(self, ip, port):
        settings = CONSTANT(f"{ip};{port}")
        if User_DB.loaded_server_settings:
            statement = UPDATE(
                "other_settings",
                SET(("settings", settings)),
                where=WHERE_EQUAL("name", "server_settings"),
            )
        else:
            statement = INSERT(
                "other_settings", values=VALUES("server_settings", settings)
            )

        self.db.exec(statement, quiet=1)
        self.db.commit()
