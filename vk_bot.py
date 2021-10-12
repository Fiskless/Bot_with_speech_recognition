import os
import random
import vk_api as vk
import logging

from dotenv import load_dotenv
from google.cloud import dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger('vk_logger')


class VKLogsHandler(logging.Handler):

    def __init__(self, token, user_id):
        super().__init__()
        self.user_id = user_id
        self.vk_session = vk.VkApi(token=token)

    def emit(self, record):
        log_entry = self.format(record)
        self.messages.send(
            user_id=self.user_id,
            message=log_entry,
            random_id=random.randint(1, 1000)
        )


def detect_intent_texts(event, vk_api, language_code='ru-RU'):

    vk_session_id = str(event.user_id)
    text = event.text
    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, vk_session_id)

    text_input = dialogflow.TextInput(text=text,
                                      language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
    vk_user_id = os.getenv("VK_USER_ID")
    vk_session = vk.VkApi(token=vk_group_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(VKLogsHandler(vk_group_token, vk_user_id))

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detect_intent_texts(event, vk_api)


if __name__ == '__main__':
    main()
