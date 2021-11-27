import os, emoji
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ..widgets import *
from libs.prmp_emoji import EMOJIS, Recent_Emoji


APPLE = "apple"
GOOGLE = "google"
FACEBOOK = "facebook"
TWITTER = "twitter"

_EMOJI_SPRITE_SHEET = (
    r"C:\Users\Administrator\Coding_Projects\Icons\Emojis\sprite_sheets\sheet_%s_64.png"
)

EMOJI_SPRITE_SHEET = lambda social: _EMOJI_SPRITE_SHEET % social

EMOJI_GROUPS_ICONS = {
    k: f":emoji_header/{v}.svg"
    for k, v in dict(
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
    ).items()
}


class Emoji_Sprite:
    @property
    def ww(self):
        return self.sprite_image.width() / 60

    @property
    def _ww(self):
        return self.sprite_image.width()

    @property
    def _hh(self):
        return self.sprite_image.height()

    @property
    def hh(self):
        return self.sprite_image.height() / 60

    def __init__(self, spritesheet):
        self.emojis = {}
        self.sprite_image = QPixmap(spritesheet)

        for emoji in EMOJIS.emojis:
            x, y = emoji.sheet_x, emoji.sheet_y
            x, y = x * self.ww, y * self.hh

            pixmap = self.sprite_image.copy(x, y, self.ww, self.hh)
            # pixmap.save('ll/'+emoji.png)
            self.emojis[emoji.hexcode] = pixmap

    def __getitem__(self, hexcode):
        return self.emojis[hexcode]


class Emoji_Group_Button(QPushButton):
    def __init__(self, group, callback):
        QPushButton.__init__(self)
        svg = EMOJI_GROUPS_ICONS[group.name]
        self._group = group
        self.setIconSize(QSize(30, 30))
        self.setIcon(QIcon(svg))
        self.setToolTip(group.name.title())
        self.setCheckable(True)
        self.clicked.connect(lambda: callback(group))

        self._pressed = False

    def choosen(self):
        self._pressed = True
        self.setStyleSheet("background: %s" % STYLE.LIGHT)

    def unchoosen(self):
        self._pressed = False
        self.leaveEvent(0)

    def enterEvent(self, event):
        if not self._pressed:
            self.setStyleSheet("background: %s" % STYLE.DARK_SHADE)

    def leaveEvent(self, event):
        if not self._pressed:
            self.setStyleSheet("")


class Emoji_Button(QPushButton):
    svg = ""

    _font = QFont()
    EMOJI_IMAGE = 1
    EMOJI_SPRITE = None

    @staticmethod
    def SET_SPRITE(social=APPLE):
        Emoji_Button.EMOJI_SPRITE = Emoji_Sprite(EMOJI_SPRITE_SHEET(social))

    def __init__(self, emoji, callback):
        QPushButton.__init__(self)
        self._emoji = emoji
        self.callback = callback
        self._image = self._icon = None

        size = 470 / 11

        found = 0
        if Emoji_Button.EMOJI_IMAGE == 1:
            self._image = Emoji_Button.EMOJI_SPRITE[self._emoji.hexcode]

        elif Emoji_Button.EMOJI_IMAGE == 2 and self.svg:
            svg = os.path.join(self.svg, emoji.svg)
            found = os.path.isfile(svg)

            if not found:
                svg = os.path.join(self.svg, emoji.svg2)
                found = os.path.isfile(svg)
            self._image = svg

        if self._image:
            self._icon = QIcon(self._image)
            self.setIcon(self._icon)

        else:
            self.setText(emoji.emoji)

        self.setToolTip(emoji.name.title())
        self.setMinimumHeight(size)
        self.setMinimumWidth(size)

    def enterEvent(self, event):
        self.setStyleSheet("background: %s" % STYLE.LIGHT_SHADE)

    def mouseReleaseEvent(self, e):
        self.leaveEvent(e)

    def mousePressEvent(self, e):
        self.setStyleSheet("background: %s" % STYLE.DARK)
        self.callback(self._emoji)

    def leaveEvent(self, event):
        self.setStyleSheet("")

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        s = min([w, h])

        if self._icon:
            s /= 1.3
            self.setIconSize(QSize(s, s))
        else:
            self._font.setPixelSize(s / 2)
            self.setFont(self._font)
            # self.setStyleSheet(f'font-size: {s/2}px')


class Emoji_Frame(QFrame):
    def __init__(self, layout):
        QFrame.__init__(self)
        self._layout = SETUP_FRAME(
            mother_layout=layout, orient="g", margins=[0, 0, 0, 20], obj=self
        )
        self._layout.setAlignment(Qt.AlignTop)
        self.set_style(self._style_colors)

        self.hide()
        self.setMinimumWidth(470)

    @property
    def _style_colors(self):
        return STYLE.DARK_SHADE

    def set_style(self, tup):
        self.setStyleSheet("background: %s" % tup)


class Emoji_Ui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(472)
        # self.setMaximumHeight(200)
        self.setMinimumHeight(500)
        self.setWindowFlag(Qt.Tool)

        layout = SETUP_FRAME(obj=self)  # , margins=[5, 5, 5, 5])

        groups_frame, groups_frame_layout = SETUP_FRAME(mother_layout=layout, re_obj=1)

        header_frame_layout = SETUP_FRAME(
            mother_layout=groups_frame_layout, orient="h", space=3
        )

        self.emoji_viewer = ScrolledWidget()
        self.emoji_viewer.set_bars_off()

        self.timer = QTimer()
        self.timer.timeout.connect(self.visi)

        # self.emoji_viewer.setMinimumHeight(233)

        layout.addWidget(groups_frame)
        layout.addWidget(self.emoji_viewer)

        self._emojis_frames_ = {}
        self.buttons_group = {}

        self._groups_ = [Recent_Emoji(60), *EMOJIS.groups]

        for group in self._groups_:
            button = Emoji_Group_Button(group, self.change_group)
            header_frame_layout.addWidget(button)

            self.buttons_group[group.name] = button

            self._emojis_frames_[group.name] = Emoji_Frame(self.emoji_viewer._layout)

    def showEvent(self, event):
        timer = QTimer()
        timer.timeout.connect(lambda: self.load_emojis(timer))
        timer.start(500)

    def load_emojis(self, timer):
        for group in self._groups_:
            layout = self._emojis_frames_[group.name]._layout
            self.arrange_emojis(group, layout)

        timer.stop()

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

        self.timer.start(50)

    def visi(self):
        self.emoji_viewer.ensureVisible(0, 0, 0, 0)
        self.timer.stop()

    def emoji_clicked(self, emoji):
        self._groups_[0].add(emoji)
        print(emoji)
        # print(self._groups_[0].emojis)
