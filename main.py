import telebot
from telebot import types  # кнопки
from string import Template
import source, config
# import sqlConnect
# import sqlite3
# from sqlite3 import Error
# from time import sleep, ctime
# from sqlConnect import SQLConnect
# import datetime
# import calendar

"""token"""
bot = telebot.TeleBot(config.token)

user_dict = {}
# # ініціалзізація конект з БД
# db = SQLConnect('db.db')

class User:
    def __init__(self, spesialist):
        self.spesialist = spesialist

        keys = ['fullname', 'phone', 'service']

        for key in keys:
            self.key = None

# menu
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/registration')
    # itembtn3 = types.KeyboardButton('/options')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Доброго дня "
                     + message.from_user.first_name
                     + ", я ваш Барбер бот.\n "
                     + "Виберіть пункт меню:\n\n"
                     + "/about  - детальна інформація про заклад\n"
                     + "/registration  - записатись на прийом\n",
                     reply_markup=markup)

# /about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, source.scissors + "Барбершоп BORODA" + source.scissors + "\n"
                     + "Це місце виключно для чоловіків" + source.mens + ", де панує своя атмосфера.\n"
                     + "Ми підкреслимо ваш стиль крутою зачіскою" + source.cool + "і тут ви зможете наслодитись"
                     + " ароматним ромом Bacardi" + source.drink + "під час стрижки.\n\n"
                     + source.pushpin + " Наша адреса:\n"
                     + " м. Дрогобич, вул. Стрийська, 34\n\n"
                     + source.clock + " Графік роботи:\n"
                     + " Пн-Сб - 10:00 - 20:00\n"
                     + " Нд - 10:00 -  15:00\n\n"
                     + source.phone + " Тел. +380672112201"
                     )

# /registration
@bot.message_handler(commands=["registration"])
def set_specialist(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    itembtn1 = types.KeyboardButton('Макс')
    itembtn2 = types.KeyboardButton('Іван')
    itembtn3 = types.KeyboardButton('Діма')
    itembtn4 = types.KeyboardButton('Максим')
    itembtn5 = types.KeyboardButton('Павло')
    itembtn6 = types.KeyboardButton('Остап')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

    msg = bot.send_message(message.chat.id, source.cool + 'Виберіть майстра:', reply_markup=markup)
    bot.register_next_step_handler(msg, set_service)

# def get_calendar(message):
#     now = datetime.datetime.now() #Текущая дата
#     chat_id = message.chat.id
#     date = (now.year,now.month)
#     current_shown_dates[chat_id] = date #Сохраним текущую дату в словарь
#     markup = create_calendar(now.year,now.month)
#     bot.send_message(message.chat.id, "Пожалйста, выберите дату", reply_markup=markup)

# set_service
def set_service(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # inline buttons
        # markup = telebot.types.InlineKeyboardMarkup()
        # markup.add(telebot.types.InlineKeyboardButton(text='Чоловіча стрижка', callback_data=1))
        # markup.add(telebot.types.InlineKeyboardButton(text='Стрижка під насадку', callback_data=2))
        # markup.add(telebot.types.InlineKeyboardButton(text='Стрижка бороди', callback_data=3))
        # markup.add(telebot.types.InlineKeyboardButton(text='Чоловіча стрижка та борода', callback_data=4))
        # markup.add(telebot.types.InlineKeyboardButton(text='Дитяча стрижка', callback_data=5))
        # bot.send_message(message.chat.id, text="Какая средняя оценка была у Вас в школе?", reply_markup=markup)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, selective=False)
        itembtn1 = types.KeyboardButton('Чоловіча стрижка')
        itembtn2 = types.KeyboardButton('Стрижка під насадку')
        itembtn3 = types.KeyboardButton('Стрижка бороди')
        itembtn4 = types.KeyboardButton('Чоловіча стрижка та борода')
        itembtn5 = types.KeyboardButton('Дитяча стрижка')

        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

        msg = bot.send_message(chat_id, source.scissors + 'Виберіть послугу:', reply_markup=markup)
        bot.register_next_step_handler(msg, set_name)

    except Exception as e:
        bot.reply_to(message, source.error + 'ooops!!')

# set_name
def set_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.service = message.text

        # видалити стару клавіатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, source.pencil + 'Введіть Ваше імя:', reply_markup=markup)
        bot.register_next_step_handler(msg, set_phone_number)

    except Exception as e:
        bot.reply_to(message, source.error + 'ooops!!')

# set_phone
def set_phone_number(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, source.phone + 'Ваш номер телефона:')
        bot.register_next_step_handler(msg, create_order)

    except Exception as e:
        msg = bot.reply_to(message, source.error + 'Будь ласка, напишіть Ваш номер телефона:')
        bot.register_next_step_handler(msg, create_order)

# create_order
def create_order(message):
    try:
        # int(message.text)
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        # ваша заявка
        bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")
        # відправити в группу
        bot.send_message(config.group_id, getRegData(user, 'Заявка від бота', bot.get_me().first_name), parse_mode="Markdown")
        # bot.send_message(-1001432228089, "TEST")

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Так', callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='Внести зміни', callback_data=2))

        msg = bot.send_message(message.chat.id, 'Все вірно?', reply_markup=markup)

        # передача даних в БД
        # async def add_order(message: types.Message):
        #     db.add_order(message.from_user.id, user.spesialist, user.service, user.fullname, user.phone)

        # bot.send_message(message.from_user.id, f'Welcome  {message.from_user.first_name}')

    except Exception as e:
        # msg = bot.reply_to(message, error + 'Будь ласка, напишіть Ваш номер телефона:')
        bot.reply_to(message, source.error + 'error')

# show_order
# нельзя делать перенос строки Template и в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template(
        '$title *$UserName* \n Спеціаліст: *$spesialist* \n Вибрана послуга: *$service* \n Імя клієта: *$name* \n Телефон клієта: *$phone*')

    return t.substitute({
        'title': title,
        'UserName': name,
        'spesialist': user.spesialist,
        'service': user.service,
        'name': user.fullname,
        'phone': user.phone
    })

    # sqlConnect.register_user(user.spesialist, user.service, user.fullname, user.phone)

# headler_block
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    # chat_id = message.chat.id
    # user = user_dict[chat_id]
    if call.data == '1':
        bot.answer_callback_query(callback_query_id=call.id, text='Дані успішно відправлені!')
        answer = source.check + 'Ваша заявка успішно створена!\n ' \
                 'Очікуємо на вас в баребершопі Boroda'

        # bot.send_message(-1001432228089, getRegData(user, 'Заявка від бота', bot.get_me().username),
        #                  parse_mode="Markdown")
        # chat_id = message.chat.id
        # user = user_dict[chat_id]
        # sqlConnect.register_user(user.spesialist, user.service, user.fullname, user.phone)
    elif call.data == '2':
        answer = 'В процесі...'
        # bot.register_next_step_handler(msg, lambda m: callback(m, args *))
        # bot.register_next_step_handler(set_specialist)

    bot.send_message(call.message.chat.id, answer)

# free_text
@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, 'О нас - /about\nРегистрация - /registration\nПомощь - /help')
    bot.send_message(-1001432228089, "Hello!")


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)



###BOT###

# mychatID = 393455790

# keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
# keyboard1.row('Привет', 'Пока', 'Каталог', 'Cube')
#
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
#
# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id, 'Привет, мой создатель')
#     elif message.text.lower() == 'привіт':
#         bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBAAGxXv-UU48L8nxZCYNjuBU_YX9yKOcAAsgDAAKc1ucKoWmiy7GEUk4aBA')
#     elif message.text.lower() == 'пока':
#         bot.send_message(message.chat.id, 'Прощай, создатель')
#     elif message.text.lower() == 'каталог':
#         bot.send_message(message.chat.id, 'Прощай, создатель')
#     elif message.text.lower() == 'як оплатити?':
#         bot.send_message(message.chat.id, 'Для оплати переведіть зазначену суму товару на картку:\n 5345 3534 3234 3245\n '
#                                           'Після чого з вами звяжеться оператор для узгодження всіх деталей змовлення.')
#     elif message.text.lower() == 'cube':
#         bot.send_dice(message.chat.id)
#
# bot.polling()

# bot = telebot.TeleBot(config.token)
