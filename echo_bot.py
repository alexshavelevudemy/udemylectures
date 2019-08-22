import requests


TG_URL = 'https://api.telegram.org/bot{}/{}'
TOKEN = '913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4'


def process_update(update):
    chat_id = update.get('message', {}).get('from').get('id')
    message_text = update.get('message', {}).get('text')
    is_photo = update.get('message').get('photo')

    if message_text:
        requests.post(url=TG_URL.format(TOKEN, 'sendMessage'),
                      data={'chat_id': chat_id,
                            'text': 'you sent me {}'.format(message_text)})
    elif is_photo:
        requests.post(url=TG_URL.format(TOKEN, 'sendMessage'),
                      data={'chat_id':chat_id,
                            'text': 'you sent me photo. it is nice'})

    # the same handlers you can make for videos, stickers etc


if __name__ == '__main__':
    offset = 0
    while True:
        response = requests.get(url=TG_URL.format(TOKEN, 'getUpdates'),
                                params={'offset': offset})

        if response.ok:
            data = response.json()['result']
            print('update:', data)
            try:
                offset = data[-1]['update_id'] + 1
            except IndexError:
                pass

            for update in data:
                process_update(update)
