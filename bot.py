# -*- coding: utf-8 -*-
import datetime
import psycopg2
import telebot
from psycopg2.extras import DictCursor

import config

from telebot import types
from datetime import datetime
from contextlib import closing
from command import *
from get_button import *
from get_statistic import *
from get_admin import *

bot = telebot.TeleBot(config.TOKEN)
amount = 0


@bot.message_handler(commands=["start"])
def commands(message):
    welcome(message)


@bot.message_handler(content_types=['text'])
def buttons(message):
    get_buttons(message)


@bot.callback_query_handler(func=lambda call: True)
def statistic(call):
    callback_inline(call)


@bot.callback_query_handler(func=lambda call: True)
def admin(call):
    callback_inline_admin(call)


def get_message(message):
    with closing(psycopg2.connect(
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
        with connection.cursor() as cursor:
            id_telegram = message.from_user.id
            check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
            cursor.execute(check_user, [int(id_telegram)])
            for user_id in cursor:
                id_user = user_id[0]
            message_review = message.text

            date_start = datetime.now()

            print(id_user, message_review, date_start)
            try:
                query = '''INSERT INTO messages (user_id, message, created_at, updated_at) VALUES (%s,%s,%s,%s)'''
                cursor.execute(query, (
                    int(id_user), str(message_review), str(date_start), str(date_start)))

                bot.send_message(message.chat.id, 'Спасибо за сообщение!')
            except Exception:
                bot.send_message(message.chat.id, 'Слишком длинное сообщение :(',
                                 parse_mode='html')

        connection.commit()


def get_category(message):
    with closing(psycopg2.connect(
            host='ec2-34-202-88-122.compute-1.amazonaws.com',
            user='psfxklbqjdysjc',
            password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
            dbname='daro9jorij2fqh')) as connection:
        with connection.cursor() as cursor:
            try:
                id_telegram = message.from_user.id
                check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                cursor.execute(check_user, [int(id_telegram)])
                for user_id in cursor:
                    id_user = user_id[0]
                    print(id_user)
                print(id_user)
                category = message.text
                print(category)
                check_category = '''SELECT id FROM categories WHERE name = %s'''
                cursor.execute(check_category, (category,))
                for check_c in cursor:
                    check_categ = check_c[0]
                    print(check_categ)
                print(check_categ)
                date_start = datetime.now()

                query = '''INSERT INTO amounts (user_id, category_id, created_at, updated_at) VALUES (%s,%s,%s,%s)'''
                cursor.execute(query, (
                    int(id_user), int(check_categ), str(date_start), str(date_start)))

                mag = bot.send_message(message.chat.id, 'Введите сумму <b>без</b> копеек:', parse_mode='html')
                bot.register_next_step_handler(mag, get_amount)
            except Exception:
                msg = bot.send_message(message.chat.id,
                                       'Упс.. Нет такой категории. <b>Попробуйте снова.</b>',
                                       parse_mode='html')
                bot.register_next_step_handler(msg, get_category)
        connection.commit()


def get_amount(message):
    with closing(psycopg2.connect(
            host='ec2-34-202-88-122.compute-1.amazonaws.com',
            user='psfxklbqjdysjc',
            password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
            dbname='daro9jorij2fqh')) as connection:
        with connection.cursor() as cursor:
            try:
                global amount
                id_telegram = message.from_user.id
                check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                cursor.execute(check_user, [int(id_telegram)])
                for user_id in cursor:
                    id_user = user_id[0]

                amount = int(message.text)

                date_start = datetime.now()

                print(id_user, amount, date_start)

                serch_user_category = '''SELECT id FROM amounts WHERE id = (SELECT max(am.id) from amounts am where am.user_id = %s and am.amount is null)'''
                cursor.execute(serch_user_category, [int(id_user)])
                for id_am in cursor:
                    am_id = id_am[0]

                query = '''UPDATE amounts SET amount = %s, updated_at = %s where user_id = %s and id = %s'''
                cursor.execute(query, (int(amount), str(date_start), int(id_user), int(am_id)))

                category_name = '''select c.name_ru 
                from amounts a join categories c on a.category_id = c.id
                where a.user_id = %s and a.category_id is not null 
                and a.id = (select max(id) from amounts where user_id = %s and category_id is not null)'''
                cursor.execute(category_name, (int(id_user), int(id_user)))
                for name_c in cursor:
                    name_ru = name_c[0]

                bot.send_message(message.chat.id, 'Добавлена сумма - {} руб. в категорию: {}'.format(amount, name_ru))

                print('t_id - {} | amount - {}'.format(message.from_user.id, amount))

            except Exception:
                msg = bot.send_message(message.chat.id,
                                       'Упс.. Должно быть целое числовое значение. <b>Попробуйте снова.</b>',
                                       parse_mode='html')
                bot.register_next_step_handler(msg, get_amount)
        connection.commit()




# RUN
# while True:
#     try:
#         bot.polling(none_stop=True)
#     except:
#         time.sleep(5)
if __name__ == '__main__':
    bot.polling(none_stop=True)
# bot.infinity_polling(True)
# while True:
#     try:
#         bot.polling(none_stop=True)
#
#     except Exception as e:
#         telebot.logger.error(e)  # или просто print(e) если у вас логгера нет,
#         # или import traceback; traceback.print_exc() для печати полной инфы
#         time.sleep(15)
# bot = telebot.TeleBot(extras.token, threaded=False)
