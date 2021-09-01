from tkinter.constants import BOTTOM
from prmp_lib.prmp_gui import *
from prmp_lib.prmp_gui.dialogs import PRMP_Dialog, PRMP_MessageDialog
from prmp_lib.prmp_gui.two_widgets import *
from prmp_chat.backend.client import *


class Form(PRMP_FillWidgets, PRMP_Frame):
    def __init__(self, master, action, log=0, **kwargs):
        PRMP_Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)

        y = .05
        res = ['username', 'password']
        
        if log: self.text = 'Login'
        else:
            self.name = LabelEntry(self, place=dict(relx=.05, rely=y, relh=.2, relw=.9), topKwargs=dict(text='Name'), orient='h', longent=.38, bottomKwargs=dict(required=1))
            self.text = 'Signup'
            y += .2
            res = ['name'] + res

        self.username = LabelEntry(self, place=dict(relx=.05, rely=y, relh=.2, relw=.9), topKwargs=dict(text='Username'), orient='h', longent=.38, bottomKwargs=dict(required=1))
        y += .2
        self.password = LabelEntry(self, place=dict(relx=.05, rely=y, relh=.2, relw=.9), topKwargs=dict(text='Password'), orient='h', longent=.38, bottomKwargs=dict(required=1))

        self._action = action

        PRMP_Button(self, command=self.action, text=self.text, place=dict(relx=.05, rely=.7, relh=.2, relw=.9))

        self.addResultsWidgets(res)
    
    def action(self): self._action(self.get())


class StartUp(PRMP_Frame):

    def __init__(self, master, client=None, callback=None, **kwargs):
        super().__init__(master, **kwargs)
        note = PRMP_Notebook(self, place=dict(x=0, y=0, relw=1, relh=1))
        login = Form(note, self.login, log=1)
        note.add(login, text=login.text)
        signup = Form(note, self.signup)
        note.add(signup, text=signup.text)
        self.client = client
        self.callback = callback
    
    def normalize(self, details):
        key = details['password']
        id = details['username']
        g = dict(key=key, id=id)
        if 'name' in details: g['name'] = details['name']
        return g

    def login(self, details):
        response = self.client.login(**self.normalize(details))
        self.callback(response)
        PRMP_MessageDialog(self, title='LOGIN RESPONSE', message=str(response), delay=1000)

    def signup(self, details):
        response = self.client.signup(**self.normalize(details))
        self.callback(response)
        PRMP_MessageDialog(self, title='LOGIN RESPONSE', message=str(response), delay=1000)


class Peach(PRMP_MainWindow):

    def __init__(self, master=None, user=None, _ttk_=False, **kwargs):
        super().__init__(master=master, _ttk_=_ttk_, geo=(300, 700), be=1, **kwargs)
        self.client = Client(user=user, LOG=self.log)
        
        # self.startup = StartUp(self.cont, client=self.client, place=dict(relx=0, rely=0, relw=1, relh=.4), callback=self.startup_response)
        
        self.setup()
        self.start()
    
    def log(self, kwargs):
        # print(kwargs)
        ...

    def startup_response(self, response):
        
        if response == RESPONSE.SUCCESSFUL:
            self.startup.destroy()
            self.setup()
    
    def setup(self):
        self.receiver = LabelEntry(self.cont, place=dict(relx=.01, rely=.005, relw=.98, relh=.07), orient='h', topKwargs=dict(text='Receiver'), longent=.3)
        self.textViewer = PRMP_Text(self.cont, place=dict(relx=.01, rely=.085, relw=.98, relh=.72), state='disabled')

        self.text = PRMP_Text(self.cont, place=dict(relx=.01, rely=.81, relw=.8, relh=.18))
        PRMP_Button(self.cont, place=dict(relx=.82, rely=.9, relw=.17, relh=.05), text='Send', command=self.send)

    def send(self):
        text = self.text.get()

        self.textViewer.state('normal')
        self.textViewer.insert_end('Me: '+text+'\n\n')
        self.textViewer.state('disabled')
    
    def receive(self, tag):
        ...





Peach(themeIndex=51)







