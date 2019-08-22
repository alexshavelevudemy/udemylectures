from telebot import TeleBot, types

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")


@bot.message_handler(commands=['start'])
def start_handler(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='who am i?'))
    markup.add(types.KeyboardButton(text='send phone', request_contact=True))
    markup.add(types.KeyboardButton(text='send location', request_location=True))

    bot.send_message(msg.from_user.id, text='hello', reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def contact_handler(msg):

    ## here we can save contact somewhere

    bot.reply_to(msg, text='thanks for your phone', reply_markup=types.ReplyKeyboardRemove())


bot.polling()



