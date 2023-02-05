import requests
from bs4 import BeautifulSoup

class Vkbot:

    def __init__(self, user_id):
        print("Создан обьект бота")
        self._user_id = user_id
        self._user_name = self.get_user_name(user_id)

        self.commands = ["ПРИВЕТ", "ПОКА"]

    def get_user_name(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        soup = BeautifulSoup(request.text, 'html.parser')
        user_name  = self.clean_all_tag(soup.findAll('title')[0])
        return user_name.split('|')[0]

    def clean_all_tag(self, string_line):
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        
        return result

    def new_message(self, message):

        if message.upper() == self.commands[0]:
            return f"Привет {self._user_name}"
        elif message.upper() == self.commands[1]:
            return f"Пока {self._user_name}"
        else:
            return 'Я не понимаю о чем вы говорите'