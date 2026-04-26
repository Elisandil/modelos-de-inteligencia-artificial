import spacy
from spacy.language import Language

from ..domain.ports import TextPreprocessor

_IRRELEVANT_POS = frozenset({"DET", "CCONJ", "SCONJ", "AUX", "PUNCT", "SPACE"})


class SpacyPreprocessor(TextPreprocessor):
    __slots__ = ("_nlp",)

    def __init__(self, nlp: Language) -> None:
        self._nlp = nlp

    @classmethod
    def from_model(cls, model_name: str) -> "SpacyPreprocessor":
        return cls(spacy.load(model_name, disable=["ner", "parser"]))

    def process(self, text: str) -> str:
        return " ".join(
            token.lemma_.lower()
            for token in self._nlp(text)
            if not token.is_stop
            and not token.is_space
            and token.pos_ not in _IRRELEVANT_POS
            and token.lemma_.strip()
        )