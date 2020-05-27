from command import *

from get_statistic import *
from get_admin import *

bot = telebot.TeleBot(config.TOKEN)
amount = 0


@bot.message_handler(commands=["start"])
def commands(message):
    welcome(message)






@bot.callback_query_handler(func=lambda call: True)
def admin(call):
    callback_inline_admin(call)


def statistic(call):
    callback_inline(call)


if __name__ == '__main__':
    bot.polling(none_stop=True)
