import os
import random

from google.cloud import dialogflow


def detect_intent_texts(update=None, event=None, language_code='ru-RU'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    if update:
        session_id = str(update.effective_user['id'])
        text_input = dialogflow.TextInput(text=update.message.text,
                                          language_code=language_code)

    if event:
        session_id = str(event.user_id)
        text_input = dialogflow.TextInput(text=event.text,
                                          language_code=language_code)

    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response





