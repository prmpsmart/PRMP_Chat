from prmp_sql.bases import Columns
from prmp_sql.database import DataBase
from prmp_sql.operators import EQUAL, CONSTANT
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
    GENERATE_TAG_ID,
    CONSTANT as core_CONSTANT,
    Tag,
)


class User_DB:
    path = os.path.join(os.path.dirname(__file__), "CLIENT_DATA.db")
    user_id = ""
    loaded_server_settings = False

    @staticmethod
    def column_names(columns):
        return [column.column for column in columns]

    def __init__(self):
        self.db = DataBase(self.path)
        self.db.init()
        self.user_details_columns = [
            VARCHAR("id"),
            VARCHAR("name"),
            BLOB("key"),
            BLOB("icon"),
            VARCHAR("description"),
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
            VARCHAR("description"),
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
            VARCHAR("member_id"),
            VARCHAR("name"),
            BLOB("icon"),
            VARCHAR("description"),
            VARCHAR("member_type"),
            BOOLEAN("admin"),
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
            *self.members_columns,
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
            self.load_user()

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
                where=WHERE_EQUAL("id", User_DB.user_id, parenthesis=0, constant=1),
            )
        else:
            statement = INSERT("user_details", values=VALUES(*values))

        User_DB.user_id = user.id
        self.db.exec(statement, dry=0, parameters=[v3], quiet=1)

        self.save_objects(user)
        self.db.commit()

    def load_user(self):
        statement = SELECT("*", "user_details")
        result = self.db.exec(statement, quiet=1)

        if result:
            result = result[0]

            columns = [a.column for a in self.user_details_columns]

            ints = columns[5:10]
            times = columns[-2:]

            details = dict(zip(columns[:5], result))
            ints = dict(zip(columns[5:10], result[5:10]))
            times = dict(zip(columns[-2:], result[-2:]))

            from prmp_chat.backend.client import User

            result = user = User(**details)
            user.recv_data = bool(ints["recv_data"])

            user.date_time = DATETIME(times["date_time"])
            user.last_seen = DATETIME(times["last_seen"])
            User_DB.user_id = user.id

            # TODO loading of the other contacts, groups, channels
            self.load_objects(user)
            self.load_chats(user)
            self.load_members(user)

        return result

    def save_objects(self, user):
        contacts = user.contacts
        contacts_datas = []
        for contact in contacts.objects:
            data = (
                contact.id,
                contact.name,
                contact.icon,
                contact.description,
                "contact",
                "",
                0,
            )
            contacts_datas.append(data)

        channels = user.channels
        channels_datas = []
        for channel in channels.objects:
            data = (
                channel.id,
                channel.name,
                channel.icon,
                channel.description,
                "channel",
                channel.creator,
                len(channel.users),
            )
            channels_datas.append(data)

        groups = user.groups
        groups_datas = []
        for group in groups.objects:
            data = (
                group.id,
                group.name,
                group.icon,
                group.description,
                "group",
                group.creator,
                len(group.users),
            )
            groups_datas.append(data)

        statement1 = INSERT("objects", values=MULTI_VALUES(*contacts_datas))
        statement2 = INSERT("objects", values=MULTI_VALUES(*channels_datas))
        statement3 = INSERT("objects", values=MULTI_VALUES(*groups_datas))

        statements = statement1, statement2, statement3

        for statement in statements:
            self.db.exec(statement)

    def load_objects(self, user):
        ...

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
                where=WHERE_EQUAL("chat_id", tag.id, constant=1),
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
            where=WHERE_EQUAL("chat_id", tag.id, constant=1),
        )

        self.db.exec(statement, quiet=1)
        self.db.commit()

    def load_chats(self, user):
        NAME = lambda n: n.OBJ.__name__

        contacts_chats_statement = SELECT(
            "*", "chats", WHERE_EQUAL("type", NAME(user.contacts))
        )

        results = self.db.exec(contacts_chats_statement, quiet=1)

        column_names = self.column_names(self.chats_columns)
        column_names[0] = "id"

        for result in results:
            dict_result = dict(zip(column_names, result))
            dict_result["sent"] = bool(dict_result["sent"])

            chat_tag = Tag(**dict_result)
            print(chat_tag)

    def load_members(self, user):
        ...

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
            where=WHERE_EQUAL("name", "server_settings", constant=1),
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
                where=WHERE_EQUAL("name", "server_settings", constant=1),
            )
        else:
            statement = INSERT(
                "other_settings", values=VALUES("server_settings", settings)
            )

        self.db.exec(statement, quiet=1)
        self.db.commit()
