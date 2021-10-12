import os
import random

from google.cloud import dialogflow


def detect_intent_texts(update, context, social_network='telegram', language_code='ru-RU'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    if social_network == 'telegram':
        session_id = str(update.effective_user['id'])
        text_input = dialogflow.TextInput(text=update.message.text,
                                          language_code=language_code)

    elif social_network == 'vkontakte':
        session_id = str(update.user_id)
        text_input = dialogflow.TextInput(text=update.text,
                                          language_code=language_code)

    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)


    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if social_network == 'telegram':
        context.bot.send_message(chat_id=update.effective_user['id'],
                                 text=response.query_result.fulfillment_text)

    elif social_network == 'vkontakte':
        if not response.query_result.intent.is_fallback:
            context.messages.send(
                user_id=update.user_id,
                message=response.query_result.fulfillment_text,
                random_id=random.randint(1, 1000)
            )




