import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot import Vk_user
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bd import UsersBd
import random

def write_msg(user_id, message=None, keyboard=None, attachment=None):
    post = {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)}
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    if attachment != None:
        post['attachment'] = attachment

    vk.method('messages.send', post)

def key_b(keyb):

    keyb.add_button(label='Выйти', color=VkKeyboardColor.SECONDARY)
    keyb.add_line()
    keyb.add_button(label='Следующая', color=VkKeyboardColor.SECONDARY)
    keyb.add_line()
    keyb.add_button(label='Добавить в избранное', color=VkKeyboardColor.SECONDARY)
    keyb.add_line()
    keyb.add_button(label='Мои избранные', color=VkKeyboardColor.SECONDARY)


with open(r'C:\Users\vladi\Desktop\project\key_api.txt', 'r') as f:
    token = f.read()


token_1 = "..." # Токен админа чат бота 

settings_1 = dict(one_time=False, inline=True)
settings = dict(one_time=True, inline=False)

if __name__ == '__main__':

    vk = vk_api.VkApi(token=token)
    vk_1 = vk_api.VkApi(token=token_1)
    longpoll = VkLongPoll(vk)
    flag = True
    flag_1 = True

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                while flag_1:
                    bot = Vk_user(event.user_id, vk_1, token_1)
                    flag_1 = False

                keyboard = VkKeyboard(**settings)
                keyboard_1 = VkKeyboard(**settings_1)
                while flag:
                    keyboard.add_button(label='Начать', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,'Для входа в приложение нажмите Начать\n"При нажатии придется подождать пока прозойдет подборка пользователей по вашим данным"', keyboard)
                    user = UsersBd()
                    if user.find_user_person(event.user_id) == False:
                        if bot.get_users_date() == 'Ошибка в дате рождения! Исправь!':
                            break
                        else:
                            user.add_user(bot.get_users_date())

                    flag = False
                
                if event.text.upper() == 'НАЧАТЬ':
                    if bot.main() == 'Ошибка в дате рождения! Исправь!':
                        keyboard_1.add_button(label='Выйти', color=VkKeyboardColor.SECONDARY)
                        keyboard_1.add_line()
                        write_msg(event.user_id,'Я не смог найти твою дату рождения или город! Проверь свои данные в настройках', keyboard)
                    else:
                        bot.main
                        key_b(keyboard_1)
                        rand = random.randrange(len(bot.list_users))
                        write_msg(event.user_id,f'{bot.list_users[rand]["first_name"]} {bot.list_users[rand]["last_name"]}', keyboard_1, attachment=bot.list_users[rand]["photo"])
                        del bot.list_users[rand]
                elif event.text.upper() == 'ВЫЙТИ':
                    keyboard.add_button(label='Начать', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,'Для входа в приложение нажмите Начать', keyboard)
                elif event.text.upper() == 'СЛЕДУЮЩАЯ':
                    key_b(keyboard_1)
                    rand = random.randrange(len(bot.list_users))
                    write_msg(event.user_id,f'{bot.list_users[rand]["first_name"]} {bot.list_users[rand]["last_name"]}', keyboard_1, attachment=bot.list_users[rand]["photo"])
                    del bot.list_users[rand]
                elif event.text.upper() == 'ДОБАВИТЬ В ИЗБРАННОЕ':
                    key_b(keyboard_1) 
                    rand = random.randrange(len(bot.list_users))
                    user.add_favorites(str(event.user_id), bot.list_users[rand])
                    write_msg(event.user_id,f'{bot.list_users[rand]["first_name"]} {bot.list_users[rand]["last_name"]}', keyboard_1, attachment=bot.list_users[rand]["photo"])
                    del bot.list_users[rand]
                elif event.text.upper() == 'МОИ ИЗБРАННЫЕ':
                    keyboard_1.add_button(label='Выйти', color=VkKeyboardColor.SECONDARY)
                    write_msg(event.user_id,user.find_all_favorites(str(event.user_id)), keyboard_1)