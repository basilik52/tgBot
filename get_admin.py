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
                    role_id = cursor.fetchone()
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

                    else:
                        bot.send_message(call.message.chat.id,
                                         'Я тебя не совсем понял 🙃\nНажми нужную кнопку меню.')

                    # remove inline buttons
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="О боте",
                                          reply_markup=None)
            except Exception as e:
                print(repr(e))
        connection.commit()
