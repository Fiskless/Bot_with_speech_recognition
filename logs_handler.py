import logging
import random


class CustomLogsHandler(logging.Handler):

    def __init__(self, chat_id, bot, social_network):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot
        self.social_network = social_network

    def emit(self, record):
        log_entry = self.format(record)
        if self.social_network == 'telegram':
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        elif self.social_network == 'vkontakte':
            self.messages.send(
                user_id=self.user_id,
                message=log_entry,
                random_id=random.randint(1, 1000)
            )