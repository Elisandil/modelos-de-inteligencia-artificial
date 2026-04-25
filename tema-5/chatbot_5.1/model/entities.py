# ============================================================
# models/entities.py — Entidades del dominio (dataclasses)
# ============================================================
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Intent:
    """
    Representa una intención reconocida por el chatbot.

    Tabla: intents
    Columnas: id (PK), name (UNIQUE)
    """
    name: str
    id: Optional[int] = field(default=None)

    def __str__(self) -> str:
        return f"Intent(id={self.id}, name='{self.name}')"


@dataclass
class Keyword:
    """
    Palabra o frase clave asociada a una intención.

    Tabla: keywords
    Columnas: id (PK), intent_id (FK → intents.id), keyword
    
    3NF:
      - keyword depende únicamente de su PK (id).
      - intent_id no crea dependencia transitiva (es FK directa).
    """
    intent_id: int
    keyword: str
    id: Optional[int] = field(default=None)

    def __str__(self) -> str:
        return f"Keyword(id={self.id}, intent_id={self.intent_id}, keyword='{self.keyword}')"


@dataclass
class Response:
    """
    Respuesta asociada a una intención.

    Tabla: responses
    Columnas: id (PK), intent_id (FK → intents.id), response_text
    
    3NF:
      - response_text depende únicamente de la PK (id).
      - intent_id actúa como FK, sin dependencias transitivas.
    """
    intent_id: int
    response_text: str
    id: Optional[int] = field(default=None)

    def __str__(self) -> str:
        return f"Response(id={self.id}, intent_id={self.intent_id})"


@dataclass
class Conversation:
    """
    Registro de cada intercambio usuario ↔ chatbot.

    Tabla: conversations
    Columnas: id (PK), created_at, user_input,
              intent_id (FK → intents.id, NULLABLE),
              response_id (FK → responses.id, NULLABLE)

    3NF:
      - created_at, user_input, intent_id y response_id dependen
        sólo de la PK (id), sin dependencias transitivas entre sí.
      - intent_id y response_id son FKs normalizadas en sus
        propias tablas, evitando redundancia de datos.
    """
    user_input: str
    intent_id: Optional[int]
    response_id: Optional[int]
    id: Optional[int] = field(default=None)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        return (
            f"Conversation(id={self.id}, "
            f"at='{self.created_at}', "
            f"intent_id={self.intent_id})"
        )
