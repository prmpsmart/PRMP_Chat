import os, time

d = r'C:\Users\Administrator\Coding_Projects\C_C++\Qt\from_designer'


for a in os.listdir(d)[2:]:
    f = os.path.join(d, a)
    g, e = os.path.splitext(a)
    if e != '.ui': continue
    g = g+'.py'
    os.system(f'PySide6-uic {f} -o {g}')
    # break

f = 'home.py'

extra = r'''
import sys
sys.path.append(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\PRMP_Chat\prmp_chat\ui')
from chatList import ChatList, ChatRoomList

'''

lines = open(f).readlines()
new_lines = extra.split('\r\n')


a = '        self.chatList = QListView'
b = '        self.chatRoomList = QListView'

for index, line in enumerate(lines):

    if a in line: line = line.replace('QListView', 'ChatList')
    elif b in line: line = line.replace('QListView', 'ChatRoomList')

    new_lines.append(line)


open(f, 'w').writelines(new_lines)








