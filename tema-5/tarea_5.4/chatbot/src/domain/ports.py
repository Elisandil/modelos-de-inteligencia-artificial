from abc import ABC, abstractmethod
from typing import Tuple

from .entities import Intent, Prediction


class IntentRepository(ABC):
    @abstractmethod
    def load(self) -> Tuple[Intent, ...]: ...


class TextPreprocessor(ABC):
    @abstractmethod
    def process(self, text: str) -> str: ...


class IntentClassifier(ABC):
    @abstractmethod
    def train(self, samples: Tuple[str, ...], labels: Tuple[str, ...]) -> None: ...

    @abstractmethod
    def predict(self, text: str) -> Prediction: ...


class ResponseSelector(ABC):
    @abstractmethod
    def select(self, tag: str) -> str: ...