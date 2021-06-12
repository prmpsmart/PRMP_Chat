from prmp_chat.client import *

dic = dict(id='EEE/18/6718', name='Apata Miracle Peter', key='princerm')

user = Client_User(**dic)
client = Client(user=user)

client.signup(**dic)
# client.login()