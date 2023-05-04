import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import datetime
from config import comunity_token, access_token
from main import VkTools
from data_base import add_id_users, get_id_users, add_id_users_elect, get_id_users_elect


class BotInterface():

    def __init__(self, comunity_token, access_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(access_token)
        self.params = None
        self.offset = 0

    def message_send(self,
                     user_id,
                     message=None,
                     attachment=None,
                     keyboard=None,
                     sticker_id=None):
        self.interface.method(
            'messages.send', {
                'user_id': user_id,
                'message': message,
                'attachment': attachment,
                'sticker_id': sticker_id,
                'random_id': get_random_id(),
                'keyboard': keyboard
            })

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(
                        event.user_id,
                        f"""Привет, {self.params["name"]} 😊, я бот VKinder \
для знакомств, нажми на кнопку Поиск, чтобы найти подходящие для тебя анкеты \
😎""",
                        keyboard=self.api.keyboard())

                elif '+город' in command:
                    if self.api.get_city(command.split()) == None and len\
                        (command.split()[0]) == 6:
                        self.message_send(event.user_id,
                                          f'❗Город указан не верно')
                    elif len(command.split()[0]) > 6:
                        self.message_send(event.user_id,
                                          f'❗Введите запрос с пробелом')
                    elif len(command.split()) == 1:
                        self.message_send(event.user_id,
                                          f'❗Задан пустой запрос')
                    else:
                        city = self.api.get_city(command.split()[1])
                        self.params['city'] = city
                        self.message_send(event.user_id, f'✅Город добавлен')

                elif '+возраст' in command:
                    if len(command.split()) == 1 and len(command) == 8:
                        self.message_send(event.user_id,
                                          f'❗Задан пустой запрос')

                    elif len(command.split()[0]) > 8:
                        self.message_send(event.user_id,
                                          f'❗Введите запрос с пробелом')
                    elif not str(command.split()[1]).isdigit():
                        self.message_send(event.user_id,
                                          f'❗Введите возраст числом')
                    else:
                        current_year = datetime.now().year
                        year_of_birth = current_year - int(command.split()[1])
                        self.params['bdate'] = f"..{year_of_birth}"
                        self.message_send(event.user_id, f"✅Возраст добавлен")

                elif command == 'поиск':
                    try:
                        if self.params['city'] == None:
                            self.message_send(
                                event.user_id,
                                f'❗Введите Ваш город, например: +город Астрахань'
                            )
                        if self.params['bdate'] == None:
                            self.message_send(
                                event.user_id,
                                f'❗Введите Ваш возраст, например: +возраст 18')

                        if self.params['city'] and self.params['bdate'] != None:
                            users = self.api.search_users(
                                self.params, self.offset)
                            list_id_users = get_id_users(event.user_id)
                            self.message_send(
                                event.user_id,
                                f'Анкеты найдены 🔥, для просмотра нажимай Далее 💫'
                            )

                    except TypeError:
                        self.message_send(event.user_id, f'Напишите привет')

                elif command == 'далее 💫':
                    try:
                        user = users.pop()

                        if user['id'] not in list_id_users:
                            photos_user = self.api.get_photos(user['id'])
                            attachment = ""

                            for num, photo in enumerate(photos_user):
                                attachment += f'photo{photo["owner_id"]}_\
{photo["id"]},'

                                if num == 2:
                                    break

                            self.message_send(event.user_id,
                                              f"""{user["name"]}
                                        vk.com/id{user["id"]}""",
                                              attachment=attachment,
                                              keyboard=self.api.keyboard())

                            add_id_users(event.user_id, user['id'])

                    except IndexError:
                        self.offset += 100
                        users = self.api.search_users(self.params, self.offset)
                        list_id_users = get_id_users(event.user_id)
                        user = users.pop()

                        if user['id'] not in list_id_users:
                            photos_user = self.api.get_photos(user['id'])
                            attachment = ""

                            for num, photo in enumerate(photos_user):
                                attachment += f'photo{photo["owner_id"]}_\
{photo["id"]},'

                                if num == 2:
                                    break

                            self.message_send(event.user_id,
                                              f"""{user["name"]}
                                        vk.com/id{user["id"]}""",
                                              attachment=attachment,
                                              keyboard=self.api.keyboard())

                            add_id_users(event.user_id, user['id'])

                    except UnboundLocalError:
                        self.message_send(event.user_id, f'Нажмите поиск')

                elif command == 'в избранное ❤':
                    try:
                        if user['id'] in get_id_users_elect(event.user_id):
                            self.message_send(
                                event.user_id,
                                f"""❗{user["name"]} уже добавлен(а) в избранное"""
                            )
                        else:
                            add_id_users_elect(event.user_id, user['id'])
                            self.message_send(
                                event.user_id,
                                f"""✅{user["name"]} добавлен(а) в избранное""")

                    except UnboundLocalError:
                        self.message_send(
                            event.user_id,
                            f"""Для добавления в избранное начните искать анкеты"""
                        )
                    except TypeError:
                        self.message_send(
                            event.user_id,
                            f"""Для добавления в избранное начните искать анкеты"""
                        )

                elif command == 'избранное':
                    list_id_users_elect = get_id_users_elect(event.user_id)
                    if list_id_users_elect == []:
                        self.message_send(event.user_id,
                                          f'❗В избранном никого нет')
                    else:
                        for user in list_id_users_elect:

                            photos_user = self.api.get_photos(user)
                            attachment = ""
                            name = self.api.get_profile_info(user)
                            for num, photo in enumerate(photos_user):
                                attachment += f'photo{photo["owner_id"]}_\
{photo["id"]},'

                                if num == 2:
                                    break

                            self.message_send(
                                event.user_id,
                                f"""{name["name"]}
                                        vk.com/id{user}""",
                                attachment=attachment,
                                keyboard=self.api.keyboard_back())

                elif command == 'назад':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(
                        event.user_id,
                        f"""Привет, {self.params["name"]} 😊, я бот VKinder \
для знакомств, нажми на кнопку Поиск, чтобы найти подходящие для тебя анкеты \
😎""",
                        keyboard=self.api.keyboard())

                elif command == 'пока':
                    self.message_send(event.user_id, sticker_id=71117)

                else:
                    self.message_send(event.user_id, 'команда не опознана 😐')


if __name__ == '__main__':
    bot = BotInterface(comunity_token, access_token)
    bot.event_handler()

            
            