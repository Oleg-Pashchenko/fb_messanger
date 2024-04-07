import os

import requests
import dotenv

dotenv.load_dotenv()


def send_message(text):
    f = open('users.txt', 'r').read().split('\n')
    for i in f:
        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(os.getenv('BOT_TOKEN'), 'sendMessage'),
            data={'chat_id': i, 'text': text}
        ).json()
        print(response)
