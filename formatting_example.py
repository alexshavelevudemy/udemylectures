from telebot import TeleBot, types

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")


@bot.message_handler()
def handler(message):
    text = """*Hello*
It is the _Goods store bot_. here you can find our [website](google.com)

If any problems contact our [admin](tg://user?id=855333390)

ps this bot is written in `python`
    """

    bot.send_message(message.from_user.id, text=text, parse_mode='markdown')


bot.polling()
