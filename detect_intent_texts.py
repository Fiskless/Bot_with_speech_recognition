import os

from google.cloud import dialogflow


def detect_intent_texts(session_id, text_input, language_code='ru-RU'):

    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response





