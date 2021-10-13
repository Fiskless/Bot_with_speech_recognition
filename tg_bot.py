import os
import logging
import telegram

from detect_intent_texts import detect_intent_texts
from dotenv import load_dotenv
from logs_handler import CustomLogsHandler
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext
)


logger = logging.getLogger('tg_logger')


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    context.bot.send_message(chat_id=update.effective_user['id'],
                             text='Здравствуйте')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def main() -> None:
    """Start the bot."""
    load_dotenv()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    updater = Updater(bot_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(CustomLogsHandler(chat_id,
                                        telegram.Bot(token=bot_token),
                                        'telegram'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_intent_texts))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
