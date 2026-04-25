# ============================================================
# views/console_view.py — Capa de presentación (Vista MVC)
# ============================================================

import asyncio
import sys
from typing import Optional

import strings as S
from exceptions import EmptyInputError


class ConsoleView:
    """
    Vista de consola asíncrona.

    Toda operación de I/O bloqueante (input/print) se delega a un
    ThreadPoolExecutor mediante run_in_executor, manteniendo el
    event loop libre para peticiones simultáneas.
    """

    def __init__(self) -> None:
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    # ----------------------------------------------------------
    # Helpers internos
    # ----------------------------------------------------------

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    async def _async_print(self, text: str) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, print, text)

    async def _async_input(self, prompt: str) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, input, prompt)

    # ----------------------------------------------------------
    # Métodos públicos de la Vista
    # ----------------------------------------------------------

    async def show_banner(self) -> None:
        """Muestra el banner inicial del chatbot."""
        await self._async_print(S.BANNER)
        await self._async_print(S.MSG_RUNNING)

    async def read_input(self) -> str:
        """
        Lee la entrada del usuario de forma asíncrona.
        Lanza EmptyInputError si la cadena es vacía o sólo espacios.
        """
        raw = await self._async_input(S.PROMPT_YOU)
        stripped = raw.strip()
        if not stripped:
            raise EmptyInputError()
        return stripped

    async def show_reply(self, message: str) -> None:
        """Muestra la respuesta del chatbot con el prefijo correspondiente."""
        await self._async_print(f"{S.PROMPT_BOT}{message}\n")

    async def show_message(self, message: str) -> None:
        """Muestra un mensaje informativo sin prefijo de bot."""
        await self._async_print(message)

    async def show_error(self, error: str) -> None:
        """Muestra un mensaje de error en stderr de forma asíncrona."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, lambda: print(f"[ERROR] {error}", file=sys.stderr)
        )
