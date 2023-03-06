'''Файл для реализации базы данных и запросов к ней'''
import sqlite3 as sl
import random
from uuid import uuid4

clients = {}

class Client:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.gender = None
        self.is_hurry = None

#TODO: Сделать объект базы данных c таблицей. Сохранение дампа базы внутри этой папки
# Тут должен быть реализован метод загрузки в базу, в нужную таблицу данных из
# класса clients. Который просто применяется потом в route телеграм бота
# Делать любое общение с базой по виду 'with connect()  as conn:
# conn.<>'
#TODO: добавить в базу номер объекта

cstmrs_cnt=15
# открываем файл с базой данных
con = sl.connect('cstmrs.db')
# открываем базу
with con:
    # получаем количество таблиц с нужным нам именем
    data = con.execute("select count(*) from sqlite_master where type='table' and name='customers'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            with con:
                # con.execute("""
                #     CREATE TABLE customers (
                #         id str PRIMARY KEY,
                #         last_name VARCHAR(30),
                #         gender VARCHAR(10),
                #         label INT,
                #         age INT); """) #label - значения номера очереди после машинной обработки
                # подготавливаем множественный запрос
                # sql = 'INSERT INTO customers (id, last_name, gender, label, age) values(?, ?, ?, ?, ?)'
                con.execute("""
                    CREATE TABLE customers (
                        id str PRIMARY KEY,
                        name VARCHAR(30),
                        age INT,
                        gender VARCHAR(10),
                        is_hurry INT); """) #is_hurry будет принимать 0 или 1, т.к. bool нет в sqlite3

            # sql = 'INSERT INTO customers (id, name, age, gender, is_hurry) values(?, ?, ?, ?, ?)'
            #
            # # указываем данные для запроса
            # data = []
            # # for x in range(cstmrs_cnt):
            # #     data.append([str(uuid4()), random.choice(list(open("surnames.txt"))).rstrip('\n'),
            # #                  random.choice(['male', 'female']), 0, random.randint(14, 99)])
            # for x in range(cstmrs_cnt):
            #     data.append([str(uuid4()), clients.name, clients.age, clients.gender, clients.is_hurry])
            #
            # # добавляем с помощью множественного запроса все данные сразу
            # with con:
            #     con.executemany(sql, data)

def insert(message):
    chat_id = message.chat.id
    client = clients[chat_id]
    data = (chat_id, client.name, client.age, client.gender, client.is_hurry)

    with sl.connect('cstmrs.db') as con:
        if is_id_unique(con, 'customers', chat_id):
            con.execute("INSERT INTO customers (id, name, age, gender, is_hurry) values(?, ?, ?, ?, ?)", data)
            con.commit()
            print("New record added successfully")
        else:
            print("ID already exists")

    # dat = con.execute("SELECT * FROM customers")
    # for row in dat:
    #     print(row)

def is_id_unique(con, table_name, id):
    with con:
        # Execute a SELECT query to retrieve the IDs from the table
        data = con.execute(f"SELECT id FROM {table_name}")
        id_list = [row[0] for row in data]
        # Check if the ID being added already exists in the list
        return id not in id_list

# with con:
#     data_queues = con.execute("select count(*) from sqlite_master where type='table' and name='queues'")
#     for row in data_queues:
#         if row[0] == 0:
#             with con:
#                 con.execute("""
#                     CREATE TABLE queues (
#                         queue_id str PRIMARY KEY,
#                         customer_id str,
#                         datetime DATETIME,
#                         value INT,
#                         is_hurry BOOLEAN); """)
#
#             sql = 'INSERT INTO queues (queue_id, customer_id, datetime, value, is_hurry) values(?, ?, ?, ?, ?)'
#             data_queues = []
#             for x in range(20):
#                 data_queues.append([str(uuid4()), str(uuid4()), '2023-01-01', x, random.choice([0, 1])])
#             with con:
#                 con.executemany(sql, data_queues)


# print content of customers table

