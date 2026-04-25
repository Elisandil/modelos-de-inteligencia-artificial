# ============================================================
# controllers/nlp_controller.py — Lógica NLP con spaCy (async)
# ============================================================

import asyncio
from typing import Optional

import spacy
from spacy.language import Language

import strings as S
from exceptions import NLPModelNotFoundError, IntentResolutionError


class NLPController:
    """
    Controlador NLP que encapsula toda la lógica de spaCy.

    - Carga el modelo de lenguaje de forma asíncrona.
    - Detecta la intención mediante:
        1) Coincidencia exacta de keywords (rápida).
        2) Similitud semántica como fallback (doc.similarity).
    - Extrae entidades NER del texto de entrada.
    """

    def __init__(self) -> None:
        self._nlp: Optional[Language] = None
        self._intents: dict[str, list[str]] = {}   # {intent_name: [keywords]}

    # ----------------------------------------------------------
    # Inicialización
    # ----------------------------------------------------------

    async def load_model(self) -> None:
        """
        Carga el modelo spaCy en un hilo separado para no bloquear
        el event loop (spacy.load es operación bloqueante).
        """
        loop = asyncio.get_running_loop()
        try:
            self._nlp = await loop.run_in_executor(
                None, spacy.load, S.NLP_MODEL
            )
        except OSError as exc:
            raise NLPModelNotFoundError(S.NLP_MODEL, exc) from exc

    def load_intents(self, intents: dict[str, list[str]]) -> None:
        """Recibe el mapa {intent: [keywords]} cargado desde la BD."""
        self._intents = intents

    # ----------------------------------------------------------
    # Detección de intención
    # ----------------------------------------------------------

    async def get_intent(self, user_input: str) -> str:
        """
        Detecta la intención del texto del usuario.

        Estrategia:
          1. Búsqueda exacta de keywords (O(n) sobre texto normalizado).
          2. Similitud semántica con spaCy si no hay coincidencia exacta.
          3. Devuelve INTENT_UNKNOWN si ningún método supera el umbral.
        """
        text = user_input.lower().strip()

        # Paso 1 — keywords exactas (sin NLP, muy rápido)
        for intent, keywords in self._intents.items():
            for keyword in keywords:
                if keyword in text:
                    return intent

        # Paso 2 — similitud semántica (en executor para no bloquear)
        loop = asyncio.get_running_loop()
        best_intent = await loop.run_in_executor(
            None, self._semantic_similarity, text
        )
        return best_intent

    def _semantic_similarity(self, text: str) -> str:
        """
        Compara el texto con cada keyword usando doc.similarity.
        Ejecutado en un ThreadPoolExecutor para no bloquear asyncio.
        """
        user_doc = self._nlp(text)
        best_intent = S.INTENT_UNKNOWN
        best_score  = 0.0

        if not user_doc.has_vector:
            return best_intent

        for intent, keywords in self._intents.items():
            for keyword in keywords:
                kw_doc = self._nlp(keyword)
                if kw_doc.has_vector:
                    score = user_doc.similarity(kw_doc)
                    if score > best_score:
                        best_score  = score
                        best_intent = intent

        return best_intent if best_score >= S.SIMILARITY_THRESHOLD else S.INTENT_UNKNOWN

    # ----------------------------------------------------------
    # Reconocimiento de entidades (NER)
    # ----------------------------------------------------------

    async def extract_entities(self, user_input: str) -> list[tuple[str, str]]:
        """
        Extrae entidades nombradas (NER) del texto.
        Devuelve lista de (texto_entidad, etiqueta).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._ner, user_input)

    def _ner(self, text: str) -> list[tuple[str, str]]:
        doc = self._nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
