import os
import vk_api as vk
import logging

from dotenv import load_dotenv
from detect_intent_texts import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType
from logs_handler import CustomLogsHandler


logger = logging.getLogger('vk_logger')


def main():
    load_dotenv()
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
    vk_user_id = os.getenv("VK_USER_ID")
    vk_session = vk.VkApi(token=vk_group_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(CustomLogsHandler(vk_user_id,
                                        vk.VkApi(token=vk_group_token),
                                        'vkontakte'))

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detect_intent_texts(event, vk_api, 'vkontakte')


if __name__ == '__main__':
    main()
