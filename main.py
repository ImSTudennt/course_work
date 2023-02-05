import vk_api
from random import randrange
# import requests
from vk_api.longpoll import VkLongPoll, VkEventType
# from bs4 import BeautifulSoup
from vk_bot import Vkbot
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

def write_msg(user_id, message=None, keyboard=None, attachment=None):
    post = {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)}
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    if attachment != None:
        post['attachment'] = attachment

    vk.method('messages.send', post)

with open(r'C:\Users\vladi\Desktop\project\key_api.txt', 'r') as f:
    token = f.read()

with open(r'C:\Users\vladi\Desktop\project\people.json', 'r', encoding='utf-8') as p:
    peoples = json.load(p)



settings = dict(one_time=False, inline=True)
settings_1 = dict(one_time=True, inline=False)
if __name__ == '__main__':

    vk = vk_api.VkApi(token=token)
    
    longpoll = VkLongPoll(vk)
    flag = True

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                text = event.text.lower()
                print('New message:')
                print(f'For me by: {event.user_id}', end=' ')

                
                bot = Vkbot(event.user_id)
                keyboard = VkKeyboard(**settings_1)
                keyboard_1 = VkKeyboard(**settings)
                while flag:
                    keyboard.add_button(label='Начать', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,'Для входа в приложение нажмите Начать', keyboard)
                    flag = False
                
                if event.text.upper() == 'НАЧАТЬ':
                    keyboard_1.add_button(label='Выйти', color=VkKeyboardColor.SECONDARY)
                    keyboard_1.add_line()
                    keyboard_1.add_button(label='Следующая', color=VkKeyboardColor.SECONDARY)
                    keyboard_1.add_line()
                    keyboard_1.add_button(label='Добавить в избранное', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,f'{peoples[0]["first_name"]} {peoples[0]["last_name"]}', keyboard_1, attachment=peoples[0]["photo"])
                    del peoples[0]
                elif event.text.upper() == 'ВЫЙТИ':
                    keyboard.add_button(label='Начать', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,'Для входа в приложение нажмите Начать', keyboard)
                elif event.text.upper() == 'СЛЕДУЮЩАЯ':
                    keyboard_1.add_button(label='Выйти', color=VkKeyboardColor.SECONDARY)
                    keyboard_1.add_line()
                    keyboard_1.add_button(label='Следующая', color=VkKeyboardColor.SECONDARY)
                    keyboard_1.add_line()
                    keyboard_1.add_button(label='Добавить в избранное', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,f'{peoples[0]["first_name"]} {peoples[0]["last_name"]}', keyboard_1, attachment=peoples[0]["photo"])
                    del peoples[0]

                    # keyboard_1.add_line()
                    # keyboard_1.add_button(label='Следующая', color=VkKeyboardColor.SECONDARY)
                    # keyboard_1.add_line()
                    # keyboard_1.add_button(label='Добавить в избранное', color=VkKeyboardColor.SECONDARY)
                    # write_msg(event.user_id,'Привет', keyboard)
                # else:
                #     write_msg(event.user_id, bot.new_message(event.text), keyboard)

                
                print('Text: ', event.text)
                # ['photo21263797_456240866', 'photo21263797_456239150']
        