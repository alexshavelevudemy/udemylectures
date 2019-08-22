from telebot import TeleBot, types
import json

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")

PHOTOS = {}


def load_photos():
    with open('photos.json') as file:
        data = json.loads(file.read())

        for k, v in data.items():
            PHOTOS[int(k)] = v


@bot.message_handler(commands=['gallery'])
def gallery_handler(msg):
    photo_url = get_photo_url()
    keyboard = get_keyboard()
    bot.send_photo(chat_id=msg.from_user.id, photo=photo_url, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def navigation_handler(call):
    requested_id = int(call.data)
    photo_url = get_photo_url(requested_id)
    keyboard = get_keyboard(requested_id)
    bot.edit_message_media(media=types.InputMediaPhoto(photo_url), chat_id=call.message.chat.id,
                           message_id=call.message.message_id, reply_markup=keyboard)


def get_photo_url(page_id=1):
    return PHOTOS[page_id]


def get_keyboard(page_id=1):
    markup = types.InlineKeyboardMarkup()

    back_button = get_back_button(page_id)
    next_button = get_next_button(page_id)

    if back_button:
        markup.add(back_button)

    if next_button:
        markup.add(next_button)

    return markup


def get_back_button(page_id):

    if page_id == 1:
        return

    return types.InlineKeyboardButton(text='back', callback_data='{}'.format(page_id - 1))


def get_next_button(page_id):

    if page_id == len(PHOTOS):
        return

    return types.InlineKeyboardButton(text='next', callback_data='{}'.format(page_id + 1))


load_photos()

bot.polling()
