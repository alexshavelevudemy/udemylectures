from telebot import TeleBot

bot = TeleBot("854707499:AAEdUKfZf8M7UY3QE8FDAUUYhDORBwQlMNA")


@bot.message_handler(regexp='bold')
def bold_handler(message):
    text = message.text.replace('bold', '')
    msg = bot.reply_to(message, text='*{}*'.format(text), parse_mode='markdown')
    print(msg)


@bot.message_handler(regexp='italic')
def italic_handler(message):
    text = message.text.replace('italic', '')
    bot.reply_to(message, text='_{}_'.format(text), parse_mode='markdown')


@bot.message_handler(regexp='inline')
def inline_handler(message):
    text = message.text.replace('inline', '')
    bot.reply_to(message, text='`{}`'.format(text), parse_mode='markdown')


bot.polling()

