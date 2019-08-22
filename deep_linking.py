from telebot import TeleBot, types


bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")


@bot.message_handler(commands=['generate'])
def on_message(msg):
    data = '{user_id}'.format(user_id=msg.from_user.id)
    referral_link = 't.me/alextestqwe123bot?start={}'.format(data)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='share', url='https://telegram.me/share/url?url={}'.format(referral_link)))
    bot.send_message(chat_id=msg.from_user.id,
                     text='Press button to share or copy link `{}`'.format(referral_link),
                     reply_markup=markup,
                     parse_mode='markdown')


@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['new_chat_members'])
@bot.message_handler(func=lambda msg: 'start' in msg.text or 'help' in msg.text)
@bot.message_handler(commands=['delete'], func=lambda message: message.from_user.id in ADMINS)
@bot.message_handler(func=lambda message: message.from_user.id in ADMINS)
@bot.message_handler()
def on_start(msg):
    if len(msg.text) > 6:
        print('\n\n\nreferral user from {}. need to save it\n\n\n'.format(msg.text[7:]))

    else:
        print('not referral user')

    bot.reply_to(msg, text='hi')


bot.polling()
