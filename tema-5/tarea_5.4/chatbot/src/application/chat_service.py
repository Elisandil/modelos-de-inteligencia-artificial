from ..domain.entities import ChatMessage
from ..domain.ports import IntentClassifier, ResponseSelector, TextPreprocessor

_LOW_CONFIDENCE_REPLY = "I don't understand."
_CONFIDENCE_THRESHOLD = 0.35


class ChatService:
    __slots__ = ("_preprocessor", "_classifier", "_selector")

    def __init__(
        self,
        preprocessor: TextPreprocessor,
        classifier: IntentClassifier,
        selector: ResponseSelector,
    ) -> None:
        self._preprocessor = preprocessor
        self._classifier = classifier
        self._selector = selector

    def reply(self, message: ChatMessage) -> str:
        normalized = self._preprocessor.process(message.text)
        if not normalized:
            return _LOW_CONFIDENCE_REPLY

        prediction = self._classifier.predict(normalized)
        if prediction.confidence < _CONFIDENCE_THRESHOLD:
            return _LOW_CONFIDENCE_REPLY

        return self._selector.select(prediction.tag)