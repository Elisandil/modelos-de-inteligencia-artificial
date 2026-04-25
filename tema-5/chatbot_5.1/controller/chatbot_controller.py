# ============================================================
# controllers/chatbot_controller.py — Controlador principal (MVC)
# ============================================================

import strings as S
from exceptions import (
    EmptyInputError,
    IntentResolutionError,
    DatabaseQueryError,
    ChatbotException,
)
from model.database import Database
from controller.nlp_controller import NLPController
from view.console_view import ConsoleView


class ChatbotController:
    """
    Controlador principal del chatbot (patrón MVC).

    Responsabilidades:
      - Orquestar la Vista (ConsoleView), el Modelo (Database)
        y el subcontrolador NLP (NLPController).
      - Gestionar el ciclo de vida de una conversación.
      - Propagar y registrar excepciones de forma controlada.
    """

    def __init__(self, db: Database, nlp: NLPController, view: ConsoleView) -> None:
        self._db   = db
        self._nlp  = nlp
        self._view = view

    # ----------------------------------------------------------
    # Inicialización
    # ----------------------------------------------------------

    async def start(self) -> None:
        """
        Carga el modelo NLP, los datos de la BD y muestra el banner.
        Debe llamarse una única vez antes del bucle principal.
        """
        await self._nlp.load_model()

        intents_map = await self._db.get_all_intents_with_keywords()
        self._nlp.load_intents(intents_map)

        await self._view.show_banner()

    # ----------------------------------------------------------
    # Bucle principal
    # ----------------------------------------------------------

    async def run(self) -> None:
        """
        Bucle asíncrono de conversación.
        Cada iteración lee la entrada, procesa y emite respuesta.
        """
        while True:
            try:
                user_input = await self._view.read_input()

                # Comando de salida
                if user_input.lower() == S.EXIT_COMMAND:
                    await self._view.show_message(S.MSG_BYE)
                    break

                reply = await self._handle_turn(user_input)
                await self._view.show_reply(reply)

            except EmptyInputError:
                await self._view.show_message(S.MSG_EMPTY)

            except ChatbotException as exc:
                # Errores del dominio: mostramos al usuario sin romper el bucle
                await self._view.show_error(str(exc))

            except (KeyboardInterrupt, EOFError):
                await self._view.show_message(f"\n{S.MSG_BYE}")
                break

    # ----------------------------------------------------------
    # Procesamiento de un turno de conversación
    # ----------------------------------------------------------

    async def _handle_turn(self, user_input: str) -> str:
        """
        Orquesta NLP + BD para un único turno.

        1. Valida la entrada.
        2. Extrae intención y entidades (NLP).
        3. Recupera la respuesta de la BD.
        4. Persiste el turno en conversations.
        5. Devuelve el texto de respuesta.
        """
        # 1. Validación básica
        if not user_input or not user_input.strip():
            raise EmptyInputError()

        # 2. NLP — intención y entidades en paralelo
        intent_name, entities = await self._resolve_nlp(user_input)

        # 3. Muestra entidades NER si las hay
        if entities:
            ner_str = ", ".join(f"{t} ({l})" for t, l in entities)
            await self._view.show_message(S.MSG_NER.format(ner_str))

        # 4. Obtener intención de la BD
        intent_obj = await self._db.get_intent_by_name(intent_name)
        intent_id  = intent_obj.id if intent_obj else None

        # 5. Obtener respuesta de la BD
        response_text = S.MSG_UNKNOWN
        response_id   = None
        if intent_id is not None:
            resp_obj = await self._db.get_response_by_intent_id(intent_id)
            if resp_obj:
                response_text = resp_obj.response_text
                response_id   = resp_obj.id

        # 6. Persistir conversación
        await self._db.log_conversation(user_input, intent_id, response_id)

        return response_text

    async def _resolve_nlp(
        self, user_input: str
    ) -> tuple[str, list[tuple[str, str]]]:
        """
        Lanza la detección de intención y NER de forma concurrente
        usando asyncio.gather para mayor rendimiento.
        """
        import asyncio
        intent_name, entities = await asyncio.gather(
            self._nlp.get_intent(user_input),
            self._nlp.extract_entities(user_input),
        )
        return intent_name, entities
