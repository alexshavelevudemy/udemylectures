from telebot import TeleBot, types
from time import sleep

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")


@bot.message_handler()
def on_message(msg):
    # bot.send_message(chat_id=msg.from_user.id, text='ok. will notify when ready')
    bot.send_chat_action(chat_id=msg.from_user.id, action='typing')

    very_very_huge_operation()
    bot.send_message(chat_id=msg.from_user.id, text='result is 1')


def very_very_huge_operation():
    sleep(3)


bot.polling()
