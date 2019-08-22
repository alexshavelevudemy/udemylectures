from telebot import TeleBot, types
import random

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")


CAPTIONS = ['panda is walking', 'panda is thinking', 'panda is eating', 'also eating', 'baby panda']


def get_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='edit caption', callback_data='edit_caption'))
    markup.add(types.InlineKeyboardButton(text='edit media', callback_data='edit_media'))
    markup.add(types.InlineKeyboardButton(text='edit keyboard', callback_data='edit_keyboard'))

    return markup


def get_new_caption(old_caption):
    new_id = random.randint(1, 5)

    if CAPTIONS[new_id - 1] != old_caption:
        return CAPTIONS[new_id - 1]
    else:
        get_new_caption(old_caption)


@bot.message_handler(commands=['start'])
def start_handler(msg):
    markup = get_keyboard()
    bot.send_photo(msg.from_user.id, photo=open('pics/panda.jpg', 'rb'), caption='this is panda', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'edit_caption' in call.data)
def edit_caption(call):
    new_caption = get_new_caption(call.message.caption),
    bot.edit_message_caption(caption=new_caption, chat_id=call.message.chat.id,
                             message_id=call.message.message_id, reply_markup=get_keyboard())


@bot.callback_query_handler(func=lambda call: 'edit_media' in call.data)
def edit_media(call):
    new_id = random.randint(1, 5)
    new_file = 'pics/{}.jpg'.format(new_id)
    bot.edit_message_media(media=types.InputMediaPhoto(open(new_file, 'rb')), chat_id=call.message.chat.id,
                           message_id=call.message.message_id, reply_markup=get_keyboard())


@bot.callback_query_handler(func=lambda call: 'edit_keyboard' in call.data)
def edit_keyboard(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='delete message', callback_data='delete_message'))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'delete_message' in call.data)
def delete_message(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text='deleted, send /start to see panda again')


bot.polling()
