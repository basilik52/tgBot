# -*- coding: utf-8 -*-
import datetime

import psycopg2
import telebot
import config

from contextlib import closing
from telebot import types
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def get_buttons(message):
    if message.chat.type == 'private':
        if message.text == u'О боте':
            bot.send_message(message.chat.id, 'Бот написан на python3. \nversion <b>3.7</b> (21.05.2020)',
                             parse_mode='html')
            with closing(psycopg2.connect(
                    host='ec2-34-198-243-120.compute-1.amazonaws.com',
                    user='yrxxtoynomwkrz',
                    password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
                    dbname='df9nfputb06mls')) as connection:
                with connection.cursor() as cursor:
                    check_role = '''SELECT role_id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_role, [int(message.from_user.id)])
                    role_id = cursor.fetchone()
                    if role_id == 1:
                        markup_admin = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton("Messages delete", callback_data='m_delete')
                        item2 = types.InlineKeyboardButton("Amounts delete", callback_data='a_delete')
                        item3 = types.InlineKeyboardButton("Users count", callback_data='u_count')
                        item4 = types.InlineKeyboardButton("Users username", callback_data='u_username')
                        markup_admin.add(item1, item2, item3, item4)
                connection.commit()
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
