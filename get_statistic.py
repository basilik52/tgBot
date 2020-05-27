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
def callback_inline(call):
    with closing(psycopg2.connect(
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
        with connection.cursor() as cursor:
            try:

                if call.message:
                    id_telegram = call.from_user.id
                    check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_user, [int(id_telegram)])
                    for user_id in cursor:
                        id_user = user_id[0]

                    if call.data == 'today':
                        amount_today = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (date(created_at) = current_date) and deleted_at is null'''
                        cursor.execute(amount_today, [int(id_user)])
                        for am_t in cursor:
                            am_tod = am_t[0]
                        if am_tod is not None:
                            bot.send_message(call.message.chat.id, "Сегодня - {} руб.".format(am_tod))
                            amount_today_name = '''SELECT sum(amount), c.name_ru FROM amounts join categories c on amounts.category_id = c.id WHERE user_id = %s and (date(created_at) = current_date) and deleted_at is null group by c.name_ru'''
                            cursor.execute(amount_today_name, [int(id_user)])
                            bot.send_message(call.message.chat.id, "В том числе:")
                            for am_to in cursor:
                                am_today = am_to[0]
                                n_today = am_to[1]
                                bot.send_message(call.message.chat.id, "- {} руб. - {}".format(am_today, n_today))
                        else:
                            bot.send_message(call.message.chat.id, "Сегодня - 0 руб.")
                    elif call.data == 'week':
                        amount_week = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (EXTRACT(WEEK FROM created_at) = EXTRACT(WEEK FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                        cursor.execute(amount_week, [int(id_user)])
                        for am_w in cursor:
                            am_week = am_w[0]
                        if am_week is not None:
                            bot.send_message(call.message.chat.id, "За неделю - {} руб.".format(am_week))
                            amount_week_name = '''SELECT sum(amount), c.name_ru FROM amounts join categories c on amounts.category_id = c.id WHERE user_id = %s and (EXTRACT(WEEK FROM created_at) = EXTRACT(WEEK FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null group by c.name_ru'''
                            cursor.execute(amount_week_name, [int(id_user)])
                            bot.send_message(call.message.chat.id, "В том числе:")
                            for am_we in cursor:
                                amo_week = am_we[0]
                                n_week = am_we[1]
                                bot.send_message(call.message.chat.id, "- {} руб. - {}".format(amo_week, n_week))
                        else:
                            bot.send_message(call.message.chat.id, "За неделю - 0 руб.")
                    elif call.data == 'month':
                        amount_month = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                        cursor.execute(amount_month, [int(id_user)])
                        for am_m in cursor:
                            am_month = am_m[0]
                        if am_month is not None:
                            bot.send_message(call.message.chat.id, "За месяц - {} руб.".format(am_month))
                            amount_month_name = '''SELECT sum(amount), c.name_ru FROM amounts join categories c on amounts.category_id = c.id WHERE user_id = %s and (EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null group by c.name_ru'''
                            cursor.execute(amount_month_name, [int(id_user)])
                            bot.send_message(call.message.chat.id, "В том числе:")
                            for am_mo in cursor:
                                amo_month = am_mo[0]
                                n_month = am_mo[1]
                                bot.send_message(call.message.chat.id, "- {} руб. - {}".format(amo_month, n_month))
                        else:
                            bot.send_message(call.message.chat.id, "За месяц - 0 руб.")
                    elif call.data == 'quarter':
                        amount_quarter = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (EXTRACT(QUARTER FROM created_at) = EXTRACT(QUARTER FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                        cursor.execute(amount_quarter, [int(id_user)])
                        for am_q in cursor:
                            am_quarter = am_q[0]
                        if am_quarter is not None:
                            bot.send_message(call.message.chat.id, "За квартал - {} руб.".format(am_quarter))
                            amount_quarter_name = '''SELECT sum(amount), c.name_ru FROM amounts join categories c on amounts.category_id = c.id WHERE user_id = %s and (EXTRACT(QUARTER FROM created_at) = EXTRACT(QUARTER FROM current_date)) and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null group by c.name_ru'''
                            cursor.execute(amount_quarter_name, [int(id_user)])
                            bot.send_message(call.message.chat.id, "В том числе:")
                            for am_mo in cursor:
                                amo_quarter = am_mo[0]
                                n_quarter = am_mo[1]
                                bot.send_message(call.message.chat.id, "- {} руб. - {}".format(amo_quarter, n_quarter))
                        else:
                            bot.send_message(call.message.chat.id, "За квартал - 0 руб.")
                    elif call.data == 'half':
                        amount_half = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and deleted_at is null and (EXTRACT(QUARTER FROM current_date) <= 2 and EXTRACT(QUARTER FROM created_at) <= 2 and (EXTRACT(QUARTER FROM created_at) <= EXTRACT(QUARTER FROM current_date)) and
                                                 (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)))
                                           or (EXTRACT(QUARTER FROM current_date) >= 3 and EXTRACT(QUARTER FROM created_at) >= 3 and (EXTRACT(QUARTER FROM created_at) <= EXTRACT(QUARTER FROM current_date)) and
                                               (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)))'''
                        cursor.execute(amount_half, [int(id_user)])
                        for am_h in cursor:
                            am_half = am_h[0]
                        if am_half is not None:
                            bot.send_message(call.message.chat.id, "За полгода - {} руб.".format(am_half))
                            amount_half_name = '''SELECT sum(amount), c.name_ru FROM amounts join categories c on amounts.category_id = c.id WHERE user_id = %s and deleted_at is null and (EXTRACT(QUARTER FROM current_date) <= 2 and EXTRACT(QUARTER FROM created_at) <= 2 and (EXTRACT(QUARTER FROM created_at) <= EXTRACT(QUARTER FROM current_date)) and
                                                 (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)))
                                           or (EXTRACT(QUARTER FROM current_date) >= 3 and EXTRACT(QUARTER FROM created_at) >= 3 and (EXTRACT(QUARTER FROM created_at) <= EXTRACT(QUARTER FROM current_date)) and
                                               (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date))) group by c.name_ru'''
                            cursor.execute(amount_half_name, [int(id_user)])
                            bot.send_message(call.message.chat.id, "В том числе:")
                            for am_ha in cursor:
                                amo_half = am_ha[0]
                                n_half = am_ha[1]
                                bot.send_message(call.message.chat.id, "- {} руб. - {}".format(amo_half, n_half))
                        else:
                            bot.send_message(call.message.chat.id, "За полгода - 0 руб.")
                    elif call.data == 'year':
                        amount_year = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null'''
                        cursor.execute(amount_year, [int(id_user)])
                        for am_y in cursor:
                            am_year = am_y[0]
                        if am_year is not None:
                            bot.send_message(call.message.chat.id, "За год - {} руб.".format(am_year))
                            amount_year_name = '''SELECT sum(amount), c.name_ru FROM amounts join categories c on amounts.category_id = c.id WHERE user_id = %s and (EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM current_date)) and deleted_at is null group by c.name_ru'''
                            cursor.execute(amount_year_name, [int(id_user)])
                            bot.send_message(call.message.chat.id, "В том числе:")
                            for am_ye in cursor:
                                amo_year = am_ye[0]
                                n_year = am_ye[1]
                                bot.send_message(call.message.chat.id, "- {} руб. - {}".format(amo_year, n_year))
                        else:
                            bot.send_message(call.message.chat.id, "За год - 0 руб.")

                    # remove inline buttons
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Статистика трат",
                                          reply_markup=None)
            except Exception as e:
                print(repr(e))
        connection.commit()
