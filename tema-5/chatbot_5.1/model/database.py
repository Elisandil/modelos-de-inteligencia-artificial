# ============================================================
# models/database.py — Capa de datos asíncrona (aiosqlite)
#
# Esquema en 3ª Forma Normal (3NF):
#
#   intents(id PK, name UNIQUE)
#   keywords(id PK, intent_id FK, keyword)
#   responses(id PK, intent_id FK, response_text)
#   conversations(id PK, created_at, user_input,
#                 intent_id FK NULLABLE, response_id FK NULLABLE)
#
# Todas las dependencias funcionales son únicamente sobre la PK.
# No existen dependencias parciales ni transitivas → 3NF cumplida.
# ============================================================

import aiosqlite
from typing import Optional

import strings as S
from exceptions import (
    DatabaseConnectionError,
    DatabaseInitError,
    DatabaseQueryError,
    DatabaseInsertError,
)
from model.entities import Intent, Keyword, Response, Conversation


class Database:
    """
    Gestor asíncrono de la base de datos SQLite embebida.

    Uso recomendado como context manager:
        async with Database() as db:
            await db.get_all_intents_with_keywords()
    """

    def __init__(self) -> None:
        self._conn: Optional[aiosqlite.Connection] = None

    # ----------------------------------------------------------
    # Context manager
    # ----------------------------------------------------------

    async def __aenter__(self) -> "Database":
        await self.connect()
        await self.init_schema()
        await self.seed()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    # ----------------------------------------------------------
    # Conexión
    # ----------------------------------------------------------

    async def connect(self) -> None:
        """Abre la conexión con la base de datos."""
        try:
            self._conn = await aiosqlite.connect(
                S.DB_NAME, timeout=S.DB_TIMEOUT
            )
            self._conn.row_factory = aiosqlite.Row
            await self._conn.execute("PRAGMA foreign_keys = ON")
            await self._conn.commit()
        except Exception as exc:
            raise DatabaseConnectionError(str(exc)) from exc

    async def close(self) -> None:
        """Cierra la conexión de forma segura."""
        if self._conn:
            await self._conn.close()
            self._conn = None

    # ----------------------------------------------------------
    # DDL — Creación de tablas (3NF)
    # ----------------------------------------------------------

    async def init_schema(self) -> None:
        """Crea las tablas si no existen. Esquema en 3NF."""
        ddl = f"""
        CREATE TABLE IF NOT EXISTS {S.TABLE_INTENTS} (
            {S.COL_ID}   INTEGER PRIMARY KEY AUTOINCREMENT,
            {S.COL_NAME} TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS {S.TABLE_KEYWORDS} (
            {S.COL_ID}        INTEGER PRIMARY KEY AUTOINCREMENT,
            {S.COL_INTENT_ID} INTEGER NOT NULL
                REFERENCES {S.TABLE_INTENTS}({S.COL_ID})
                ON DELETE CASCADE,
            {S.COL_KEYWORD}   TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS {S.TABLE_RESPONSES} (
            {S.COL_ID}            INTEGER PRIMARY KEY AUTOINCREMENT,
            {S.COL_INTENT_ID}     INTEGER NOT NULL
                REFERENCES {S.TABLE_INTENTS}({S.COL_ID})
                ON DELETE CASCADE,
            {S.COL_RESPONSE_TEXT} TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS {S.TABLE_CONVERSATIONS} (
            {S.COL_ID}          INTEGER  PRIMARY KEY AUTOINCREMENT,
            {S.COL_CREATED_AT}  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            {S.COL_USER_INPUT}  TEXT     NOT NULL,
            {S.COL_INTENT_ID}   INTEGER  REFERENCES {S.TABLE_INTENTS}({S.COL_ID}),
            {S.COL_RESPONSE_ID} INTEGER  REFERENCES {S.TABLE_RESPONSES}({S.COL_ID})
        );
        """
        try:
            await self._conn.executescript(ddl)
            await self._conn.commit()
        except Exception as exc:
            raise DatabaseInitError(str(exc)) from exc

    # ----------------------------------------------------------
    # Datos semilla
    # ----------------------------------------------------------

    async def seed(self) -> None:
        """Inserta intenciones, keywords y respuestas si la BD está vacía."""
        try:
            async with self._conn.execute(
                f"SELECT COUNT(*) FROM {S.TABLE_INTENTS}"
            ) as cur:
                row = await cur.fetchone()
                if row[0] > 0:
                    return  # Ya inicializada, no repetir

            for intent_name, keywords in S.SEED_KEYWORDS.items():
                # Insertar intención
                cur = await self._conn.execute(
                    f"INSERT INTO {S.TABLE_INTENTS} ({S.COL_NAME}) VALUES (?)",
                    (intent_name,),
                )
                intent_id = cur.lastrowid

                # Insertar keywords
                for kw in keywords:
                    await self._conn.execute(
                        f"INSERT INTO {S.TABLE_KEYWORDS} "
                        f"({S.COL_INTENT_ID}, {S.COL_KEYWORD}) VALUES (?, ?)",
                        (intent_id, kw),
                    )

                # Insertar respuesta
                response_text = S.SEED_RESPONSES.get(intent_name, S.MSG_UNKNOWN)
                await self._conn.execute(
                    f"INSERT INTO {S.TABLE_RESPONSES} "
                    f"({S.COL_INTENT_ID}, {S.COL_RESPONSE_TEXT}) VALUES (?, ?)",
                    (intent_id, response_text),
                )

            await self._conn.commit()

        except Exception as exc:
            raise DatabaseInitError(str(exc)) from exc

    # ----------------------------------------------------------
    # Consultas de lectura
    # ----------------------------------------------------------

    async def get_all_intents_with_keywords(self) -> dict[str, list[str]]:
        """
        Devuelve un dict {intent_name: [keyword, ...]} con todos
        los datos de la BD. Usado por el NLPController al arrancar.
        """
        try:
            query = f"""
                SELECT i.{S.COL_NAME}, k.{S.COL_KEYWORD}
                FROM   {S.TABLE_INTENTS}  i
                JOIN   {S.TABLE_KEYWORDS} k
                       ON k.{S.COL_INTENT_ID} = i.{S.COL_ID}
                ORDER  BY i.{S.COL_ID}
            """
            result: dict[str, list[str]] = {}
            async with self._conn.execute(query) as cur:
                async for row in cur:
                    result.setdefault(row[0], []).append(row[1])
            return result
        except Exception as exc:
            raise DatabaseQueryError(str(exc)) from exc

    async def get_intent_by_name(self, name: str) -> Optional[Intent]:
        """Recupera una intención por su nombre canónico."""
        try:
            async with self._conn.execute(
                f"SELECT {S.COL_ID}, {S.COL_NAME} "
                f"FROM {S.TABLE_INTENTS} WHERE {S.COL_NAME} = ?",
                (name,),
            ) as cur:
                row = await cur.fetchone()
                if row:
                    return Intent(id=row[S.COL_ID], name=row[S.COL_NAME])
                return None
        except Exception as exc:
            raise DatabaseQueryError(str(exc)) from exc

    async def get_response_by_intent_id(self, intent_id: int) -> Optional[Response]:
        """Recupera la primera respuesta registrada para una intención."""
        try:
            async with self._conn.execute(
                f"SELECT {S.COL_ID}, {S.COL_INTENT_ID}, {S.COL_RESPONSE_TEXT} "
                f"FROM {S.TABLE_RESPONSES} "
                f"WHERE {S.COL_INTENT_ID} = ? LIMIT 1",
                (intent_id,),
            ) as cur:
                row = await cur.fetchone()
                if row:
                    return Response(
                        id=row[S.COL_ID],
                        intent_id=row[S.COL_INTENT_ID],
                        response_text=row[S.COL_RESPONSE_TEXT],
                    )
                return None
        except Exception as exc:
            raise DatabaseQueryError(str(exc)) from exc

    # ----------------------------------------------------------
    # Escritura — registro de conversaciones
    # ----------------------------------------------------------

    async def log_conversation(
        self,
        user_input: str,
        intent_id: Optional[int],
        response_id: Optional[int],
    ) -> Conversation:
        """Persiste un turno de conversación en la BD."""
        try:
            cur = await self._conn.execute(
                f"INSERT INTO {S.TABLE_CONVERSATIONS} "
                f"({S.COL_USER_INPUT}, {S.COL_INTENT_ID}, {S.COL_RESPONSE_ID}) "
                f"VALUES (?, ?, ?)",
                (user_input, intent_id, response_id),
            )
            await self._conn.commit()
            return Conversation(
                id=cur.lastrowid,
                user_input=user_input,
                intent_id=intent_id,
                response_id=response_id,
            )
        except Exception as exc:
            raise DatabaseInsertError(S.TABLE_CONVERSATIONS, str(exc)) from exc
