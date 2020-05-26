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

bot = telebot.TeleBot(config.TOKEN)
amount = 0


@bot.message_handler(commands=["start"])
def commands(message):
    welcome(message)


@bot.message_handler(commands=["delete"])
def commands(message):
    delete(message)


@bot.message_handler(commands=["messages_delete"])
def commands(message):
    messages_delete(message)


@bot.message_handler(commands=["amounts_delete"])
def commands(message):
    amounts_delete(message)


@bot.message_handler(commands=["user"])
def commands(message):
    user(message)


@bot.message_handler(commands=["users_count"])
def commands(message):
    users_count(message)


@bot.message_handler(commands=["users_username"])
def commands(message):
    users_username(message)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == u'О боте':
            bot.send_message(message.chat.id, 'Бот написан на python3. \nversion <b>3.7</b> (21.05.2020)',
                             parse_mode='html')
        elif message.text == u'Добавить сумму':
            with closing(psycopg2.connect(
                    host='ec2-34-198-243-120.compute-1.amazonaws.com',
                    user='yrxxtoynomwkrz',
                    password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
                    dbname='df9nfputb06mls')) as connection:

                with connection.cursor() as cursor:
                    # id_telegram = message.from_user.id
                    check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_user, [int(message.from_user.id)])
                    for user_id in cursor:
                        id_user = user_id[0]

                    try:
                        query = '''DELETE FROM amounts WHERE amount is null and user_id = %s'''
                        cursor.execute(query, [int(id_user)])
                    except Exception as e:
                        print(repr(e))
                connection.commit()
                mag = bot.send_message(message.chat.id,
                                       '<b>Выбери категорию:</b>\nАвтомобиль - /auto\nВсе для дома - /house\nЗдоровье и красота - '
                                       '/beauty\nИскусство - /art\nКоммунальные платежи - /communal\nСвязь и интернет - /internet\n'
                                       'Образование - /education\nОдежда и аксессуары - /clothes\nОтдых и развлечения - /entertainment\n'
                                       'Перевод - /transfer\nКредит - /credit\nПутешествия - /travel\nРестораны и кафе - /cafe\nСупермаркет'
                                       ' - /supermarket\nТранспорт - /transport\nПрочие расходы - /other',
                                       parse_mode='html')

                bot.register_next_step_handler(mag, get_category)

        elif message.text == u'Статистика трат':

            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Сегодня", callback_data='today')
            item2 = types.InlineKeyboardButton("За неделю", callback_data='week')
            item3 = types.InlineKeyboardButton("За месяц", callback_data='month')
            item4 = types.InlineKeyboardButton("За квартал", callback_data='quarter')
            item5 = types.InlineKeyboardButton("За полгода", callback_data='half')
            item6 = types.InlineKeyboardButton("За год", callback_data='year')

            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, 'Выбери период трат:', reply_markup=markup)

        elif message.text == u'Удалить сумму':
            with closing(psycopg2.connect(
                    host='ec2-34-198-243-120.compute-1.amazonaws.com',
                    user='yrxxtoynomwkrz',
                    password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
                    dbname='df9nfputb06mls')) as connection:

                with connection.cursor() as cursor:
                    # id_telegram = message.from_user.id
                    check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_user, [int(message.from_user.id)])
                    for user_id in cursor:
                        id_user = user_id[0]

                    date_delete = datetime.now()

                    query1 = '''DELETE FROM amounts WHERE amount is null and user_id = %s'''
                    cursor.execute(query1, [int(id_user)])

                    print(id_user, date_delete)
                    query = '''SELECT max(id) from amounts where user_id = %s and (date(created_at) = current_date)'''
                    cursor.execute(query, [int(id_user)])
                    for max_id in cursor:
                        id_max = max_id[0]
                        print(max_id[0])
                    print(max_id)

                    try:
                        query = '''DELETE FROM amounts WHERE user_id = %s and id = %s'''
                        cursor.execute(query, (int(id_user), int(id_max)))
                        bot.send_message(message.chat.id, 'Последняя сумма была успешно удалена!')

                        query = '''SELECT date(created_at), amount from amounts where user_id = %s and (date(created_at) = current_date)'''
                        cursor.execute(query, [int(id_user)])
                        for date_amount in cursor:
                            date_c = date_amount[0]
                            amount_a = date_amount[1]
                            bot.send_message(message.chat.id, '{} - {} руб.'.format(date_c, amount_a))
                    except Exception:
                        bot.send_message(message.chat.id, 'Нет данных для удаления.')
                connection.commit()
        elif message.text == u'Обратная связь':
            with closing(psycopg2.connect(
                    host='ec2-34-198-243-120.compute-1.amazonaws.com',
                    user='yrxxtoynomwkrz',
                    password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
                    dbname='df9nfputb06mls')) as connection:

                with connection.cursor() as cursor:
                    id_telegram = message.from_user.id
                    if id_telegram == 1017018910:
                        query = '''SELECT message from messages where checked is null and deleted_at is null'''
                        cursor.execute(query)
                        for m_c in cursor:
                            msg_chck = m_c[0]
                            bot.send_message(message.chat.id, '- {}\n'.format(msg_chck), parse_mode='html')
                    else:
                        mag = bot.send_message(message.chat.id,
                                               'Дорогой {0.first_name}, спасибо, что пользуешься ботом  - помошником! '
                                               'В данном разделе ты можешь оставить отзыв о данном боте, заказать своевого бота на python или заказать рекламу (Оставляйте свои данные). Пиши:'.format(
                                                   message.from_user), parse_mode='html')
                        bot.register_next_step_handler(mag, get_message)
                connection.commit()
        else:
            bot.send_message(message.chat.id, 'Я тебя не совсем понял 🙃\nНажми нужную кнопку меню.')


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
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
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
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
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
