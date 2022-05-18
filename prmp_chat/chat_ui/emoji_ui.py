import os
from .extras import *
from .prmp_emoji import EMOJIS, Emoji, Recent_Emoji, emoji


EMOJI_GROUPS_ICONS = dict(
    recent="clock",
    smileys_emotion="emoji-happy",
    people_body="user-group",
    component="chip",
    food_drink="cake",
    travel_places="globe",
    activities="camera",
    objects="bell",
    symbols="hashtag",
    flags="flag",
    animals_nature="bug",
)


class Emoji_Sprite:
    @property
    def ww(self):
        return self._ww / 60

    @property
    def _ww(self):
        return self.sprite_image.width()

    @property
    def _hh(self):
        return self.sprite_image.height()

    @property
    def hh(self):
        return self._hh / 60

    def __init__(self, spritesheet):
        self.emojis = {}
        self.sprite_image = QPixmap(spritesheet)

        for emoji in EMOJIS.emojis:
            x, y = emoji.sheet_x, emoji.sheet_y
            x, y = x * self.ww, y * self.hh

            pixmap = self.sprite_image.copy(x, y, self.ww, self.hh)
            self.emojis[emoji.hexcode] = pixmap

    def __getitem__(self, hexcode):
        return self.emojis[hexcode]


class Emoji_Group_Button(QPushButton):
    _size = QSize(30, 30)

    def __init__(self, group, callback):
        QPushButton.__init__(self)
        svg = EMOJI_GROUPS_ICONS[group.name]
        self._group = group
        self.setIconSize(self._size)
        self.setIcon(QIcon(f":emoji_headers/{svg}.svg"))
        self.setToolTip(group.name.title())
        self.setCheckable(True)
        self.clicked.connect(lambda: callback(group))

        self._pressed = False

    def choosen(self):
        self._pressed = True
        # self.setStyleSheet("background: %s" % STYLE.LIGHT)

    def unchoosen(self):
        self._pressed = False
        self.leaveEvent(0)

    def enterEvent(self, event):
        if not self._pressed:
            # self.setStyleSheet("background: %s" % STYLE.DARK_SHADE)
            ...

    def leaveEvent(self, event):
        if not self._pressed:
            self.setStyleSheet("")


class Emoji_Button(QPushButton):
    # _font = QFont()
    USE_IMAGE = 1

    def __init__(self, emoji, callback):
        QPushButton.__init__(self)
        self._emoji = emoji
        self.callback = callback
        self._pixmap = self._icon = None

        size = 450 / 11

        found = 0

        if self.USE_IMAGE:
            self._pixmap = QPixmap(f":emoji_icons/{self._emoji.hexcode}.png")
            self._icon = QIcon(self._pixmap)
            self.setIcon(self._icon)

        else:
            self.setText(emoji.emoji)

        self.setToolTip(emoji.name.title())
        self.setMinimumHeight(size)
        self.setMinimumWidth(size)

    def enterEvent(self, event):
        # self.setStyleSheet("background: %s" % STYLE.LIGHT_SHADE)
        ...

    def mouseReleaseEvent(self, e):
        self.leaveEvent(e)

    def mousePressEvent(self, e):
        # self.setStyleSheet("background: %s" % STYLE.DARK)
        self.callback(self._emoji)

    def leaveEvent(self, event):
        self.setStyleSheet("")

    def resizeEvent(self, event):
        s = min(self.size().toTuple())

        if self._icon:
            s /= 1.3
            self.setIconSize(QSize(s, s))
        else:
            # self._font.setPixelSize(s / 2)
            # self.setFont(self._font)
            self.setStyleSheet(f"font-size: {s/2}px")


class Emoji_Group(QFrame):
    def __init__(self, layout):
        QFrame.__init__(self)
        self._layout = SETUP_FRAME(
            mother_layout=layout, orient="g", margins=[0, 0, 0, 20], obj=self
        )
        self._layout.setAlignment(Qt.AlignTop)
        self.set_style(self._style_colors)

        self.hide()
        # self.setMinimumWidth(470)

    @property
    def _style_colors(self):
        # return STYLE.DARK_SHADE
        ...

    def set_style(self, tup):
        self.setStyleSheet("background: %s" % tup)


class Emoji(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.chat_tab: "ChatTab" = parent

        self.setMinimumHeight(200)
        self.setWindowTitle("Emoji Picker")

        layout = SETUP_FRAME(obj=self)

        groups_frame, groups_frame_layout = SETUP_FRAME(mother_layout=layout, re_obj=1)

        header_frame_layout = SETUP_FRAME(
            mother_layout=groups_frame_layout, orient="h", space=3
        )

        self.emoji_viewer = ScrolledWidget()
        self.emoji_viewer.set_bars_off()

        self.loaded = False

        layout.addWidget(groups_frame)
        layout.addWidget(self.emoji_viewer)

        self._emojis_frames_ = {}
        self.buttons_group = {}

        self._groups_ = [Recent_Emoji(60), *EMOJIS.groups]

        for group in self._groups_:
            button = Emoji_Group_Button(group, self.change_group)
            header_frame_layout.addWidget(button)

            self.buttons_group[group.name] = button

            self._emojis_frames_[group.name] = Emoji_Group(self.emoji_viewer._layout)

    def showEvent(self, event):
        QTimer.singleShot(100, lambda: self.load_emojis())

    def load_emojis(self):
        if not self.loaded:
            for group in self._groups_:
                layout = self._emojis_frames_[group.name]._layout
                self.arrange_emojis(group, layout)
            self.loaded = True

    def arrange_emojis(self, group, layout, sort=1):
        if sort:
            emojis = sorted(group.emojis)
        else:
            emojis = group.emojis

        column = 0
        for index, emoji in enumerate(emojis):
            button = Emoji_Button(emoji, self.emoji_clicked)

            row = index % 11
            if index and not row:
                row = 0
                column += 1
            layout.addWidget(button, column, row)

    def change_group(self, group):
        n = group.name
        for name, frame in self._emojis_frames_.items():
            button = self.buttons_group[name]
            if n == name:
                frame.show()
                button.choosen()
            else:
                frame.hide()
                button.unchoosen()

        if group.name == "recent":
            frame = self._emojis_frames_["recent"]
            grid = frame.layout()
            grid.setAlignment(Qt.AlignTop)
            self.arrange_emojis(group, grid, 0)
            frame.setLayout(grid)

        QTimer.singleShot(50, lambda: self.emoji_viewer.ensureVisible(0, 0, 0, 0))

    def emoji_clicked(self, emoji: Emoji):
        self._groups_[0].add(emoji)

        if self.chat_tab.current:
            footer = self.chat_tab.current.footer
            footer.add_emoji(emoji)

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.chat_tab.emoji_closed()
        return super().closeEvent(arg__1)
