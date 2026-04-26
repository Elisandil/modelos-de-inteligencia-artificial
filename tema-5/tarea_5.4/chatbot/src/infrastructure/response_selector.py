import random
from typing import Dict, Tuple

from ..domain.entities import Intent
from ..domain.ports import ResponseSelector

_FALLBACK = "I don't understand."


class RandomResponseSelector(ResponseSelector):
    __slots__ = ("_responses_by_tag",)

    def __init__(self, intents: Tuple[Intent, ...]) -> None:
        self._responses_by_tag: Dict[str, Tuple[str, ...]] = {
            intent.tag: intent.responses for intent in intents
        }

    def select(self, tag: str) -> str:
        responses = self._responses_by_tag.get(tag)
        return random.choice(responses) if responses else _FALLBACK