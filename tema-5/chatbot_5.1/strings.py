# ============================================================
# strings.py — Constantes y "magic strings/numbers" del proyecto
# Tarea 5.1 - Chatbot con Python y spaCy (MVC)
# ============================================================

# ------------------------------------------------------------------
# BASE DE DATOS
# ------------------------------------------------------------------
DB_NAME              = "chatbot.db"
DB_TIMEOUT           = 10               

# Nombres de tablas
TABLE_INTENTS        = "intents"
TABLE_KEYWORDS       = "keywords"
TABLE_RESPONSES      = "responses"
TABLE_CONVERSATIONS  = "conversations"

# Columnas — intents
COL_ID               = "id"
COL_NAME             = "name"

# Columnas — keywords
COL_INTENT_ID        = "intent_id"
COL_KEYWORD          = "keyword"

# Columnas — responses
COL_RESPONSE_TEXT    = "response_text"

# Columnas — conversations
COL_CREATED_AT       = "created_at"
COL_USER_INPUT       = "user_input"
COL_RESPONSE_ID      = "response_id"

# ------------------------------------------------------------------
# NLP
# ------------------------------------------------------------------
NLP_MODEL            = "en_core_web_sm"
SIMILARITY_THRESHOLD = 0.75           

# ------------------------------------------------------------------
# INTENCIONES (nombres canónicos)
# ------------------------------------------------------------------
INTENT_GREETING  = "greeting"
INTENT_GOODBYE   = "goodbye"
INTENT_THANKS    = "thanks"
INTENT_NAME      = "name"
INTENT_HELP      = "help"
INTENT_WEATHER   = "weather"
INTENT_JOKE      = "joke"
INTENT_UNKNOWN   = "unknown"

# ------------------------------------------------------------------
# DATOS SEMILLA — keywords por intención
# ------------------------------------------------------------------
SEED_KEYWORDS: dict[str, list[str]] = {
    INTENT_GREETING: ["hello", "hi", "hey", "good morning", "good afternoon"],
    INTENT_GOODBYE:  ["bye", "goodbye", "see you", "farewell"],
    INTENT_THANKS:   ["thanks", "thank you", "appreciate it"],
    INTENT_NAME:     ["what is your name", "who are you"],
    INTENT_HELP:     ["help", "what can you do", "options", "commands"],
    INTENT_WEATHER:  ["weather", "temperature", "forecast", "rain", "sunny"],
    INTENT_JOKE:     ["joke", "tell me a joke", "make me laugh", "funny"],
}

# Datos semilla — respuestas por intención
SEED_RESPONSES: dict[str, str] = {
    INTENT_GREETING: "Hello! How can I assist you today?",
    INTENT_GOODBYE:  "Goodbye! Have a great day!",
    INTENT_THANKS:   "You're welcome! Happy to help.",
    INTENT_NAME:     "I'm a simple chatbot built with Python and spaCy (MVC).",
    INTENT_HELP:     (
        "I understand: greeting, goodbye, thanks, name, "
        "help, weather and jokes. Just type naturally!"
    ),
    INTENT_WEATHER:  "I'm not connected to a weather service yet, but it sounds like a great day!",
    INTENT_JOKE:     "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
}

# ------------------------------------------------------------------
# INTERFAZ DE CONSOLA
# ------------------------------------------------------------------
CHATBOT_NAME   = "SpaCy Chatbot — MVC"
PROMPT_YOU     = "You: "
PROMPT_BOT     = "Chatbot: "
EXIT_COMMAND   = "exit"

BANNER = (
    f"{'=' * 52}\n"
    f"  {CHATBOT_NAME}\n"
    f"  Tarea 5.1 — I.E.S. Al Ándalus\n"
    f"{'=' * 52}"
)
MSG_RUNNING  = f"  Type '{EXIT_COMMAND}' to quit.\n" + "=" * 52
MSG_BYE      = "Goodbye! Thanks for chatting!"
MSG_UNKNOWN  = "Sorry, I didn't understand that. Type 'help' for options."
MSG_NER      = "  [NER detected: {}]"
MSG_EMPTY    = "(empty input, please write something)"

# ------------------------------------------------------------------
# MENSAJES DE ERROR
# ------------------------------------------------------------------
ERR_NLP_LOAD       = "Failed to load NLP model '{}': {}"
ERR_INTENT_RESOLVE = "Could not resolve intent for input: '{}'"
ERR_DB_CONNECT     = "Database connection failed: {}"
ERR_DB_INIT        = "Database initialization failed: {}"
ERR_DB_QUERY       = "Database query error: {}"
ERR_DB_INSERT      = "Failed to insert record into '{}': {}"
ERR_EMPTY_INPUT    = "User input must not be empty or whitespace-only."
ERR_INVALID_INPUT  = "Invalid input received: {}"
