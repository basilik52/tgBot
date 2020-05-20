# -*- coding: utf-8 -*-
import datetime
import time
import psycopg2
import telebot
from psycopg2 import extras

import config

from telebot import types
from datetime import datetime
from psycopg2.extras import DictCursor
from contextlib import closing
from telebot import apihelper



bot = telebot.TeleBot(config.TOKEN)
amount = 0


@bot.message_handler(commands=['start'])
def welcome(message):
    with closing(psycopg2.connect(
            host='ec2-54-86-170-8.compute-1.amazonaws.com',
            user='xblukmphspyoak',
            password='eb7d8b9e12313c121ad00651d0cd6791473381105d9a04c3116e5aaf1356bd6f',
            dbname='d2iaoufpucitsq',
            port='5432',
            charset='utf8mb4',
            cursorclass=DictCursor)) as connection:
        with connection.cursor() as cursor:
            sti = open('static/welcome.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)

            # keyboard
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            item1 = types.KeyboardButton("Удалить сумму")
            item2 = types.KeyboardButton("Добавить сумму")
            item3 = types.KeyboardButton("Реклама/отзыв")
            item4 = types.KeyboardButton("Статистика трат")
            item5 = types.KeyboardButton("О боте")

            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id,
                             "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь тебе узнать свои траты за определенное время..".format(
                                 message.from_user, bot.get_me()),
                             parse_mode='html', reply_markup=markup)

            user_id = message.from_user.id
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username
            language_code = message.from_user.language_code
            date_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(user_id, first_name, last_name, username, language_code, date_start)
            check_user = '''SELECT id_telegram FROM users WHERE id_telegram = %s'''
            cursor.execute(check_user, int(user_id))
            row = cursor.fetchone()
            if row is None:
                query = '''INSERT INTO users (id_telegram, first_name, last_name, username, language_code, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
                cursor.execute(query, (
                    int(user_id), str(first_name), str(last_name), str(username), str(language_code), str(date_start),
                    str(date_start)))
            else:
                print("user - {} exist".format(user_id))
        connection.commit()


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == u'О боте':
            bot.send_message(message.chat.id, 'Бот написан на python3. \nversion <b>2.3</b> (19.05.2020)', parse_mode='html')
        elif message.text == u'Добавить сумму':

            # markup_category = types.InlineKeyboardMarkup(row_width=2)
            # category1 = types.InlineKeyboardButton("Автомобиль", callback_data='car')
            # category2 = types.InlineKeyboardButton("Все для дома", callback_data='transfer')
            # category3 = types.InlineKeyboardButton("Здоровье и красота", callback_data='transfer')
            # category4 = types.InlineKeyboardButton("Искусство", callback_data='art')
            # category5 = types.InlineKeyboardButton("Коммунальные платежи", callback_data='transfer')
            # category6 = types.InlineKeyboardButton("Связь и интернет", callback_data='internet')
            # category7 = types.InlineKeyboardButton("Образование", callback_data='transfer')
            # category8 = types.InlineKeyboardButton("Одежда и аксессуары", callback_data='transfer')
            # category9 = types.InlineKeyboardButton("Отдых и развлечения", callback_data='transfer')
            # category10 = types.InlineKeyboardButton("Перевод", callback_data='transfer')
            # category11 = types.InlineKeyboardButton("Кредит", callback_data='credit')
            # category12 = types.InlineKeyboardButton("Путешествие", callback_data='travel')
            # category13 = types.InlineKeyboardButton("Рестораны и кафе", callback_data='cafe')
            # category14 = types.InlineKeyboardButton("Супермаркеты", callback_data='supermarket')
            # category15 = types.InlineKeyboardButton("Транспорт", callback_data='transport')
            # category16 = types.InlineKeyboardButton("Прочие расходы", callback_data='other')
            #
            # markup_category.add(category1, category2, category3, category4, category5, category6, category7, category8,
            #                     category9, category10, category11, category12, category13, category14, category15, category16)
            #
            # bot.send_message(message.chat.id, 'Выбери категорию:', reply_markup=markup_category)

            mag = bot.send_message(message.chat.id, 'Введите сумму <b>без</b> копеек:', parse_mode='html')
            bot.register_next_step_handler(mag, get_amount)


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
                    host='ec2-54-86-170-8.compute-1.amazonaws.com',
                    user='xblukmphspyoak',
                    password='eb7d8b9e12313c121ad00651d0cd6791473381105d9a04c3116e5aaf1356bd6f',
                    dbname='d2iaoufpucitsq',
                    charset='utf8mb4',
                    cursorclass=DictCursor)) as connection:

                with connection.cursor() as cursor:
                    id_telegram = message.from_user.id
                    check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_user, int(id_telegram))
                    for user_id in cursor:
                        id_user = user_id['id']
                    date_delete = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    print(id_user, date_delete)
                    query = '''SELECT max(id) from amounts where user_id = %s '''
                    cursor.execute(query, (int(id_user)))
                    for max_id in cursor:
                        id_max = max_id['max(id)']
                        print(id_max)
                    query = '''SELECT deleted_at from amounts where user_id = %s and id = (select max(id) from amounts where user_id = %s)'''
                    cursor.execute(query, (int(id_user), int(id_user)))

                    for d_l in cursor:
                        del_last = d_l['deleted_at']
                        print(del_last)
                    try:
                        if del_last is None:
                            query = '''UPDATE amounts SET deleted_at = %s, updated_at = %s where user_id = %s and id = %s'''
                            cursor.execute(query, (
                                str(date_delete), str(date_delete), int(id_user), int(id_max)))
                            bot.send_message(message.chat.id, 'Последняя сумма была успешно удалена!')
                        else:
                            bot.send_message(message.chat.id, 'Сумма уже удалена.')
                    except Exception:
                        bot.send_message(message.chat.id, 'Нет данных для удаления.')
                connection.commit()
        elif message.text == u'Реклама/отзыв':
            with closing(psycopg2.connect(
                    host='ec2-54-86-170-8.compute-1.amazonaws.com',
                    user='xblukmphspyoak',
                    password='eb7d8b9e12313c121ad00651d0cd6791473381105d9a04c3116e5aaf1356bd6f',
                    dbname='d2iaoufpucitsq',
                    charset='utf8mb4',
                    cursorclass=DictCursor)) as connection:

                with connection.cursor() as cursor:
                    id_telegram = message.from_user.id
                    if id_telegram == 1017018910:
                        query = '''SELECT message from messages where checked is null and deleted_at is null'''
                        cursor.execute(query)
                        for m_c in cursor:
                            msg_chck = m_c['message']
                            bot.send_message(message.chat.id, '- {}\n'.format(msg_chck), parse_mode='html')
                    else:
                        mag = bot.send_message(message.chat.id,
                                               'Дорогой {0.first_name}, спасибо, что пользуешься ботом  - помошником! '
                                               'В данном разделе ты можешь оставить отзыв о данном боте, заказать своевого бота на python или заказать рекламу (Оставляйте свои данные). Пиши:'.format(
                                                   message.from_user), parse_mode='html')
                        bot.register_next_step_handler(mag, get_message)
                connection.commit()
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


def get_message(message):
    with closing(psycopg2.connect(
            host='ec2-54-86-170-8.compute-1.amazonaws.com',
            user='xblukmphspyoak',
            password='eb7d8b9e12313c121ad00651d0cd6791473381105d9a04c3116e5aaf1356bd6f',
            dbname='d2iaoufpucitsq',
            charset='utf8mb4',
            cursorclass=DictCursor)) as connection:
        with connection.cursor() as cursor:
            id_telegram = message.from_user.id
            check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
            cursor.execute(check_user, int(id_telegram))
            for user_id in cursor:
                id_user = user_id['id']
            message_review = message.text

            date_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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


def get_amount(message):
    with closing(psycopg2.connect(
            host='ec2-54-86-170-8.compute-1.amazonaws.com',
            user='xblukmphspyoak',
            password='eb7d8b9e12313c121ad00651d0cd6791473381105d9a04c3116e5aaf1356bd6f',
            dbname='d2iaoufpucitsq',
            charset='utf8mb4',
            cursorclass=DictCursor)) as connection:
        with connection.cursor() as cursor:

            try:
                # categoryId = '''SELECT id FROM categories WHERE name_translate = %s'''
                # cursor.execute(categoryId, str(call.data))
                global amount
                id_telegram = message.from_user.id
                check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                cursor.execute(check_user, int(id_telegram))
                for user_id in cursor:
                    id_user = user_id['id']
                amount = int(message.text)

                date_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                print(id_user, amount, date_start)

                query = '''INSERT INTO amounts (user_id, amount, created_at, updated_at) VALUES (%s,%s,%s,%s)'''
                cursor.execute(query, (
                    int(id_user), int(amount), str(date_start), str(date_start)))

                bot.send_message(message.chat.id, 'Добавлена сумма - {} руб.'.format(amount))
                print('t_id - {} | amount - {}'.format(message.from_user.id, amount))

            except Exception:
                msg = bot.send_message(message.chat.id,
                                       'Упс.. Должно быть целое числовое значение. <b>Попробуйте снова.</b>',
                                       parse_mode='html')
                # bot.register_next_step_handler(msg, get_amount)
        connection.commit()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    with closing(psycopg2.connect(
            host='ec2-54-86-170-8.compute-1.amazonaws.com',
            user='xblukmphspyoak',
            password='eb7d8b9e12313c121ad00651d0cd6791473381105d9a04c3116e5aaf1356bd6f',
            dbname='d2iaoufpucitsq',
            charset='utf8mb4',
            cursorclass=DictCursor)) as connection:
        with connection.cursor() as cursor:
            try:

                if call.message:
                    id_telegram = call.from_user.id
                    check_user = '''SELECT id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_user, int(id_telegram))
                    for user_id in cursor:
                        id_user = user_id['id']

                    if call.data == 'today':
                        amount_today = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (date(created_at) = current_date) and deleted_at is null'''
                        cursor.execute(amount_today, int(id_user))
                        for am_t in cursor:
                            am_tod = am_t['sum(amount)']
                        if am_tod is not None:
                            bot.send_message(call.message.chat.id, "Сегодня - {} руб.".format(am_tod))
                        else:
                            bot.send_message(call.message.chat.id, "Сегодня - 0 руб.")
                    elif call.data == 'week':
                        amount_week = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (week(created_at) = week(current_date)) and (year(created_at) = year(current_date)) and deleted_at is null'''
                        cursor.execute(amount_week, int(id_user))
                        for am_w in cursor:
                            am_week = am_w['sum(amount)']
                        if am_week is not None:
                            bot.send_message(call.message.chat.id, "За неделю - {} руб.".format(am_week))
                        else:
                            bot.send_message(call.message.chat.id, "За неделю - 0 руб.")
                    elif call.data == 'month':
                        amount_month = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (month(created_at) = month(current_date)) and (year(created_at) = year(current_date)) and deleted_at is null'''
                        cursor.execute(amount_month, int(id_user))
                        for am_m in cursor:
                            am_month = am_m['sum(amount)']
                        if am_month is not None:
                            bot.send_message(call.message.chat.id, "За месяц - {} руб.".format(am_month))
                        else:
                            bot.send_message(call.message.chat.id, "За месяц - 0 руб.")
                    elif call.data == 'quarter':
                        amount_quarter = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (QUARTER(created_at) = QUARTER(current_date)) and (year(created_at) = year(current_date)) and deleted_at is null'''
                        cursor.execute(amount_quarter, int(id_user))
                        for am_q in cursor:
                            am_quarter = am_q['sum(amount)']
                        if am_quarter is not None:
                            bot.send_message(call.message.chat.id, "За квартал - {} руб.".format(am_quarter))
                        else:
                            bot.send_message(call.message.chat.id, "За квартал - 0 руб.")
                    elif call.data == 'half':
                        amount_half = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and deleted_at is null and (QUARTER(current_date) <= 2 and QUARTER(created_at) <= 2 and (QUARTER(created_at) <= QUARTER(current_date)) and
                                                 (year(created_at) = year(current_date)))
                                           or (QUARTER(current_date) >= 3 and QUARTER(created_at) >= 3 and (QUARTER(created_at) <= QUARTER(current_date)) and
                                               (year(created_at) = year(current_date)))'''
                        cursor.execute(amount_half, int(id_user))
                        for am_h in cursor:
                            am_half = am_h['sum(amount)']
                        if am_half is not None:
                            bot.send_message(call.message.chat.id, "За полгода - {} руб.".format(am_half))
                        else:
                            bot.send_message(call.message.chat.id, "За полгода - 0 руб.")
                    elif call.data == 'year':
                        amount_year = '''SELECT sum(amount) FROM amounts WHERE user_id = %s and (year(created_at) = year(current_date)) and deleted_at is null'''
                        cursor.execute(amount_year, int(id_user))
                        for am_y in cursor:
                            am_year = am_y['sum(amount)']
                        if am_year is not None:
                            bot.send_message(call.message.chat.id, "За год - {} руб.".format(am_year))
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