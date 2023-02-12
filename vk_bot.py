import json
from datetime import  date


class Vk_user:

    def __init__(self, user_id, vk, token_2):
        self._user_id = user_id
        self.vk = vk
        self.token_1 = token_2
        self.list_users = []

    def get_users_date(self):
        user_date = self.vk.method('users.get', {'user_ids': self._user_id, 'access_token': self.token_1, 'fields': 'sex, city, bdate'})
        if len(user_date[0]['bdate'].split('.')) < 3:
            return 'Ошибка в дате рождения! Исправь!'
        age_user = date.today().year - int(user_date[0]['bdate'].split('.')[2])
        return {
            'id': user_date[0]['id'],
            'first_name': user_date[0]['first_name'],
            'last_name': user_date[0]['last_name'],
            'sex': user_date[0]['sex'],
            'city': user_date[0]['city']['title'],
            'bdate': user_date[0]['bdate'],
            'age': age_user
        }

    def get_users_for_user(self,user_date, count=100):
        if user_date['sex'] == 2:
            list_users = self.vk.method('users.search', {'hometown': user_date['city'], 'sex': 1, 'fields': 'sex, city, bdate, domain', 'has_photo': 1, 'count': count, 'age_from': user_date['age'], 'age_to': user_date['age'] + 2,  'starus': 6})
            list_itog = []
            for i in list_users['items']:
                if i['is_closed'] == False:
                    list_itog.append(i)    
        else:
            list_users = self.vk.method('users.search', {'hometown': user_date['city'], 'sex': 2, 'fields': 'sex, city, bdate, domain', 'has_photo': 1, 'count': count, 'age_from': user_date['age'], 'age_to': user_date['age'] + 2,  'starus': 6})
            list_itog = []
            for i in list_users['items']:
                if i['is_closed'] == False:
                    list_itog.append(i)   
        return list_itog

    def list_for_bd(self,list):
        list_users_for_bd = []
        for i in list:
            list_photo_user = self.get_photo_user(i['id'])
            list_users_for_bd.append({'id': i['id'], 'first_name': i['first_name'], 'last_name': i['last_name'], 'href': 'https://vk.com/' + i['domain'], 'photo': list_photo_user})
        return list_users_for_bd    
    
    def get_photo_user(self,id_user):
        req = self.vk.method('photos.get', {'owner_id': id_user, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 0})
        sorted_count_like = sorted(req['items'], key=lambda likes: likes['likes']['count'], reverse=True)
        list_photo= f'https://vk.com/id{id_user}'
        for i in range(len(sorted_count_like[:3])):
            owner_id = sorted_count_like[i]['owner_id']
            photo_id = sorted_count_like[i]['id']
            list_photo += f',photo{owner_id}_{photo_id}'
        return list_photo
    
    def write_users_json(self,list_users):
        with open('people.json', 'w', encoding='utf-8') as file:
            json.dump(list_users, file, ensure_ascii=False, indent=2)
     
    def main(self):
        id_data = self.get_users_date()
        if id_data == 'Ошибка в дате рождения! Исправь!':
            return 'Ошибка в дате рождения! Исправь!'
        else:
            list_users_all = self.get_users_for_user(id_data)
            list_users_for_user = self.list_for_bd(list_users_all)
            self.write_users_json(list_users_for_user)
            self.list_users = list_users_for_user