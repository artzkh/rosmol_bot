import json_file
import time
from python_rucaptcha import ImageCaptcha

import requests

from os.path import abspath
from os import curdir

directory = abspath(curdir)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
RUCAPTCHA_KEY = "973e7835b66116c1b53d62278637a303"

while True:
    try:
        with open(fr'{directory}\пользователи.txt', 'r') as f:
            user_tokens = f.read().splitlines()
    except Exception:
        print("Неверные ключи доступа! Проверь их в файле \"пользователи.txt\"")
        break

    current_user_token_id = 0
    count_user_tokens = len(user_tokens)

    # try:
    #     with open(fr'{directory}\прокси.txt', 'r') as f:
    #         proxies = f.read().splitlines()
    # except Exception:
    #     print("\033[31mНеверные прокси! Проверь их в файле \"прокси.txt\"")
    #     break
    # current_proxy_id = 0
    # count_proxies = len(user_tokens)

    # def get_proxy():
    #     global current_proxy_id
    #     if current_proxy_id + 1 < count_proxies:
    #         current_proxy_id += 1
    #     else:
    #         current_proxy_id = 0
    #     if len(proxies) >= 1:
    #         if 'https' in proxies[current_proxy_id]:
    #             return {'https': proxies[current_proxy_id]}
    #         elif 'http' in proxies[current_proxy_id]:
    #             return {'http': proxies[current_proxy_id]}
    #         else:
    #             return {'https': proxies[current_proxy_id]}
    #     else:
    #         return ''

    def get_token():
        global current_user_token_id
        if current_user_token_id + 1 < count_user_tokens:
            current_user_token_id += 1
        else:
            current_user_token_id = 0
        return user_tokens[current_user_token_id]

    try:
        post_url = input('\nВставь ссылку на пост:\n')
        post_url = post_url[post_url.find('wall'):]
        post_id = post_url[post_url.find('_')+1:len(post_url)]
        group_id = post_url[post_url.find('wall-')+5:post_url.find('_')]
        int(post_id)
        int(group_id)

        request = f'https://api.vk.com/method/wall.getById?' \
                  f'access_token={get_token()}' \
                  f'&v=5.131' \
                  f'&posts=-{group_id}_{post_id}'
        post = requests.get(request, headers=headers).json()
        likes_count = post['response'][0]['likes']['count']
    except Exception:
        print("Неверная ссылка")
        break

    likes = []
    try:
        offset = 0
        while True:
            print(f"Получаю лайкнувших пользователей...")
            likes = likes + (requests.get(f'https://api.vk.com/method/likes.getList?'
                                          f'&access_token={get_token()}'
                                          f'&v=5.131'
                                          f'&type=post'
                                          f'&owner_id=-{group_id}'
                                          f'&item_id={post_id}'
                                          f'&count=1000'
                                          f'&offset={offset}', headers=headers).json()['response']['items'])
            print(f"Получено {len(likes)}/{likes_count}")
            if likes_count - len(likes) <= 0:
                break
            else:
                offset = len(likes)

        counter = 0
        ids = ''
        users = []
        for item in likes:
            if item == likes[0]:
                counter = 1
                ids = f'{item}'
            if item == likes[-1]:
                users = users + (requests.get(f'https://api.vk.com/method/users.get?'
                                              f'&access_token={get_token()}'
                                              f'&v=5.131'
                                              f'&fields=sex,can_send_friend_request,online'
                                              f'&user_ids={ids}', headers=headers).json()['response'])
            elif counter < 1000:
                counter += 1
                ids += f',{item}'
            else:
                counter = 0
                ids += f',{item}'
                users = users + (requests.get(f'https://api.vk.com/method/users.get?'
                                              f'&access_token={get_token()}'
                                              f'&v=5.131'
                                              f'&fields=sex,can_send_friend_request,online'
                                              f'&user_ids={ids}', headers=headers).json()['response'])
        del likes[:]
    except Exception:
        print("Ошибка при получении лайкнувших пользователей!")
        break

    while True:
        try:
            sex = int(input('1 - Мужской\n2 - Женский\nВведи номер пола: '))
            if sex == 1:
                sex = 2
            elif sex == 2:
                sex = 1
            else:
                print("Ошибка при выборе пола!")
                continue
            break
        except Exception:
            print("Ошибка при выборе пола!")

    print(f"Начинаю отправку заявок...")
    for user in users:
        if user.get('deactivated') is None:
            first_name = user['first_name']
            last_name = user['last_name']
            if user['sex'] == sex:
                if user['can_send_friend_request']:
                    if user['online']:
                        token = get_token()
                        response = requests.get(f'https://api.vk.com/method/friends.add?'
                                                f'&access_token={token}'
                                                f'&v=5.131'
                                                f'&user_id={user["id"]}', headers=headers).json()
                        if response.get('error'):
                            if response['error'].get('error_msg') == 'Captcha needed':
                                while True:
                                    captcha_sid = response["error"]['captcha_sid']
                                    captcha_img = response['error']['captcha_img']
                                    print(f"Распознавание капчи...")
                                    user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_link=captcha_img)
                                    if not user_answer['error']:
                                        code = user_answer['captchaSolve']
                                        print(f"Капча распознана!")
                                    else:
                                        print(f"Требуется ручной ввод ({captcha_img})")
                                        code = input(f"Код: ")
                                    response = requests.get(f'https://api.vk.com/method/friends.add?'
                                                            f'&access_token={token}'
                                                            f'&v=5.131'
                                                            f'&user_id={user["id"]}'
                                                            f'&captcha_sid={captcha_sid}'
                                                            f'&captcha_key={code}', headers=headers).json()
                                    if response.get('error'):
                                        print("Ошибка при вводе капчи!")
                                    else:
                                        print(f"Запрос пользователю {last_name} {first_name} отправлен")
                                        time.sleep(1)
                                        break
                        else:
                            print(f"Запрос пользователю {last_name} {first_name} отправлен")
                            time.sleep(1)
                    else:
                        print(f"Пользователь {last_name} {first_name} не онлайн.")
                else:
                    print(f"Пользователь {last_name} {first_name} запретил отправлять себе заявки в друзья.")
            else:
                if sex == 2:
                    print(f"Пользователь {last_name} {first_name} не мужчина.")
                else:
                    print(f"Пользователь {last_name} {first_name} не женщина.")
    print(f"Все заявки отправлены!")
input("Работа программы завершилась\n")