import telebot
import os

from dotenv import load_dotenv


load_dotenv(os.path.join(os.getcwd(), '.env'))
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

def send_message(chat_id, message_text):
    bot.send_message(chat_id, message_text)
