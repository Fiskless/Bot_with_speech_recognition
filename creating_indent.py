import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    project_id = os.getenv('DIALOG_FLOW_PROJECT_ID')

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    load_dotenv()

    with open("questions.json", "r") as file:
        questions = json.load(file)

    for question in questions:
        questions_from_user = questions[question]['questions']
        answer_to_user = questions[question]['answer']
        create_intent(question, questions_from_user, [answer_to_user])


if __name__ == '__main__':
    main()
