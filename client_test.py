from prmp_chat.backend.client import *
import random

# dic = dict(id=f'EEE/18/6718_{random.random()}', name='Apata Miracle Peter', key='princerm')
# dic = dict(id=f'EEE/18/6718', name='Apata Miracle Peter', key='princerm')
dic = dict(id=f'ade1', name='ade1', key='ade1')
# print(dic)

user = Client_User(**dic)
client = Client(user=user)

# client.signup()
client.login()
client.start_session()