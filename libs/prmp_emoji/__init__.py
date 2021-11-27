import json, os, re
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File

# courtesy of pypi.org/emoji_data_python
# courtesy of openmoji.com
# courtesy of github.org/emoji_data


def get_file(file):
    file_dir = os.path.dirname(__file__)
    file_path = os.path.join(file_dir, file)
    return file_path


def get_json(file):
    file = get_file(file)
    if not os.path.exists(file):
        return {}

    opened_file = open(file, "rb")
    load = json.load(opened_file)
    opened_file.close()
    return load


def create_json(js, file):
    opened_file = open(file, "wb")

    dumps = json.dumps(js, indent=2, ensure_ascii=False)
    dumps = dumps.encode()
    opened_file.write(dumps)
    opened_file.close()


def load_emoji(file):
    f = PRMP_File(get_file(file))
    obj = f.loadObj()
    return obj


def save_emoji(obj, file):
    f = PRMP_File(get_file(file))
    f.saveObj(obj)
    f.save()


class Base:
    def normalize_name(self, name):
        return name.lower().replace("-", "_").replace(" ", "_")

    def hexcode_to_emoji(self, code_point: str) -> str:
        split = code_point.split("-")
        ints = [int(code, 16) for code in split]
        chrs = [chr(intt) for intt in ints]
        char = "".join(chrs)
        return char

    def emoji_to_hexcode(self, chars: str) -> str:
        ords = [ord(char) for char in chars]
        strs = [f"{ordd: 04x}".upper() for ordd in ords]
        hexcode = "-".join(strs)
        return hexcode

    def __init__(self):
        self.__subs = {}

    @property
    def _subs(self):
        return self.__subs

    @property
    def subs(self):
        return list(self._subs.values())

    @property
    def subs_names(self):
        return list(self._subs.keys())

    @property
    def subs_count(self):
        return len(self._subs)

    def __repr__(self):
        return f"<{self}>"


class Common(Base):
    def __init__(self, master, name):
        Base.__init__(self)

        self.master = master
        self.name = self.normalize_name(name)

    def __str__(self):
        return f"{self.name}(master={self.master.name}, subs={self.subs_count})"

    @property
    def dict(self):
        dic = self.__dict__.copy()
        del dic["_Base__subs"], dic["master"]
        return dic


class Emoji_Base(Common):
    def __init__(self, master, name):
        Common.__init__(self, master, name)

        self.hexcode = ""
        self.non_qualified = ""
        self.image = ""
        self.sheet_x = 0
        self.sheet_y = 0
        self.annotation = ""
        self.skintone_combination = ""
        # self.need_nq = 0

    def __lt__(self, other):
        return self.hexcode < other.hexcode

    def __gt__(self, other):
        return self.hexcode >= other.hexcode

    def __le__(self, other):
        return self.hexcode <= other.hexcode

    def __ge__(self, other):
        return self.hexcode >= other.hexcode

    @property
    def emoji(self):
        return self.hexcode_to_emoji(self.hexcode)

    @property
    def png(self):
        return self.image.replace(".SVG", ".PNG")

    @property
    def svg(self):
        return self.image.replace(".PNG", ".SVG")

    @property
    def png2(self):
        return self.non_qualified + ".png"

    @property
    def svg2(self):
        return self.non_qualified + ".svg"


class Emoji_Variation(Emoji_Base):
    def __init__(self, master, data, prmp=""):
        Emoji_Base.__init__(self, master, master.name)

        if not prmp:
            self.skintone = 0
            self.hexcode = data.get("unified")
            self.non_qualified = data.get("non_qualified")
            self.sheet_x = data.get("sheet_x")
            self.sheet_y = data.get("sheet_y")
            self.image = data.get("image").upper()
        else:
            self.name = prmp
            self.__dict__.update(data)
            self.__dict__["image"] = self.__dict__["image"].upper()

    def __str__(self):
        return f"{self.name}_{self.skintone}(master={self.master.name}, subs={self.subs_count})"

    @property
    def subdict(self):
        dic = super().dict
        del dic["name"]
        dic["emoji"] = self.emoji
        return dic

    @property
    def dict(self):
        dic = self.subdict
        dic.update(super().dict)
        dic["emoji"] = self.emoji
        dic["base"] = self.master.name
        dic["subgroup"] = self.subgroup.name
        dic["group"] = self.group.name
        return dic

    @property
    def skintone_base_emoji(self):
        return self.master

    @property
    def skintone_base_hexcode(self):
        return self.master.hexcode

    @property
    def tags(self):
        return self.master.tags

    @property
    def subgroup(self):
        return self.master.subgroup

    @property
    def group(self):
        return self.subgroup.group

    def update_data(self, data):
        self.annotation = data.get("annotation")
        self.skintone = data.get("skintone")
        self.name = f"{self.name}_{self.skintone}"
        self.skintone_combination = data.get("skintone_combination")


class Emoji(Emoji_Base):
    def __init__(self, master, name, **kwargs):
        Emoji_Base.__init__(self, master, name)

        self.tags = []
        self.NAME = ""
        if kwargs:
            self.update_data(**kwargs)

    @property
    def all_variations(self):
        return [self.hexcode, *self.variations_hexcode]

    @property
    def is_doublebyte(self) -> bool:
        """`True` if emoji is coded on two or more bytes"""
        return "-" in self.hexcode

    @property
    def emojis(self):
        return list(map(self.hexcode_to_emoji, self.all_variations))

    @property
    def subdict(self):
        dic = super().dict
        del dic["name"]
        dic["emoji"] = self.emoji
        if self._variations:
            variations = {}
            for var in self.variations:
                variations[var.name] = var.subdict
            dic["variations"] = variations
        return dic

    @property
    def dict(self):
        dic = self.subdict
        dic.update(super().dict)
        dic["emoji"] = self.emoji
        if self._variations:
            variations = {}
            for var in self.variations:
                variations[var.name] = var.subdict
            dic["variations"] = variations
        dic["group"] = self.group.name
        dic["subgroup"] = self.subgroup.name
        return dic

    @property
    def _variations(self):
        return self._subs

    @property
    def variations(self):
        return self.subs

    @property
    def variations_names(self):
        return self.subs_names

    @property
    def variations_hexcode(self):
        return [var.hexcode for var in self.variations]

    def update_data(self, data, jsonfile):

        if jsonfile == "e":
            hexcode = data.get("unified")

            self.NAME = data.get("name").replace(" ", "_")
            self.hexcode = hexcode

            # grouping
            group = data.get("group")
            subgroup = data.get("subgroup")

            group = self.normalize_name(group)
            subgroup = self.normalize_name(subgroup)

            assert (
                group == self.group.name and subgroup == self.subgroup.name
            ), "Error group or subgroup is incorrect!"
            # grouping

            self.non_qualified = data.get("non_qualified")
            self.sheet_x = data.get("sheet_x")
            self.sheet_y = data.get("sheet_y")
            self.image = data.get("image").upper()

            self.tags = data.get("short_names")
            skin_variations = data.get("skin_variations")

            if skin_variations:
                for skin_variation in skin_variations.values():
                    sk_v = Emoji_Variation(self, skin_variation)
                    self._subs[skin_variation.get("unified")] = sk_v

        elif jsonfile == "o":
            hexcode = data.get("hexcode")
            skintone_base_hexcode = data.get("skintone_base_hexcode")
            if (skintone_base_hexcode != hexcode) and (
                skintone_base_hexcode in [self.hexcode, self.non_qualified]
            ):
                var = self._variations[hexcode]
                var.update_data(data)

            else:
                self.skintone_combination = data.get("skintone_combination")
                self.annotation = data.get("annotation")
                tags = data.get("tags") or ""
                openmoji_tags = data.get("openmoji_tags") or ""
                tags += openmoji_tags

                if tags:
                    self.tags.extend(tags.split(", "))
        else:
            del data["emoji"]
            vars = data.get("variations")
            if vars:
                del data["variations"]
            self.__dict__.update(data)
            self.__dict__["image"] = self.__dict__["image"].upper()

            if vars:
                for name, data in vars.items():
                    var = Emoji_Variation(self, data, name)
                    self._subs[name] = var

    @property
    def subgroup(self):
        return self.master

    @property
    def group(self):
        return self.subgroup.group


class Emoji_Sub_Group(Common):
    def __init__(self, master, name, data):
        Common.__init__(self, master, name)

        tr = isinstance(data, dict)

        for emoji_name in data:
            emoji_name = self.normalize_name(emoji_name)
            dat = dict(data=data[emoji_name], jsonfile="p") if tr else {}
            self._subs[emoji_name] = Emoji(self, emoji_name, **dat)

    @property
    def subdict(self):
        dic = super().dict
        del dic["name"]
        if self._emojis:
            for emoji in self.emojis:
                dic[emoji.name] = emoji.subdict
        return dic

    @property
    def dict(self):
        dic = self.subdict
        dic.update(super().dict)
        if self._emojis:
            for emoji in self.emojis:
                dic[emoji.name] = emoji.subdict
        dic["group"] = self.group.name

        return dic

    @property
    def group(self):
        return self.master

    @property
    def _emojis(self):
        return self._subs

    @property
    def emojis(self):
        return self.subs

    @property
    def emojis_names(self):
        return self.subs_names

    @property
    def emojis_count(self):
        return self.subs_count

    def get_emoji(self, name="", hexcode="", non_qualified=""):
        if name:
            name = self.normalize_name(name)
            if name in self.emojis_names:
                return self._emojis[name]

            for emoji in self.emojis_names:
                if name in emoji:
                    return self._emojis[emoji]

        elif hexcode:
            for emoji in self.emojis:
                if (hexcode in emoji.variations_hexcode) or (hexcode == emoji.hexcode):
                    return emoji
                # get variations

        elif non_qualified:
            for emoji in self.emojis:
                if non_qualified == emoji.non_qualified:
                    return emoji


class Emoji_Group(Common):
    def __init__(self, master, name, data):
        Common.__init__(self, master, name)

        for sub_group_name, sub_group_data in data.items():
            sub_group_name = self.normalize_name(sub_group_name)
            self._subs[sub_group_name] = Emoji_Sub_Group(
                self, sub_group_name, sub_group_data
            )

    @property
    def subdict(self):
        dic = super().dict
        del dic["name"]
        if self._subgroups:
            subgroups = {}
            for subgroup in self.subgroups:
                d = subgroup.subdict
                dic[subgroup.name] = d
                # subgroups.append(subgroup.dict)
            # dic['subgroups'] = subgroups
        return dic

    @property
    def dict(self):
        dic = self.subdict
        dic.update(super().dict)
        if self._subgroups:
            subgroups = {}
            for subgroup in self.subgroups:
                d = subgroup.subdict
                dic[subgroup.name] = d
                # subgroups.append(subgroup.dict)
            # dic['subgroups'] = subgroups
        return dic

    @property
    def _subgroups(self):
        return self._subs

    @property
    def subgroups(self):
        return self.subs

    @property
    def subgroups_names(self):
        return self.subs_names

    @property
    def subgroups_count(self):
        return self.subs_count

    @property
    def emojis_count(self):
        return sum([group.emojis_count for group in self.subgroups])

    @property
    def emojis(self):
        _emos = []
        for subgroup in self.subgroups:
            _emos.extend(subgroup.emojis)
        return _emos

    def get_subgroup(self, name, exact=0):
        name = self.normalize_name(name)
        if name in self.subgroups_names:
            return self._subgroups[name]

        for subgroup in self.subgroups_names:
            if exact:
                valid = name == subgroup
            else:
                valid = name in subgroup

            if valid:
                return self._subgroups[subgroup]

    def get_emoji(self, **kwargs):
        for subgroup in self.subgroups:
            emoji = subgroup.get_emoji(**kwargs)
            if emoji:
                return emoji


class Recent_Emoji:
    def __init__(self, max=30):
        self.emojis = []
        self.max = 30

    def __str__(self):
        return f"recent({len(self.emojis)})"

    def __repr__(self):
        return f"<{self}>"

    @property
    def name(self):
        return "recent"

    @property
    def hexcodes(self):
        return [em.hexcode for em in self.emojis]

    def add(self, emoji):
        all = self.emojis.copy()
        if emoji in all:
            all.remove(emoji)
        all.insert(0, emoji)

        self.emojis = all[: self.max]


class EMOJIS(Base):
    @property
    def name(self):
        return "EMOJIS"

    def __init__(self):
        Base.__init__(self)

        self.parse_jsons()
        self.emoji_names = {}
        for emoji in self.emojis:
            self.emoji_names[emoji.name] = emoji
            for tag in emoji.tags:
                if tag not in self.emoji_names:
                    self.emoji_names[tag] = emoji

    def __setstate__(self, dict):
        self.__dict__.update(dict)
        global PRMP_EMOJI_DICT
        if not PRMP_EMOJI_DICT:
            PRMP_EMOJI_DICT = json.dumps(self.dict)

    @property
    def dict(self):
        groups = {}
        for group in self.groups:
            d = group.dict
            del d["name"]
            groups[group.name] = d
        return groups

    @property
    def _groups(self):
        return self._subs

    @property
    def groups(self):
        return self.subs

    @property
    def groups_names(self):
        return self.subs_names

    @property
    def groups_count(self):
        return self.subs_count

    @property
    def subgroups_count(self):
        return sum([group.subgroups_count for group in self.groups])

    @property
    def emojis_count(self):
        return sum([group.emojis_count for group in self.groups])

    def get_group(self, name, exact=0):
        name = self.normalize_name(name)
        if name in self.groups_names:
            return self._groups[name]

        for group in self.groups_names:
            if exact:
                valid = name == group
            else:
                valid = name in group

            if valid:
                return self._groups[group]

    def get_subgroup(self, name, exact=0):
        for group in self.groups:
            subgroup = group.get_subgroup(name, exact=exact)
            if subgroup:
                return subgroup

    @property
    def emojis(self):
        _emojis = []
        for group in self.groups:
            for subgroup in group.subgroups:
                for emoji in subgroup.emojis:
                    _emojis.append(emoji)
                    _emojis.extend(emoji.variations)
        return _emojis

    def get_emoji(self, **kwargs):
        for group in self.groups:
            emoji = group.get_emoji(**kwargs)
            if emoji:
                return emoji

    def parse_jsons(self):
        if PRMP_EMOJI_DICT:
            for name, group in PRMP_EMOJI_DICT.items():
                self._subs[name] = Emoji_Group(self, name, group)

        elif EMOJI_GROUPS_DICT and OPENMOJI_DICT and EMOJI_PRETTY_DICT:
            for group_name, group_data in EMOJI_GROUPS_DICT.items():
                group_name = self.normalize_name(group_name)
                self._subs[group_name] = Emoji_Group(self, group_name, group_data)

            for emoji in EMOJI_PRETTY_DICT:
                _subgroup = emoji.get("subgroup")
                subg = self.get_subgroup(_subgroup, exact=1)
                emo: Emoji = subg.get_emoji(emoji.get("short_name"))
                emo.update_data(emoji, "e")

            emoo = i = v = 0
            for emoji in OPENMOJI_DICT:
                if "extra" in emoji.get("group"):
                    continue

                hexcode = emoji.get("hexcode")
                base_hexcode = emoji.get("skintone_base_hexcode")

                func = self.get_emoji

                emo: Emoji = (
                    func(hexcode=hexcode)
                    or func(non_qualified=hexcode)
                    or func(hexcode=base_hexcode)
                    or func(non_qualified=base_hexcode)
                )

                if emo:
                    emo.update_data(emoji, "o")

        save_emoji(self, "_prmp_emoji.obj")

    def to_json(self, file=""):
        if PRMP_EMOJI_DICT:
            return

        file = file or get_file("_prmp_emoji.json")
        create_json(self.dict, file)

    def get_emoji_regex(self):
        """Returns a regex to match any emoji

        >>> emoji_data_python.get_emoji_regex().findall('Hello world ! 👋🏼 🌍 ❗')
        ['👋', '🏼', '🌍', '❗']
        """
        # Sort emojis by length to make sure mulit-character emojis are
        # matched first

        emojis = sorted([emoji.char for emoji in self.emojis], key=len, reverse=True)
        pattern = "(" + "|".join(re.escape(u) for u in emojis) + ")"
        return re.compile(pattern)

    def replace_colons(self, text: str, strip: bool = False) -> str:
        """Parses a string with colon encoded emoji and renders found emoji.
        Unknown emoji are left as is unless `strip` is set to `True`

        :param text: String of text to parse and replace
        :param strip: Whether to strip unknown codes or to leave them as `:unknown:`

        >>> emoji_data_python.replace_colons('Hello world ! :wave::skin-tone-3: :earth_africa: :exclamation:')
        'Hello world ! 👋🏼 🌍 ❗'
        """
        # pylint: disable=import-outside-toplevel

        def emoji_repl(matchobj) -> str:
            emoji_match = matchobj.group(1)
            base_emoji = self.emoji_names.get(emoji_match.strip(":").replace("-", "_"))

            if matchobj.lastindex == 2:
                skin_tone_match = matchobj.group(2)
                skin_tone = self.emoji_names.get(skin_tone_match.strip(":"))

                if base_emoji is None:
                    return f'{emoji_match if strip is False else ""}{skin_tone.char}'

                emoji_with_skin_tone = base_emoji.skin_variations.get(skin_tone.unified)
                if emoji_with_skin_tone is None:
                    return f"{base_emoji.char}{skin_tone.char}"
                return emoji_with_skin_tone.char

            if base_emoji is None:
                return f'{emoji_match if strip is False else ""}'
            return base_emoji.char

        return re.sub(r"(\:[a-zA-Z0-9-_+]+\:)(\:skin-tone-[2-6]\:)?", emoji_repl, text)

    def all_doublebyte(self):
        """Returns all emoji coded on two or more bytes"""

        return [emoji for emoji in self.emojis if emoji.is_doublebyte]


# #####################################################
PRMP_EMOJI_DICT = EMOJI_GROUPS_DICT = OPENMOJI_DICT = EMOJI_PRETTY_DICT = {}
LOADED = load_emoji("_prmp_emoji.obj")

if not LOADED:
    PRMP_EMOJI_DICT = get_json("_prmp_emoji.json")
    if not PRMP_EMOJI_DICT:
        EMOJI_GROUPS_DICT = get_json("_groups.json")
        OPENMOJI_DICT = get_json("openmoji.json")
        EMOJI_PRETTY_DICT = get_json("emoji_pretty.json")
# #####################################################

EMOJIS = LOADED or EMOJIS()
