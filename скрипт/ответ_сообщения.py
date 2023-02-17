import json
import time
from os.path import abspath
from os import curdir
from os import mkdir

import requests

directory = abspath(curdir)

while True:
    messages_count = 0

    try:
        with open(fr'{directory}\пользователи.txt', 'r') as f:
            user_tokens = f.read().splitlines()
    except Exception:
        print("Неверные ключи доступа! Проверь их в файле \"пользователи.txt\"")
        break

    try:
        with open(fr'{directory}\сообщение1.txt', 'r', encoding="utf-8") as f:
            message1 = f.read()
            if message1 != '':
                messages_count += 1
            messages_count += 1
    except Exception:
        print("Неверное сообщение 1 - проверь его в файле \"сообщение1.txt\"")
        break
    try:
        with open(fr'{directory}\сообщение2.txt', 'r', encoding="utf-8") as f:
            message2 = f.read()
            if message2 != '':
                messages_count += 1
    except Exception:
        print("Неверное сообщение 2 - проверь его в файле \"сообщение2.txt\"")
        break
    try:
        with open(fr'{directory}\сообщение3.txt', 'r', encoding="utf-8") as f:
            message3 = f.read()
            if message3 != '':
                messages_count += 1
    except Exception:
        message3 = False
    try:
        try:
            mkdir("json_file")
        except Exception:
            pass
        try:
            with open(fr"{directory}/json_file/answers.json", "r") as file:
                answers = json.load(file)
        except Exception as e:
            answers = {}
            with open(fr"{directory}/json_file/answers.json", "w+") as file:
                json.dump(answers, file)
    except Exception as e:
        print(e)
        break

    print(f"Начинаю отвечать на сообщения...")
    while True:
        for token in user_tokens:
            response = requests.get(f'https://api.vk.com/method/messages.getConversations?'
                                    f'&access_token={token}'
                                    f'&v=5.131'
                                    f'&filter=unread'
                                    f'&count=200').json()
            for chat in response['response']['items']:
                if chat['conversation']['peer']['type'] == 'user':
                    peer_id = chat['conversation']['peer']['id']
                    if answers.get(peer_id):
                        count = answers[peer_id]
                    else:
                        count = 0
                    if count == 0:
                        response = requests.get(f'https://api.vk.com/method/messages.send?'
                                                f'&access_token={token}'
                                                f'&v=5.131'
                                                f'&user_id={peer_id}'
                                                f'&random_id=0'
                                                f'&message={message1}').json()
                        print("Отправлен первый ответ на сообщение")
                        answers[peer_id] = 1
                    elif count == 1:
                        response = requests.get(f'https://api.vk.com/method/messages.send?'
                                                f'&access_token={token}'
                                                f'&v=5.131'
                                                f'&user_id={peer_id}'
                                                f'&random_id=0'
                                                f'&message={message2}').json()
                        print("Отправлен второй ответ на сообщение")
                        answers[peer_id] = 2
                    elif count == 2:
                        if message3:
                            response = requests.get(f'https://api.vk.com/method/messages.send?'
                                                    f'&access_token={token}'
                                                    f'&v=5.131'
                                                    f'&user_id={peer_id}'
                                                    f'&random_id=0'
                                                    f'&message={message3}').json()
                            print("Отправлен третий ответ на сообщение")
                            answers[peer_id] = 3
                    else:
                        response = requests.get(f'https://api.vk.com/method/messages.markAsRead?'
                                                f'&access_token={token}'
                                                f'&v=5.131'
                                                f'&peer_id={peer_id}'
                                                ).json()
                        print("Прочитано сообщение")
                    time.sleep(2)
        with open(fr"{directory}/json_file/answers.json", "w+") as file:
            json.dump(answers, file)
        time.sleep(10)
