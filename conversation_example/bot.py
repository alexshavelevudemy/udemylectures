from telebot import TeleBot, types
from states import States
import storage

bot = TeleBot("913744703:AAHyREa9dESClOHce4MMC33ivRhoVoB-2k4")

USER_DATA = {}


@bot.message_handler(commands=['reservation'])
def reservation_handler(msg):
    # clear user reservation data
    USER_DATA[msg.from_user.id] = {}
    # ask for date
    bot.reply_to(msg, text='Tell me please reservation date')
    # new line
    storage.set_user_state(msg.from_user.id, States.WAIT_DATE)


@bot.message_handler(func=lambda msg: storage.get_current_state(msg.from_user.id) == States.WAIT_DATE)
def save_date(msg):
    # get user data
    data = USER_DATA[msg.from_user.id]
    # save date to user data
    data['date'] = msg.text
    # update storage
    USER_DATA[msg.from_user.id] = data
    # ask about persons count
    bot.reply_to(msg, text='how many persons?')
    # new line
    storage.set_user_state(msg.from_user.id, States.WAIT_PERSONS_COUNT)


@bot.message_handler(func=lambda msg: storage.get_current_state(msg.from_user.id) == States.WAIT_PERSONS_COUNT)
def save_persons_count(msg):
    # get user data
    data = USER_DATA[msg.from_user.id]
    # save persons to user data
    data['persons'] = msg.text
    # update storage
    USER_DATA[msg.from_user.id] = data
    # create phone share button
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text='share phone', request_contact=True))
    # ask for phone number
    bot.send_message(chat_id=msg.from_user.id, text='share your phone number',
                     reply_markup=markup)

    # new line
    storage.set_user_state(msg.from_user.id, States.WAIT_PHONE)


@bot.message_handler(content_types=['contact'])
@bot.message_handler(func=lambda msg: storage.get_current_state(msg.from_user.id) == States.WAIT_PHONE)
def save_phone(msg):

    data = USER_DATA[msg.from_user.id]
    print('user {} with phone {} wants to reserve table for {} persons at {}'.format(
        msg.from_user.id, msg.contact.phone_number, data['persons'], data['date']
    ))

    bot.reply_to(msg, text='thanks, reservation is created')
    # new line
    storage.set_user_state(msg.from_user.id, States.START)


bot.polling()
