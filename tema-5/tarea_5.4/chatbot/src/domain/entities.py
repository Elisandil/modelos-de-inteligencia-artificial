from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class Intent:
    tag: str
    patterns: Tuple[str, ...]
    responses: Tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Prediction:
    tag: str
    confidence: float


@dataclass(frozen=True, slots=True)
class ChatMessage:
    text: str