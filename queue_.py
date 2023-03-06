#TODO: Методология очереди. Добавить функцию возвращающую очередь обычным sort
import sqlite3 as sl
from queue_database.database import insert, clients, Client

def user_queue(message):
    con = sl.connect('/Users/ketra/Desktop/telegram_bot/cstmrs.db')

    dat = con.execute("SELECT * FROM customers")
    dat_list = list(dat)  # convert to a list of tuples
    return sorted(dat_list, key=lambda x: x[2])  # sort by the third item in each tuple
