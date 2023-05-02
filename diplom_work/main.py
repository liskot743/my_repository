from datetime import datetime
import vk_api
from config import access_token
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class VkTools():

    def __init__(self, access_token):
        self.api = vk_api.VkApi(token=access_token)

    def get_profile_info(self, user_id):
        info, = self.api.method('users.get', {
            'user_id': user_id,
            'fields': 'bdate,sex,city'
        })

        user_info = {'name': info['first_name'] + ' ' + info['last_name'],
                     'id':  info['id'],
                     'bdate': info['bdate'] if 'bdate' in info and\
                     len(info['bdate'].split('.')) == 3 else None,
                     'sex': info['sex'],
                     'city': info['city']['id'] if 'city' in info else None
                    }

        return user_info

    def search_users(self, params, offset=0):
        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        current_year = datetime.now().year
        year_of_birth = int(params['bdate'].split('.')[2])
        age = current_year - year_of_birth
        age_from = age - 5
        age_to = age + 5

        users = self.api.method(
            'users.search', {
                'count': 100,
                'offset': offset,
                'age_from': age_from,
                'age_to': age_to,
                'sex': sex,
                'city': city,
                'status': 6,
                'is_closed': False
            })
        try:
            users = users['items']
        except KeyError:
            return []

        res = []

        for user in users:
            if user['is_closed'] == False:
                res.append({
                    'id': user['id'],
                    'name': user['first_name'] + ' ' + user['last_name']
                })

        return res

    def get_photos(self, user_id):
        photos = self.api.method('photos.get', {
            'user_id': user_id,
            'album_id': 'profile',
            'extended': 1
        })
        try:
            photos = photos['items']
        except KeyError:
            return []

        res = []

        for photo in photos:
            res.append({
                'owner_id': photo['owner_id'],
                'id': photo['id'],
                'likes': photo['likes']['count'],
                'comments': photo['comments']['count'],
            })

        res.sort(key=lambda x: x['likes'] + x['comments'], reverse=True)

        return res

    def get_city(self, query):
        city = self.api.method('database.getCities', {
            'q': query,
            'need_all': 0,
            'count': 1
        })

        if city['items'] == []:
            return None

        return city['items'][0]['id']

    def keyboard(self):
        VK_kb = VkKeyboardColor
        keyboard = VkKeyboard(one_time=False)

        keyboard.add_button('Поиск', color=VK_kb.PRIMARY)
        keyboard.add_button('Далее 💫', color=VK_kb.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('В избранное ❤', color=VK_kb.POSITIVE)
        keyboard.add_button('Избранное', color=VK_kb.SECONDARY)

        return keyboard.get_keyboard()

    def keyboard_back(self):
        VK_kb = VkKeyboardColor
        keyboard = VkKeyboard(one_time=False)

        keyboard.add_button('Назад', color=VK_kb.PRIMARY)

        return keyboard.get_keyboard()







