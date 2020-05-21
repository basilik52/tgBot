# -*- coding: utf-8 -*-
import datetime

import psycopg2
import telebot
import config

from contextlib import closing
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    with closing(psycopg2.connect(
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
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
            date_start = datetime.now()
            print(user_id, first_name, last_name, username, language_code, date_start)
            check_user = '''SELECT id_telegram FROM users WHERE id_telegram = %s'''
            cursor.execute(check_user, [int(user_id)])
            row = cursor.fetchone()
            if row is None:
                query = '''INSERT INTO users (id_telegram, first_name, last_name, username, language_code, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
                cursor.execute(query, (
                    int(user_id), str(first_name), str(last_name), str(username), str(language_code), str(date_start),
                    str(date_start)))
            else:
                print("user - {} exist".format(user_id))
        connection.commit()

@bot.message_handler(commands=["delete"])
def delete(message):
    id_telegram = message.from_user.id
    if id_telegram == 1017018910:
        bot.send_message(message.chat.id, '1 - /messages_delete\n2 - /amounts_delete')
    else:
        bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.message_handler(commands=["messages_delete"])
def messages_delete(message):
    with closing(psycopg2.connect(
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
        with connection.cursor() as cursor:
            id_telegram = message.from_user.id
            if id_telegram == 1017018910:
                try:
                    query = '''DELETE FROM messages WHERE deleted_at is not null'''
                    cursor.execute(query)
                    bot.send_message(message.chat.id, 'messages с <b>deleted_at is not null</b> удалены.',
                                     parse_mode='html')
                except Exception:
                    bot.send_message(message.chat.id, 'Нет данных для удаления.')
            else:
                bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
        connection.commit()


@bot.message_handler(commands=["amounts_delete"])
def amounts_delete(message):
    with closing(psycopg2.connect(
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
        with connection.cursor() as cursor:
            id_telegram = message.from_user.id
            if id_telegram == 1017018910:
                try:
                    query = '''DELETE FROM amounts WHERE deleted_at is not null'''
                    cursor.execute(query)
                    bot.send_message(message.chat.id, 'amounts с <b>deleted_at is not null</b> удалены.',
                                     parse_mode='html')
                except Exception:
                    bot.send_message(message.chat.id, 'Нет данных для удаления.')
            else:
                bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
        connection.commit()


@bot.message_handler(commands=["user"])
def user(message):
    id_telegram = message.from_user.id
    if id_telegram == 1017018910:
        bot.send_message(message.chat.id, '1 - /users_count\n2 - /users_username')
    else:
        bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.message_handler(commands=["users_count"])
def users_count(message):
    with closing(psycopg2.connect(
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
        with connection.cursor() as cursor:
            id_telegram = message.from_user.id
            if id_telegram == 1017018910:
                query = '''SELECT count(id) from users'''
                cursor.execute(query)
                for user_c in cursor:
                    users_count = user_c[0]
                bot.send_message(message.chat.id, '<b>{}</b> - пользователей'.format(users_count),
                                 parse_mode='html')
            else:
                bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
        connection.commit()


@bot.message_handler(commands=["users_username"])
def users_username(message):
    with closing(psycopg2.connect(
            host='ec2-34-198-243-120.compute-1.amazonaws.com',
            user='yrxxtoynomwkrz',
            password='8164a0d936762b96651abde918d0c68c46739338a3f0cef7c8dd01214043b2b3',
            dbname='df9nfputb06mls')) as connection:
        with connection.cursor() as cursor:
            id_telegram = message.from_user.id
            if id_telegram == 1017018910:
                query2 = '''SELECT username from users'''
                cursor.execute(query2)
                for user_n in cursor:
                    users_username = user_n[0]
                    bot.send_message(message.chat.id, '@{}\n'.format(users_username),
                                     parse_mode='html')
            else:
                bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
        connection.commit()
