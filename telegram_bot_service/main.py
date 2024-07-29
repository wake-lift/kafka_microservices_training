import json
import logging
import os
from threading import Thread
from time import localtime, strftime

from kafka import KafkaConsumer
from telegram import Chat, ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

CONSUMER_GROUP: str = 'telegram_bot_consumer_group'
TELEGRAM_BOT_TOPIC: str = 'telegram_bot_topic'

activate_consumer: bool = False


def wake_up(update: Update, context: CallbackContext) -> None:
    """Генерирует начальное приветствие."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = button_shortcut([
        ['Начать прием сообщений'], ['Завершить прием сообщений'],
    ],)
    text = f'Здравствуйте, {name}!'
    send_message(context, chat, text, buttons)


def button_shortcut(button_names: list[list]) -> ReplyKeyboardMarkup:
    """
    Формирует кнопку с указанными полями.
    """
    return ReplyKeyboardMarkup(
        keyboard=button_names,
        resize_keyboard=True
    )


def format_message(msg: str) -> str:
    """Форматирует сообщение в читаемый вид."""
    date = strftime('%Y-%m-%d %H:%M:%S', localtime(int(msg['timestamp'])))
    return (
        f"Дата: {date};\n"
        f"Датчик: {msg['sensor_name']};\n"
        f"Уровень: {msg['level']};\n"
        f"Текст: {msg['log_message']}.\n"
    )


def consumer_loop(context: CallbackContext, chat: Chat):
    global activate_consumer
    consumer = KafkaConsumer(
        # bootstrap_servers=['localhost:29092', 'localhost:39092'],
        bootstrap_servers=['kafka-1:19092', 'kafka-2:19092'],
        group_id=CONSUMER_GROUP
    )
    consumer.subscribe(TELEGRAM_BOT_TOPIC)
    while True:
        for msg in consumer:
            decoded_msg = json.loads(msg.value.decode('utf-8'))
            if activate_consumer:
                send_message(context, chat, format_message(decoded_msg))
                logging.warning('Сообщение отправлено в чат пользователю')
            else:
                consumer.close()
                break


def send_message(
        context: CallbackContext,
        chat: Chat,
        text: str,
        buttons: ReplyKeyboardMarkup = None,
) -> None:
    """
    Отправляет сообщение с указанными текстом и кнопками.
    """
    return context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )


def handle_messages(update: Update, context: CallbackContext) -> None:
    """
    Обработчик текстовых сообщений от пользователя.
    """
    global activate_consumer
    chat = update.effective_chat
    message = update.message.text
    if message == 'Начать прием сообщений':
        buttons = button_shortcut([['Завершить прием сообщений'],])
        text = 'Приступаю к приему сообщений...'
        send_message(context, chat, text, buttons)
        activate_consumer = True
        thread = Thread(target=consumer_loop, args=(context, chat,))
        thread.start()
        logging.warning('Начата работа телеграм-бота по приему сообщений')
    if message == 'Завершить прием сообщений':
        buttons = button_shortcut([['Начать прием сообщений'],])
        text = 'Завершаю прием сообщений...'
        send_message(context, chat, text, buttons)
        activate_consumer = False
        logging.warning('Закончена работа телеграм-бота по приему сообщений')


if __name__ == '__main__':
    updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))
    updater.dispatcher.add_handler(
        CommandHandler(('start',), wake_up)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, handle_messages)
    )
    updater.start_polling()
    updater.idle()
