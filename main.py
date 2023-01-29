import vk_api
from random import randrange
# import requests
from vk_api.longpoll import VkLongPoll, VkEventType
# from bs4 import BeautifulSoup
from vk_bot import Vkbot

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

with open(r'C:\Users\vladi\Desktop\project\key_api.txt', 'r') as f:
    token = f.read()

if __name__ == '__main__':

    vk = vk_api.VkApi(token=token)
    
    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                print('New message:')
                print(f'For me by: {event.user_id}', end=' ')
                
                bot = Vkbot(event.user_id)
                write_msg(event.user_id, bot.new_message(event.text))
                
                print('Text: ', event.text)
        