# ============================================================
# exceptions.py — Jerarquía de excepciones personalizadas
# ============================================================


class ChatbotException(Exception):
    """Excepción base del chatbot. Todas las excepciones heredan de ésta."""


# ------------------------------------------------------------------
# Excepciones de NLP
# ------------------------------------------------------------------

class NLPException(ChatbotException):
    """Base para errores relacionados con el motor NLP."""


class NLPModelNotFoundError(NLPException):
    """Se lanza cuando spaCy no puede cargar el modelo solicitado."""

    def __init__(self, model_name: str, original: Exception):
        self.model_name = model_name
        self.original   = original
        super().__init__(f"NLP model '{model_name}' could not be loaded: {original}")


class IntentResolutionError(NLPException):
    """Se lanza cuando no se puede resolver la intención del usuario."""

    def __init__(self, user_input: str):
        self.user_input = user_input
        super().__init__(f"Could not resolve intent for: '{user_input}'")


# ------------------------------------------------------------------
# Excepciones de Base de Datos
# ------------------------------------------------------------------

class DatabaseException(ChatbotException):
    """Base para errores relacionados con la base de datos."""


class DatabaseConnectionError(DatabaseException):
    """Se lanza cuando falla la conexión con SQLite."""

    def __init__(self, detail: str):
        super().__init__(f"Database connection failed: {detail}")


class DatabaseInitError(DatabaseException):
    """Se lanza cuando falla la inicialización de tablas o semilla."""

    def __init__(self, detail: str):
        super().__init__(f"Database initialization failed: {detail}")


class DatabaseQueryError(DatabaseException):
    """Se lanza ante un error en una consulta SQL."""

    def __init__(self, detail: str):
        super().__init__(f"Database query error: {detail}")


class DatabaseInsertError(DatabaseException):
    """Se lanza cuando falla una operación de inserción."""

    def __init__(self, table: str, detail: str):
        self.table = table
        super().__init__(f"Insert into '{table}' failed: {detail}")


# ------------------------------------------------------------------
# Excepciones de entrada del usuario
# ------------------------------------------------------------------

class InputException(ChatbotException):
    """Base para errores relacionados con la entrada del usuario."""


class EmptyInputError(InputException):
    """Se lanza cuando el usuario envía una cadena vacía."""

    def __init__(self):
        super().__init__("User input must not be empty or whitespace-only.")


class InvalidInputError(InputException):
    """Se lanza cuando la entrada no supera las validaciones básicas."""

    def __init__(self, detail: str):
        super().__init__(f"Invalid input: {detail}")
