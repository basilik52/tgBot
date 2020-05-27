# -*- coding: utf-8 -*-
import datetime

import psycopg2
import telebot
import config

from contextlib import closing
from telebot import types
from datetime import datetime


bot = telebot.TeleBot(config.TOKEN)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline_admin(call):
    with closing(psycopg2.connect(
            host='ec2-34-202-88-122.compute-1.amazonaws.com',
            user='psfxklbqjdysjc',
            password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
            dbname='daro9jorij2fqh')) as connection:
        with connection.cursor() as cursor:
            try:

                if call.message:
                    check_role = '''SELECT role_id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_role, [int(call.from_user.id)])
                    for role in cursor:
                        role_id = role[0]

                    if role_id == 1:
                        if call.data == 'm_delete':

                            try:
                                query = '''DELETE FROM messages WHERE deleted_at is not null'''
                                cursor.execute(query)
                                bot.send_message(call.message.chat.id,
                                                 'messages с <b>deleted_at is not null</b> удалены.',
                                                 parse_mode='html')
                            except Exception:
                                bot.send_message(call.message.chat.id, 'Нет данных для удаления.')

                        elif call.data == 'a_delete':

                            try:
                                query = '''DELETE FROM amounts WHERE deleted_at is not null'''
                                cursor.execute(query)
                                bot.send_message(call.message.chat.id,
                                                 'amounts с <b>deleted_at is not null</b> удалены.',
                                                 parse_mode='html')
                            except Exception:
                                bot.send_message(call.message.chat.id, 'Нет данных для удаления.')

                        elif call.data == 'u_count':

                            query = '''SELECT count(id) from users'''
                            cursor.execute(query)
                            for user_c in cursor:
                                users_count = user_c[0]
                            bot.send_message(call.message.chat.id, '<b>{}</b> - пользователей'.format(users_count),
                                             parse_mode='html')

                        elif call.data == 'u_username':

                            query2 = '''SELECT username from users'''
                            cursor.execute(query2)
                            for user_n in cursor:
                                users_username = user_n[0]
                                bot.send_message(call.message.chat.id, '@{}\n'.format(users_username),
                                                 parse_mode='html')

                        elif call.data == 'stat':

                            amount_today = '''SELECT sum(amount) FROM amounts WHERE (date(created_at) = current_date) and deleted_at is null'''
                            cursor.execute(amount_today)
                            for am_t in cursor:
                                am_tod = am_t[0]
                            if am_tod is not None:
                                bot.send_message(call.message.chat.id, "Сегодня - {} руб.".format(am_tod))
                            else:
                                bot.send_message(call.message.chat.id, "Сегодня - 0 руб.")

                            amount_week = '''SELECT sum(amount) FROM amounts WHERE (EXTRACT(WEEK FROM created_at) = EXTRACT(WEEK FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                            cursor.execute(amount_week)
                            for am_w in cursor:
                                am_week = am_w[0]
                            if am_week is not None:
                                bot.send_message(call.message.chat.id, "За неделю - {} руб.".format(am_week))
                            else:
                                bot.send_message(call.message.chat.id, "За неделю - 0 руб.")

                            amount_month = '''SELECT sum(amount) FROM amounts WHERE (EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                            cursor.execute(amount_month)
                            for am_m in cursor:
                                am_month = am_m[0]
                            if am_month is not None:
                                bot.send_message(call.message.chat.id, "За месяц - {} руб.".format(am_month))
                            else:
                                bot.send_message(call.message.chat.id, "За месяц - 0 руб.")

                            amount_quarter = '''SELECT sum(amount) FROM amounts WHERE (EXTRACT(QUARTER FROM created_at) = EXTRACT(QUARTER FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                            cursor.execute(amount_quarter)
                            for am_q in cursor:
                                am_quarter = am_q[0]
                            if am_quarter is not None:
                                bot.send_message(call.message.chat.id, "За квартал - {} руб.".format(am_quarter))
                            else:
                                bot.send_message(call.message.chat.id, "За квартал - 0 руб.")

                            amount_half = '''SELECT sum(amount) FROM amounts WHERE deleted_at is null and (EXTRACT(QUARTER FROM current_date) <= 2 and EXTRACT(QUARTER FROM created_at) <= 2 and (EXTRACT(QUARTER FROM created_at) <= EXTRACT(QUARTER FROM current_date)) and
                                                                             (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)))
                                                                       or (EXTRACT(QUARTER FROM current_date) >= 3 and EXTRACT(QUARTER FROM created_at) >= 3 and (EXTRACT(QUARTER FROM created_at) <= EXTRACT(QUARTER FROM current_date)) and
                                                                           (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)))'''
                            cursor.execute(amount_half)
                            for am_h in cursor:
                                am_half = am_h[0]
                            if am_half is not None:
                                bot.send_message(call.message.chat.id, "За полгода - {} руб.".format(am_half))
                            else:
                                bot.send_message(call.message.chat.id, "За полгода - 0 руб.")

                            amount_year = '''SELECT sum(amount) FROM amounts WHERE (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                            cursor.execute(amount_year)
                            for am_y in cursor:
                                am_year = am_y[0]
                            if am_year is not None:
                                bot.send_message(call.message.chat.id, "За год - {} руб.".format(am_year))
                            else:
                                bot.send_message(call.message.chat.id, "За год - 0 руб.")

                    else:
                        bot.send_message(call.message.chat.id,
                                         'Я тебя не совсем понял 🙃\nНажми нужную кнопку меню.')

            except Exception as e:
                print(repr(e))
        connection.commit()
