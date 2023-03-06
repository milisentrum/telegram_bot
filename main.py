import os
import telebot
from telebot import types
from typing import List, Dict, Tuple
# import queue_database.database
from queue_database.database import insert, clients, Client
from queue_ import user_queue

bot = telebot.TeleBot("6289556666:AAGpinAWZMv3AaI3pNOk4s79_pFLP3jpV0E")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот для огрганизации очереди, "
                          "нажми /registration для регистрации, "
                          "или /queue для просмотра текущей очереди")

@bot.message_handler(commands=['registration'])
def send_welcome(message):
    message_ = bot.reply_to(message, "Привет, как тебя зовут?")
    bot.register_next_step_handler(message_, user_name)

def user_name(message):
    try:
        print(message)
        chat_id = message.chat.id
        name = message.text
        client = Client(name)

        # : записать в базу данных (разобраться как именно выглядит архитектура)
        clients[chat_id] = client

        message_ = bot.reply_to(message, "Возраст:")
        bot.register_next_step_handler(message_, user_age)
    except Exception as e:
        print(e)

def user_age(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            message_ = bot.reply_to(message, "Неверный возраст, введите заново")
            bot.register_next_step_handler(message_, user_age)
        client = clients[chat_id]
        client.age = age

        # clients[chat_id] = (client, age)
        ##
        gender_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        gender_markup.add('М','Ж')
        message_ = bot.reply_to(message, "Пол", reply_markup=gender_markup)
        bot.register_next_step_handler(message_, user_gender)
    except Exception as e:
        print(e)

def user_gender(message):
    try:
        chat_id = message.chat.id
        gender = message.text
        client = clients[chat_id]
        client.gender = gender

        hurry_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        hurry_markup.add('1', '0') # вводить только str
        message_ = bot.reply_to(message, "Вы торопитесь?", reply_markup=hurry_markup)
        bot.register_next_step_handler(message_, user_hurry)
    except Exception as e:
        print(e)

def user_hurry(message):
    try:
        chat_id = message.chat.id
        is_hurry = message.text
        client = clients[chat_id]
        client.is_hurry = is_hurry
        message_ = bot.reply_to(message, "Отлично, регистрация прошла успешно!")
        insert(message)
    except Exception as e:
        print(e)

#: послe получения данных применить написанный в database.py insert
# (пусть этот инсекрт принимает класс как аргумент).

# : А также нужно зарегистрировать /queue который возвращает текущую выдачу очереди.
#  пока применить обычный sort для возвращения порядка

@bot.message_handler(commands=['queue'])
def send_welcome(message):
    try:
        sorted_users = user_queue(message)
        for row in sorted_users:
            bot.send_message(chat_id=message.chat.id, text=f"{row[1]}")

    except Exception as e:
        print(e)

bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
bot.infinity_polling()
