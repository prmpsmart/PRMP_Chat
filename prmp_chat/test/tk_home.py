
from tkinter.constants import *
from prmp_lib.prmp_gui.scrollables import Hierachy
from prmp_lib.prmp_gui.windows import *
from prmp_lib.prmp_gui.core_tk import *
from prmp_lib.prmp_gui.core_ttk import *
from prmp_lib.prmp_miscs.prmp_images import *
from prmp_lib.prmp_gui.image_widgets import PRMP_ImageSLabel, tk
from prmp_lib.prmp_gui.scrollables import *

# import lib.prmp_miscs
# from gui import Button, Frame, Tk, PRMP_Image, Label, Entry, PanedWindow


def _image(file, pre='imgs/', ex='@3x', ext='png', resize=(40, 40), **kwargs):
    pic = f'{pre}{file}{ex}.{ext}'
    img = PRMP_Image(pic, for_tk=1, resize=resize, **kwargs)
    return img


class Pic_Btn(Button):
    def __init__(self, master, image=None, resize=(20, 20), imgkwargs={}, **kwargs):
        imgkwargs['resize'] = resize
        if image: image = _image(image, **imgkwargs)
        self.imag = image
        super().__init__(master, image=image,  relief='raised', overrelief='flat', asLabel=0, activebackground='black', borderwidth=0, **kwargs)
    
    # def 


class Chat_Button(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, relief='groove', **kwargs)

        self.image = Pic_Btn(self, image='menu_add_account', place=dict(x=0, w=80, y=0, relh=1), resize=(80, 80))

        self.chat_name = Label(self, text='Name', relief='flat', anchor=W)

        self.chat_preview = Label(self, text='The last message from the chat', font=None, relief='flat', anchor='w')

        self.last_month = Label(self, text='May 2021', font=None, relief='flat')
        self.last_day = Label(self, text='10:45 AM', font=None, relief='flat')

        self.after(100, self.place_subs)
    
    def place_subs(self):
        self.image.imag = _image('menu_add_account', resize=(self.image.winfo_width(), self.image.winfo_height()))
        self.image['image'] = self.image.imag

        w = self.winfo_width()
        self.chat_name.place(x=80, y=0, w=w-143, relh=.6)
        self.chat_preview.place(x=80, rely=.6, w=w-143, relh=.4)

        self.last_month.place(x=w-63, y=0, w=60, relh=.6)
        self.last_day.place(x=w-63, rely=.6, w=60, relh=.4)


class Chat_Listing(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, relief='groove', background='pink', **kwargs)


class Chat_Room(Frame):
    def __init__(self, master, title='Chats', **kwargs):
        Frame.__init__(self, master, relief='flat', **kwargs)
        self._title = title
        self.is_room = False

        self.load_widgets()


    def load_widgets(self):
        self.header = Frame(self, place=dict(relx=0, rely=0, relw=1, relh=.06), relief='groove', bd=0)

        self.title = Label(self.header, text=self._title, font=dict(family='Times New Roman', weight='bold', size=20), compound='right', borderwidth=1, relief='flat')
        
        tit = self._title.lower() + '_'

        self.contacts_add = Pic_Btn(self.header, image='contacts_add', resize=(35, 40), imgkwargs=dict(name=tit+'contacts_add'))
        self.search = Pic_Btn(self.header, image='title_search', resize=(40, 40), imgkwargs=dict(name=tit+'title_search'))
        self.settings = Pic_Btn(self.header, image='settings', resize=(20, 40), imgkwargs=dict(name=tit+'settings'))

        r = 40
        self.footer = Frame(self, relief='flat', bd=0)

        self.links = Pic_Btn(self.footer, image='input_attach', place=dict(relx=0, y=0, w=40, relh=1), resize=(r, r), imgkwargs=dict(name=tit+'input_attach'))
        
        self.text = Text(self.footer, placeholder='Write something here to send.', relief='flat', font='')
        
        self.emojis = Pic_Btn(self.footer, image='emoji_people', resize=(r, r), imgkwargs=dict(name=tit+'emoji_people'))

        self.audio_text = Pic_Btn(self.footer, image='input_send', resize=(r, r), imgkwargs=dict(name=tit+'input_send'))
        
        # self.after(100, self.configure_imputs)
        self.after(200, self.configure_imputs)

        self.bind('<Configure>', self.configure_imputs)
        self.bind('<1>', self.toggle_room)
        # self.bind('<1>', lambda e: print(self.header.width))
    
    def configure_imputs(self, event=0):
        
        w = width = self.header.width

        if not self.is_room:
            self.title.set(self._title)
            self.footer.place_forget()

        else:
            # self.title['text'] = f'Specific {"".join(self._title[:-1])} Name'
            
            self.footer.place(relx=0, rely=.94, relw=1, relh=.06)
            self.audio_text.place(x=width-40, y=0, relh=1, w=40)
            width -= 42
            self.emojis.place(x=width-40, y=0, relh=1, w=40)
            width -= 42
            self.text.place(x=42, y=0, relh=1, w=width-42)

        self.settings.place(x=w-24, y=0, relh=1, w=20)
        w -= 26
        self.search.place(x=w-40, y=0, relh=1, w=40)
        w -= 42
        self.contacts_add.place(x=w-35, y=0, relh=1, w=35)
        w -= 35
        self.title.place(relx=0, rely=0, w=w, relh=1)
    
    def toggle_room(self, event=0):
        if self.is_room: self.is_room = False
        else: self.is_room = True
        self.configure_imputs()


class Home1(Tk):
    def __init__(self, geo=(1300, 750), themeIndex=10, **kwargs):
        Tk.__init__(self, asb=0, atb=0, tm=0, geo=geo, ntb=0, be=1, themeIndex=themeIndex, resize=(1, 1), alpha=1, **kwargs)

        self.container['relief'] = 'flat'

        fr = Frame(self.cont, place=dict(x=0, y=0, w=70, relh=1), background='red')
        
        Pic_Btn(fr, place=dict(x=10, y=5, w=45, h=35), background='red', image='dialogs_menus', compound='top', resize=(20, 20))

        w = geo[0] - 70


        pane = PanedWindow(self.cont, place=dict(x=70, y=0, w=w, relh=1), handlepad=3, handlesize=8, sashpad=1, sashwidth=3, sashrelief='flat', showhandle=0, orient='horizontal')

        w /= 3

        self.contact_pane = Chat_Room(pane, title='Chats')
        pane.add(self.contact_pane, width=w)

        self.group_pane = Chat_Room(pane, title='Groups')
        pane.add(self.group_pane, width=w)

        self.channel_pane = Chat_Room(pane, title='Channels')
        pane.add(self.channel_pane)


        self.start()


class Chat_Tree(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tree = PRMP_Treeview(self,  place=dict(relx=0, rely=0, relw=1, relh=1), config=dict(show='tree'))


class Tab_Pane(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.chats_tab = Chat_Tree(self, text='Contacts', place=dict(relx=0, rely=.4, relw=1, relh=.3))

        self.notify_tab = Chat_Tree(self, text='Notifications', place=dict(relx=0, rely=.7, relw=1, relh=.3))





class Home2(Tk):
    def __init__(self, geo=(1300, 750), themeIndex=10, **kwargs):
        Tk.__init__(self, asb=0, atb=0, tm=0, geo=geo, ntb=0, be=1, themeIndex=themeIndex, resize=(1, 1), alpha=1, **kwargs)

        self.container['relief'] = 'flat'

        fr = Frame(self.cont, place=dict(x=0, y=0, w=70, relh=1), background='red')
        
        Pic_Btn(fr, place=dict(x=10, y=5, w=45, h=35), background='red', image='dialogs_menus', compound='top', resize=(20, 20))

        w = geo[0] - 70


        pane = PanedWindow(self.cont, place=dict(x=70, y=0, w=w, relh=1), handlepad=3, handlesize=8, sashpad=1, sashwidth=3, sashrelief='flat', showhandle=0, orient='horizontal')

        w /= 3

        self.tab_pane = Tab_Pane(pane)
        pane.add(self.tab_pane, width=w)

        self.chat_room = Chat_Room(pane, title='Chats')
        pane.add(self.chat_room, width=w)

        # self.group_pane = Chat_Room(pane, title='Groups')
        # pane.add(self.group_pane, width=w)

        # self.channel_pane = Chat_Room(pane, title='Channels')
        # pane.add(self.channel_pane)


        self.start()






Home1()











