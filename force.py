from telebot import TeleBot, types

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")


"""
    
    ForceReply - https://core.telegram.org/bots/api#forcereply
    
"""


@bot.message_handler()
def on_message(msg):
    bot.send_message(chat_id=msg.from_user.id,
                     text='how are you?',
                     reply_markup=types.ForceReply())


bot.polling()
