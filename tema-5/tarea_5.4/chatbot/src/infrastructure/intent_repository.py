import json
from pathlib import Path
from typing import Tuple

from ..domain.entities import Intent
from ..domain.ports import IntentRepository


class JsonIntentRepository(IntentRepository):
    __slots__ = ("_path",)

    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> Tuple[Intent, ...]:
        with self._path.open(encoding="utf-8") as f:
            raw = json.load(f)

        return tuple(
            Intent(
                tag=item["tag"],
                patterns=tuple(item["patterns"]),
                responses=tuple(item["responses"]),
            )
            for item in raw["intents"]
        )