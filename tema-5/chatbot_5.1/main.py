# ============================================================
# main.py — Punto de entrada de la aplicación
# ============================================================

import asyncio

from model.database import Database
from controller.nlp_controller import NLPController
from controller.chatbot_controller import ChatbotController
from view.console_view import ConsoleView
from exceptions import ChatbotException


async def main() -> None:
    """
    Composición de dependencias (Manual DI) y arranque del chatbot.

    El Database se usa como async context manager para garantizar
    que la conexión SQLite se cierra siempre, incluso ante errores.
    """
    view = ConsoleView()
    nlp  = NLPController()

    try:
        async with Database() as db:
            controller = ChatbotController(db=db, nlp=nlp, view=view)
            await controller.start()
            await controller.run()

    except ChatbotException as exc:
        print(f"\n[FATAL] {exc}")
    except Exception as exc:
        print(f"\n[UNEXPECTED ERROR] {exc}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
