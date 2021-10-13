import os
import vk_api as vk
import logging
import random

from dotenv import load_dotenv
from detect_intent_texts import detect_intent_texts
from logs_handler import CustomLogsHandler
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger('vk_logger')


def main():
    load_dotenv()
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
    vk_user_id = os.getenv("VK_USER_ID")
    vk_session = vk.VkApi(token=vk_group_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(CustomLogsHandler(vk_user_id, None, vk_group_token))

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            response = detect_intent_texts(None, event)
            if not response.query_result.intent.is_fallback:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=response.query_result.fulfillment_text,
                    random_id=random.randint(1, 1000)
                )


if __name__ == '__main__':
    main()
