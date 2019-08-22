from telebot import TeleBot, types
from config import TG_TOKEN, BITLY_TOKEN, BITLY_URL
import requests
import db_api
import time
from time import sleep
import threading

bot = TeleBot(TG_TOKEN)


WELCOME_MESSAGE = """
Hey! I can shorten links and many more

🔹 Send long url https://www.chelseafc.com/en 
   receive short http://bit.ly/2FUgzLf

🔹 Send short url bit.ly/2FUgzLf 
   receive clicks count
   
 🔹 Also you can use buttons to see help again or top links by clicks count
"""

ABOUT = 'about me'
TOP_LINKS = 'see top links'
TOP_24 = 'top24'
TOP_ALL = 'top_all'
CLICKS_COUNT = "🔹 Clicks count = {}"
LINK_CLICKS_COUNT = "- clicks count for {} = {}"


@bot.message_handler(commands=['start', 'help'])
def start_handler(msg):
    keyboard = get_main_keyboard()
    bot.send_message(msg.chat.id, text=WELCOME_MESSAGE, reply_markup=keyboard, disable_web_page_preview=True)


@bot.message_handler(regexp=f'^{ABOUT}$')
def help_handler(msg):
    bot.reply_to(msg, text=WELCOME_MESSAGE, disable_web_page_preview=True)


@bot.message_handler(regexp=f'^{TOP_LINKS}$')
def top_links_handler(msg):
    keyboard = get_top_links_keyboard()
    bot.send_message(msg.chat.id, text='choose period', reply_markup=keyboard)


@bot.message_handler()
def messages_handler(msg):
    link_url = msg.text[7:] if msg.text.startswith('http://bit.ly/') else msg.text

    clicks_count = get_clicks_count(link_url)

    if isinstance(clicks_count, int):
        response = CLICKS_COUNT.format(clicks_count)
        db_api.update_link_clicks(link_url, clicks_count)
    else:

        text = 'https://' + msg.text if not msg.text.startswith('https://') else msg.text
        short_link = shorten_url(text)

        if short_link:
            response = short_link
            db_api.create_link_record(msg.from_user.id, text, short_link[7:], get_timestamp())
        else:
            response = 'bad url'

    bot.reply_to(msg, text=response)


@bot.callback_query_handler(func=lambda call: TOP_24 in call.data)
def top_24_handler(call):
    timestamp = get_timestamp()
    created_after = timestamp - 86400
    stats = db_api.get_top_links(call.from_user.id, created_after=created_after)
    response = ''
    for link, clicks in stats:
        response += LINK_CLICKS_COUNT.format(link, clicks)
        response += '\n'

    bot.send_message(call.from_user.id, text=response, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: TOP_ALL in call.data)
def top_all_handler(call):
    stats = db_api.get_top_links(call.from_user.id)
    response = ''
    for link, clicks in stats:
        response += LINK_CLICKS_COUNT.format(link, clicks)
        response += '\n'

    bot.send_message(call.from_user.id, text=response, disable_web_page_preview=True)


def get_top_links_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='top links (24 hours)', callback_data=TOP_24))
    markup.add(types.InlineKeyboardButton(text='top links (all time)', callback_data=TOP_ALL))
    return markup


def get_timestamp():
    return int(time.time())


def get_headers(token):
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(token)}
    return headers


def shorten_url(link):
    url = BITLY_URL.format('shorten')
    headers = get_headers(BITLY_TOKEN)
    res = requests.post(url=url, headers=headers, json={'long_url': link})
    if res.ok:
        bitly_data = res.json()
        return bitly_data['link']


def get_clicks_count(link):
    url = BITLY_URL.format('bitlinks/{}/clicks/summary'.format(link))
    headers = get_headers(BITLY_TOKEN)
    res = requests.get(url=url, headers=headers, json={'long_url': link})
    if res.ok:
        bitly_data = res.json()
        return bitly_data['total_clicks']


def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text=ABOUT))
    markup.add(types.KeyboardButton(text=TOP_LINKS))
    return markup


def clicks_updater():
    while True:
        print('updater wackes up')
        offset = 0
        while True:
            rows = db_api.get_links(offset=offset)

            if not rows:
                break

            for old_clicks, link in rows:

                print('get clicks count for ', link)

                clicks_count = get_clicks_count(link)

                if isinstance(clicks_count, int) and clicks_count != old_clicks:
                    db_api.update_link_clicks(link, clicks_count)

            offset += 10

        print('updater go to sleep')
        sleep(60*30)


threading.Thread(target=clicks_updater, args=()).start()


bot.polling()
