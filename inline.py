from telebot import TeleBot, types

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")


"""
Module to show work with keyboards
"""


# Labels and messages
WELCOME = 'Welcome'
# end


@bot.message_handler(commands=['start'])
def social_medias(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='twitter', url='https://twitter.com'))
    markup.add(types.InlineKeyboardButton(text='contact me', callback_data='contact_me'))
    markup.add(types.InlineKeyboardButton(text='switch inline', switch_inline_query='horse'))
    markup.add(types.InlineKeyboardButton(text='switch inline current chat', switch_inline_query_current_chat='panda'))
    bot.send_message(chat_id=msg.from_user.id, text=WELCOME, reply_markup=markup)


@bot.message_handler(regexp='panda')
def panda_handler(msg):
    bot.send_photo(msg.from_user.id, photo=open('pics/panda.jpg', 'rb'))


@bot.message_handler(regexp='horse')
def panda_handler(msg):
    bot.send_photo(msg.chat.id, photo=open('pics/horse.jpg', 'rb'))


@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    print('we receive callback {}'.format(call.data))
    bot.send_message(call.from_user.id, text='our support will contact you')


bot.polling()


"""
 


"""