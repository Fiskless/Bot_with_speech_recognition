import os
import logging

from google.cloud import dialogflow
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    context.bot.send_message(chat_id=user['id'], text='Здравствуйте')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def detect_intent_texts(update: Update, context: CallbackContext, language_code='ru-RU'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    user = update.effective_user
    session_id = str(user['id'])
    text = update.message.text
    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text,
                                      language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    context.bot.send_message(chat_id=user['id'], text=response.query_result.fulfillment_text)


def main() -> None:
    """Start the bot."""
    load_dotenv()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(bot_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_intent_texts))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
