
from prmp_lib.prmp_gui.windows import *
from prmp_lib.prmp_gui.core_tk import *
# from prmp_lib.prmp_gui.core_ttk import *
from prmp_lib.prmp_miscs.prmp_images import *

# import lib.prmp_miscs
# from gui import Button, Frame, Tk, PRMP_Image, Label, Entry, PanedWindow


class Pic_Btn(Button):
    def __init__(self, master, image=None, resize=(20, 20), imgkwargs={}, **kwargs):
        imgkwargs['resize'] = resize
        if image: image = PRMP_Image(image, for_tk=1, **imgkwargs)
        Button.__init__(self, master, image=image,  relief='flat', overrelief='flat', **kwargs)
    
    # def 


class Chat_Listing(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)



class Chat_Room(Frame):
    def __init__(self, master, title='Chats', **kwargs):
        Frame.__init__(self, master, **kwargs)
        self._title = title
        self.is_room = False

        self.load_widgets()


    def load_widgets(self):
        self.header = Frame(self, place=dict(relx=0, rely=0, relw=1, relh=.06), relief='flat', bd=0)

        self.title = Label(self.header, text=self._title, font=dict(family='Times New Roman', weight='bold', size=20))


        self.footer = Frame(self, relief='flat', bd=0)

        self.links = Pic_Btn(self.footer, image='imgs/input_attach.png', place=dict(relx=0, y=0, w=40, relh=1), bd=0, resize=(40, 40))
        
        self.text = Text(self.footer, placeholder='Write something here to send.', bd=0, relief='flat', font='')
        
        self.emojis = Pic_Btn(self.footer, bd=0)

        self.audio_text = Pic_Btn(self.footer, bd=0)
        
        self.after(100, self.configure_imputs)
        self.bind('<Configure>', self.configure_imputs)
        self.bind('<1>', self.toggle_room)
    
    def configure_imputs(self, event=0):
        
        header_width = footer_width = self.header.width

        if self.is_room is False:
            self.title.place(relx=0, rely=0, relw=1, relh=1)
            self.footer.place_forget()

        else:
            self.title.place_forget()
            
            self.footer.place(relx=0, rely=.94, relw=1, relh=.06)
            self.audio_text.place(x=footer_width-40, y=0, relh=1, w=40)
            footer_width -= 42
            self.emojis.place(x=footer_width-40, y=0, relh=1, w=40)
            footer_width -= 42
            self.text.place(x=42, y=0, relh=1, w=footer_width-42)
    
    def toggle_room(self, event=0):
        if self.is_room: self.is_room = False
        else: self.is_room = True
        self.configure_imputs()





class Home(Tk):
    def __init__(self, geo=(1300, 750), themeIndex=53, **kwargs):
        Tk.__init__(self, asb=0, atb=0, tm=0, geo=geo, ntb=0, be=1, themeIndex=themeIndex, resize=(0, 0), alpha=1, **kwargs)

        self.container['relief'] = 'flat'

        fr = Frame(self.cont, place=dict(x=0, y=0, w=70, relh=1), background='red')
        
        Pic_Btn(fr, place=dict(x=10, y=5, w=45, h=35), background='red', image='imgs/dialogs_menu.png', compound='top')

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

Home()





