from typing import Tuple

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from ..domain.entities import Prediction
from ..domain.ports import IntentClassifier


class NaiveBayesClassifier(IntentClassifier):
    __slots__ = ("_pipeline", "_trained")

    def __init__(self) -> None:
        self._pipeline = Pipeline([
            ("vectorizer", CountVectorizer(ngram_range=(1, 2))),
            ("model", MultinomialNB(alpha=0.3)),
        ])
        self._trained = False

    def train(self, samples: Tuple[str, ...], labels: Tuple[str, ...]) -> None:
        self._pipeline.fit(samples, labels)
        self._trained = True

    def predict(self, text: str) -> Prediction:
        if not self._trained:
            raise RuntimeError("Classifier not trained")

        probabilities = self._pipeline.predict_proba([text])[0]
        best_index = probabilities.argmax()
        return Prediction(
            tag=self._pipeline.classes_[best_index],
            confidence=float(probabilities[best_index]),
        )