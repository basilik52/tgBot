from command import *
# from get_button import *
from get_statistic import *
from get_admin import *

bot = telebot.TeleBot(config.TOKEN)
amount = 0


@bot.message_handler(commands=["start"])
def commands(message):
    welcome(message)


# @bot.message_handler(content_types=['text'])
# def buttons(message):
#     get_buttons(message)


# @bot.callback_query_handler(func=lambda call: True)
# def admin(call):
#     callback_inline_admin(call)
#
#
# def statistic(call):
#     callback_inline(call)


@bot.message_handler(content_types=['text'])
def get_buttons(message):
    if message.chat.type == 'private':

        if message.text == u'О боте':
            bot.send_message(message.chat.id, 'Бот написан на python3. \nversion <b>3.7</b> (21.05.2020)',
                             parse_mode='html')
            with closing(psycopg2.connect(
                    host='ec2-34-202-88-122.compute-1.amazonaws.com',
                    user='psfxklbqjdysjc',
                    password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
                    dbname='daro9jorij2fqh')) as connection:
                with connection.cursor() as cursor:
                    check_role = '''SELECT role_id FROM users WHERE id_telegram = %s'''
                    cursor.execute(check_role, [int(message.from_user.id)])
                    for role in cursor:
                        role_id = role[0]

                    if role_id == 1:
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton("Messages delete", callback_data='m_delete')
                        item2 = types.InlineKeyboardButton("Amounts delete", callback_data='a_delete')
                        item3 = types.InlineKeyboardButton("Users count", callback_data='u_count')
                        item4 = types.InlineKeyboardButton("Users username", callback_data='u_username')
                        markup.add(item1, item2, item3, item4)
                        bot.send_message(message.chat.id, 'Меню администратора:', reply_markup=markup)
                connection.commit()

        elif message.text == u'Добавить сумму':
            with closing(psycopg2.connect(
                    host='ec2-34-202-88-122.compute-1.amazonaws.com',
                    user='psfxklbqjdysjc',
                    password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
                    dbname='daro9jorij2fqh')) as connection:

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
                    host='ec2-34-202-88-122.compute-1.amazonaws.com',
                    user='psfxklbqjdysjc',
                    password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
                    dbname='daro9jorij2fqh')) as connection:

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
                    host='ec2-34-202-88-122.compute-1.amazonaws.com',
                    user='psfxklbqjdysjc',
                    password='eaf1f4c9415008833090228825842986dcac8e6e269b1c9d430b7814a5f9ea97',
                    dbname='daro9jorij2fqh')) as connection:

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



if __name__ == '__main__':
    bot.polling(none_stop=True)
