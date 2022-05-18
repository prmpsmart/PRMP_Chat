from ..mimi_wave import *
from ..mimi_wave import _WaveApp, _WaveSender, _WaveReceiver, _WaveWidget
from tkinter import *
from tkinter.messagebox import showinfo


class WaveApp(_WaveApp, Tk):
    def __init__(self, windowClass: "_WaveWidget"):
        Tk.__init__(self)
        _WaveApp.__init__(self, windowClass)

    def start(self):
        # self.bind('WM_DELETE_PROTOCOL', self.window.destroy)
        self.window.place(x=0, y=0, relw=1, relh=1)
        self.mainloop()

    def destroy(self):
        self.closing()
        super().destroy()


class WaveWidgetCommon(Frame):
    klass = None

    def __init__(self, app: WaveApp, title="Wave Widget"):
        super().__init__(app)

        self.setup()

    def GEOMETRY(self, geo):
        self.app.geometry("%dx%d+%d+%d" % geo)

    def INFO(self, title, text):
        showinfo(title, text)

    def TITLE(self, title):
        self.app.title(title)

    def CONNECT(self, widget: Widget, func):
        widget.config(command=func)

    def SET_TEXT(self, widget: Widget, text):
        if hasattr(widget, "insert"):
            widget.insert("0", text)
        else:
            widget.config(text=text)

    def GET_TEXT(self, widget: Widget) -> str:
        return widget.get()

    def GET_INT(self, widget: Widget) -> int:
        value = widget.get()
        try:
            value = int(value)
            return value
        except:
            return 0

    def DISABLE(self, widget: Widget):
        widget["state"] = "disabled"

    def ENABLE(self, widget: Widget):
        widget["state"] = "normal"

    def setup(self, masters=[]):
        if masters:
            m1, m2, m3 = masters
        else:
            m1 = m2 = m3 = self

        self._frames_details = Label(m1, relief="sunken")
        self._play_recording = Button(m2)
        self._server_port = Spinbox(m3, from_=6000, to=9000)

    def destroy(self) -> None:
        self.klass.closing(self)
        return super().destroy()
