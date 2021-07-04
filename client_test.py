from prmp_chat.backend.client import *
import random

# dic = dict(id=f'EEE/18/6718_{random.random()}', name='Apata Miracle Peter', key='princerm')
# dic = dict(id=f'EEE/18/6718', name='Apata Miracle Peter', key='princerm')

n = 'ade1'
# n = 'ade'+input()

dic = dict(id=n, name=n, key=n)

user = User(**dic)
client = Client(user=user, relogin=0)

# client.signup()
# r = client.login()
r = client.re_login()
if r == RESPONSE.SUCCESSFUL: client.start_session()