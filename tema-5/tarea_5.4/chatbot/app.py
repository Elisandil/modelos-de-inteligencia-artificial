from pathlib import Path

from flask import Flask

from src.application.chat_service import ChatService
from src.infrastructure.classifier import NaiveBayesClassifier
from src.infrastructure.intent_repository import JsonIntentRepository
from src.infrastructure.preprocessor import SpacyPreprocessor
from src.infrastructure.response_selector import RandomResponseSelector
from src.presentation.controllers import build_blueprint

_SPACY_MODEL = "en_core_web_sm"
_INTENTS_PATH = Path(__file__).parent / "data" / "intents.json"


def create_app() -> Flask:
    intents = JsonIntentRepository(_INTENTS_PATH).load()
    preprocessor = SpacyPreprocessor.from_model(_SPACY_MODEL)

    samples, labels = zip(*(
        (preprocessor.process(pattern), intent.tag)
        for intent in intents
        for pattern in intent.patterns
    ))

    classifier = NaiveBayesClassifier()
    classifier.train(samples, labels)

    service = ChatService(
        preprocessor=preprocessor,
        classifier=classifier,
        selector=RandomResponseSelector(intents),
    )

    app = Flask(__name__)
    app.register_blueprint(build_blueprint(service))
    return app


if __name__ == "__main__":
    create_app().run(debug=True)