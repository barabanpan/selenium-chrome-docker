import os

import telebot
from dotenv import load_dotenv

from bot.db_manager import add_id, get_all_ids
from bot.run import run_selenium_bot
from bot.constants import REMOTE_DRIVER


load_dotenv(os.path.join(os.getcwd(), '.env'))
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
help_text = "/update - update data about stock prices"


@bot.message_handler(commands=["start"])
def start(m, res=False):
    add_id(m.chat.id)
    bot.send_message(m.chat.id, f"{m.chat.id} - start")


@bot.message_handler(commands=["update"])
def update(m, res=False):
    result = run_selenium_bot(REMOTE_DRIVER)
    bot.send_message(m.chat.id, result)


@bot.message_handler(commands=["help"])
def help_(m, res=False):
    bot.send_message(m.chat.id, help_text)


# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     bot.send_message(message.chat.id, 'You wrote: ' + message.text)


def send_to_all(message):
    for chat_row in set(get_all_ids()):
        bot.send_message(chat_row[0], message)
    

bot.polling(none_stop=True, interval=0)
