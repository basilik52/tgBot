# -*- coding: utf-8 -*-
import datetime

import psycopg2
import telebot
import config

from contextlib import closing
from telebot import types
from datetime import datetime


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    with closing(psycopg2.connect(
            host='ec2-34-202-88-122.compute-1.amazonaws.com',
            user='psfxklbqjdysjc',
            password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
            dbname='daro9jorij2fqh')) as connection:
        with connection.cursor() as cursor:
            sti = open('static/welcome.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)

            # keyboard
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            item1 = types.KeyboardButton("Удалить сумму")
            item2 = types.KeyboardButton("Добавить сумму")
            item3 = types.KeyboardButton("Обратная связь")
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
            role = 10
            language_code = message.from_user.language_code
            date_start = datetime.now()
            print(user_id, first_name, last_name, username, language_code, date_start)
            check_user = '''SELECT id_telegram FROM users WHERE id_telegram = %s'''
            cursor.execute(check_user, [int(user_id)])
            row = cursor.fetchone()
            if row is None:
                query = '''INSERT INTO users (id_telegram, first_name, last_name, username, role_id, language_code, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
                cursor.execute(query, (
                    int(user_id), str(first_name), str(last_name), str(username), int(role), str(language_code),
                    str(date_start),
                    str(date_start)))
            else:
                print("user - {} exist".format(user_id))
        connection.commit()