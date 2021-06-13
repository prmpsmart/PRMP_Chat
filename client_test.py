from prmp_chat.client import *
import random

dic = dict(id=f'EEE/18/6718_{random.random()}', name='Apata Miracle Peter', key='princerm')
print(dic)

user = Client_User(**dic)
client = Client(user=user)

client.signup(**dic)
# client.login()