# Manual de uso — Chatbot con Python y spaCy (MVC)
### Tarea 5.1 · Curso de especialización en IA y Big Data · I.E.S. Al Ándalus

---

## Índice

1. [Requisitos previos](#1-requisitos-previos)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Instalación del entorno virtual (venv)](#3-instalación-del-entorno-virtual-venv)
4. [Instalación de dependencias](#4-instalación-de-dependencias)
5. [Descarga del modelo de lenguaje spaCy](#5-descarga-del-modelo-de-lenguaje-spacy)
6. [Ejecución del chatbot](#6-ejecución-del-chatbot)
7. [Uso del chatbot en consola](#7-uso-del-chatbot-en-consola)
8. [Arquitectura MVC — explicación detallada](#8-arquitectura-mvc--explicación-detallada)
9. [Base de datos SQLite (3NF)](#9-base-de-datos-sqlite-3nf)
10. [Excepciones personalizadas](#10-excepciones-personalizadas)
11. [Métodos asíncronos](#11-métodos-asíncronos)
12. [Constantes y magic strings (`strings.py`)](#12-constantes-y-magic-strings-stringspy)
13. [Desactivar y eliminar el entorno virtual](#13-desactivar-y-eliminar-el-entorno-virtual)
14. [Resolución de problemas frecuentes](#14-resolución-de-problemas-frecuentes)

---

## 1. Requisitos previos

Antes de empezar, asegúrese de tener instalado en su sistema:

| Herramienta | Versión mínima | Comprobación |
|-------------|---------------|--------------|
| Python | 3.10 | `python --version` |
| pip | 23.x | `pip --version` |
| Sistema operativo | Windows 11 / macOS 12 / Ubuntu 20.04 | — |

> **Nota:** En algunos sistemas Linux o macOS, el ejecutable de Python 3 se llama `python3` en lugar de `python`. Sustituya el comando según corresponda en todos los pasos siguientes.

---

## 2. Estructura del proyecto

Tras descomprimir el archivo `chatbot_5.1.zip`, obtendrá el siguiente árbol de directorios:

```
chatbot_5.1/
│
├── main.py                    ← Punto de entrada de la aplicación
├── strings.py                 ← Todas las constantes (magic strings/numbers)
├── exceptions.py              ← Jerarquía de excepciones personalizadas
├── requirements.txt           ← Dependencias del proyecto
│
├── model/
│   ├── __init__.py
│   ├── entities.py            ← Dataclasses: Intent, Keyword, Response, Conversation
│   └── database.py            ← CRUD asíncrono con aiosqlite (SQLite embebida)
│
├── view/
│   ├── __init__.py
│   └── console_view.py        ← Capa de presentación en consola (async)
│
└── controller/
    ├── __init__.py
    ├── nlp_controller.py      ← Lógica spaCy: intención y NER (async)
    └── chatbot_controller.py  ← Orquestador MVC principal (async)
```

---

## 3. Instalación del entorno virtual (venv)

El entorno virtual (`venv`) aísla las dependencias de este proyecto del resto del sistema, evitando conflictos entre versiones de librerías.

### 3.1 Acceder al directorio del proyecto

```bash
cd ruta/hasta/chatbot_5.1
```

Ejemplo en Windows:
```bash
cd C:\Users\Profesor\Desktop\chatbot_5.1
```

Ejemplo en macOS/Linux:
```bash
cd ~/Desktop/chatbot_5.1
```

### 3.2 Crear el entorno virtual

```bash
python -m venv venv
```

Esto crea una carpeta llamada `venv/` dentro del directorio del proyecto. Contiene su propio intérprete de Python y una copia aislada de pip.

### 3.3 Activar el entorno virtual

El procedimiento varía según el sistema operativo:

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Símbolo del sistema / CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

Cuando el entorno está activo, el prompt de la terminal cambia y muestra el prefijo `(venv)`:

```
(venv) C:\Users\Profesor\Desktop\chatbot_5.1>
```

> **Importante:** Todos los comandos de los pasos siguientes deben ejecutarse con el entorno virtual **activo**. Si cierra la terminal, deberá activarlo de nuevo antes de continuar.

---

## 4. Instalación de dependencias

Con el entorno virtual activo, instale las dependencias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

Este comando instalará:

| Paquete | Función |
|---------|---------|
| `spacy` | Motor de Procesamiento del Lenguaje Natural (NLP) |
| `aiosqlite` | Interfaz asíncrona para SQLite |

Para verificar que la instalación fue correcta:

```bash
pip list
```

Debería ver `spacy` y `aiosqlite` entre los paquetes listados.

---

## 5. Descarga del modelo de lenguaje spaCy

spaCy necesita un modelo de lenguaje preentrenado para analizar texto en inglés. Descárguelo con:

```bash
python -m spacy download en_core_web_sm
```

El modelo `en_core_web_sm` es la versión pequeña del modelo inglés de spaCy. Incluye:
- Tokenizador
- Lematizador
- Reconocedor de entidades (NER)
- Vectores de palabras para similitud semántica

Para verificar que el modelo se descargó correctamente:

```bash
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Modelo cargado OK')"
```

---

## 6. Ejecución del chatbot

Con el entorno virtual activo y todas las dependencias instaladas, lance la aplicación:

```bash
python main.py
```

Si todo está configurado correctamente, verá en la consola:

```
====================================================
  SpaCy Chatbot — MVC
  Tarea 5.1 — I.E.S. Al Ándalus
====================================================
  Type 'exit' to quit.
====================================================
You: 
```

La primera vez que se ejecute, el programa:

1. Crea automáticamente el archivo de base de datos `chatbot.db` en el mismo directorio.
2. Genera las tablas en esquema 3NF.
3. Inserta los datos semilla (intenciones, keywords y respuestas).

En ejecuciones posteriores, la base de datos ya existirá y estos pasos se omiten.

---

## 7. Uso del chatbot en consola

### 7.1 Interacción básica

Escriba su mensaje tras el prompt `You:` y pulse **Enter**:

```
You: hello
Chatbot: Hello! How can I assist you today?

You: what is your name
Chatbot: I'm a simple chatbot built with Python and spaCy (MVC).

You: tell me a joke
Chatbot: Why do programmers prefer dark mode? Because light attracts bugs! 🐛
```

### 7.2 Intenciones disponibles

| Intención | Ejemplos de entrada |
|-----------|-------------------|
| `greeting` | hello, hi, hey, good morning |
| `goodbye` | bye, goodbye, see you, farewell |
| `thanks` | thanks, thank you, appreciate it |
| `name` | what is your name, who are you |
| `help` | help, what can you do, options |
| `weather` | weather, temperature, forecast |
| `joke` | joke, tell me a joke, funny |

### 7.3 Reconocimiento de entidades (NER)

Si el texto contiene una entidad nombrada (persona, lugar, fecha, organización…), el chatbot la detecta y la muestra entre corchetes antes de la respuesta:

```
You: I was born in Madrid on January 5th
  [NER detected: Madrid (GPE), January 5th (DATE)]
Chatbot: Sorry, I didn't understand that. Type 'help' for options.
```

### 7.4 Similitud semántica

Si la entrada no contiene ningún keyword exacto, el chatbot utiliza vectores semánticos de spaCy para encontrar la intención más cercana. Esto permite frases como:

```
You: good evening
Chatbot: Hello! How can I assist you today?
```

### 7.5 Salir del chatbot

Escriba `exit` y pulse **Enter**:

```
You: exit
Chatbot: Goodbye! 👋
```

También puede pulsar **Ctrl+C** en cualquier momento para salir de forma segura.

---

## 8. Arquitectura MVC — explicación detallada

El proyecto sigue el patrón **Modelo-Vista-Controlador (MVC)**, que separa las responsabilidades en tres capas independientes:

```
┌─────────────────────────────────────────────────────┐
│                    main.py                          │
│         (composición de dependencias + asyncio)     │
└───────────────────┬─────────────────────────────────┘
                    │ instancia y conecta
                    ▼
┌─────────────────────────────────────────────────────┐
│            ChatbotController                        │  ← CONTROLADOR
│  · Orquesta Model y View                            │
│  · Gestiona el bucle de conversación                │
│  · Propaga excepciones controladas                  │
└────────┬─────────────────────────┬──────────────────┘
         │                         │
         ▼                         ▼
┌──────────────────┐     ┌─────────────────────────────┐
│    Database      │     │       ConsoleView           │
│  (models/)       │     │       (views/)              │
│                  │     │                             │  ← VISTA
│  · SQLite 3NF    │     │  · Lectura asíncrona de     │
│  · aiosqlite     │     │    entrada del usuario      │
│  · CRUD async    │     │  · Salida formateada        │
└──────────────────┘     └─────────────────────────────┘
       ▲ MODELO
       │
┌──────────────────┐
│   NLPController  │  ← SUBCONTROLADOR (lógica de negocio NLP)
│  · spaCy         │
│  · Intent match  │
│  · NER           │
└──────────────────┘
```

### Flujo de una petición

```
Usuario escribe texto
        │
        ▼
ConsoleView.read_input()           ← Vista: captura entrada
        │
        ▼
ChatbotController._handle_turn()   ← Controlador: orquesta
        │
        ├──► NLPController.get_intent()     ─┐
        │                                    ├─ asyncio.gather() en paralelo
        └──► NLPController.extract_entities()─┘
        │
        ▼
Database.get_intent_by_name()      ← Modelo: consulta intención
Database.get_response_by_intent_id() ← Modelo: consulta respuesta
Database.log_conversation()        ← Modelo: persiste el turno
        │
        ▼
ConsoleView.show_reply()           ← Vista: muestra respuesta
```

---

## 9. Base de datos SQLite (3NF)

Al ejecutar el chatbot por primera vez se crea el archivo `chatbot.db`. El esquema sigue la **Tercera Forma Normal (3NF)**:

### Tablas y relaciones

```
intents                    keywords
┌────┬───────────┐         ┌────┬───────────┬──────────────┐
│ id │ name      │◄────────┤ id │ intent_id │ keyword      │
├────┼───────────┤         ├────┼───────────┼──────────────┤
│  1 │ greeting  │         │  1 │     1     │ hello        │
│  2 │ goodbye   │         │  2 │     1     │ hi           │
│  3 │ thanks    │         │  3 │     2     │ bye          │
│ …  │ …         │         │ …  │ …         │ …            │
└────┴───────────┘         └────┴───────────┴──────────────┘
       │
       │                   responses
       │                   ┌────┬───────────┬──────────────────────────┐
       └──────────────────►│ id │ intent_id │ response_text            │
                           ├────┼───────────┼──────────────────────────┤
                           │  1 │     1     │ Hello! How can I help... │
                           │  2 │     2     │ Goodbye! Have a great... │
                           │ …  │ …         │ …                        │
                           └────┴───────────┴──────────────────────────┘

conversations
┌────┬─────────────────────┬─────────────┬───────────┬─────────────┐
│ id │ created_at          │ user_input  │ intent_id │ response_id │
├────┼─────────────────────┼─────────────┼───────────┼─────────────┤
│  1 │ 2025-01-01 10:00:00 │ hello       │     1     │      1      │
│  2 │ 2025-01-01 10:00:05 │ bye         │     2     │      2      │
└────┴─────────────────────┴─────────────┴───────────┴─────────────┘
```

### Por qué se cumple la 3NF

- **1NF:** todos los atributos son atómicos, no hay grupos repetidos.
- **2NF:** todas las claves primarias son simples (un solo campo `id`), por lo que no puede haber dependencias parciales.
- **3NF:** ningún atributo no-clave depende de otro atributo no-clave. Las FKs (`intent_id`, `response_id`) referencian directamente su PK sin crear dependencias transitivas.

### Consultar la base de datos manualmente

Si desea inspeccionar la BD durante o después de una sesión, instale el cliente de línea de comandos de SQLite o use una herramienta gráfica como [DB Browser for SQLite](https://sqlitebrowser.org/).

Con el cliente de consola:

```bash
sqlite3 chatbot.db
```

Consultas útiles:

```sql
-- Ver todas las intenciones
SELECT * FROM intents;

-- Ver keywords de una intención
SELECT k.keyword FROM keywords k
JOIN intents i ON k.intent_id = i.id
WHERE i.name = 'greeting';

-- Ver el historial de conversaciones
SELECT c.created_at, c.user_input, i.name AS intent, r.response_text
FROM conversations c
LEFT JOIN intents i ON c.intent_id = i.id
LEFT JOIN responses r ON c.response_id = r.id;

-- Salir
.quit
```

---

## 10. Excepciones personalizadas

El proyecto define una jerarquía propia de excepciones en `exceptions.py`:

```
ChatbotException                ← Base de todas las excepciones
│
├── NLPException
│   ├── NLPModelNotFoundError   ← El modelo de spaCy no se pudo cargar
│   └── IntentResolutionError   ← No se pudo resolver la intención
│
├── DatabaseException
│   ├── DatabaseConnectionError ← Fallo al conectar con SQLite
│   ├── DatabaseInitError       ← Fallo al crear tablas o insertar semilla
│   ├── DatabaseQueryError      ← Error en una consulta SELECT
│   └── DatabaseInsertError     ← Error en una operación INSERT
│
└── InputException
    ├── EmptyInputError         ← El usuario envió una cadena vacía
    └── InvalidInputError       ← La entrada no pasó validaciones básicas
```

Las excepciones del dominio (`ChatbotException` y subclases) son capturadas en el bucle principal y mostradas al usuario sin detener la aplicación. Los errores inesperados (`Exception`) se dejan propagar para que sean visibles durante el desarrollo.

---

## 11. Métodos asíncronos

Toda la lógica de la aplicación es **asíncrona** (`async/await`) para permitir peticiones simultáneas sin bloquear el hilo principal.

### Puntos clave de la implementación

| Técnica | Dónde se usa | Por qué |
|---------|-------------|---------|
| `asyncio.run(main())` | `main.py` | Lanza el event loop |
| `async with Database()` | `main.py` | Garantiza cierre de conexión BD |
| `aiosqlite` | `database.py` | Queries SQL sin bloquear el loop |
| `run_in_executor()` | `nlp_controller.py`, `console_view.py` | `spacy.load` e `input()` son bloqueantes; se ejecutan en un hilo separado |
| `asyncio.gather()` | `chatbot_controller.py` | Lanza detección de intención y NER **en paralelo** |

### Ejemplo del paralelismo en un turno

```python
# En chatbot_controller.py — _resolve_nlp()
intent_name, entities = await asyncio.gather(
    self._nlp.get_intent(user_input),      # ← se ejecuta a la vez
    self._nlp.extract_entities(user_input), # ← se ejecuta a la vez
)
```

Ambas operaciones NLP se lanzan simultáneamente en lugar de secuencialmente, reduciendo la latencia de cada respuesta.

---

## 12. Constantes y magic strings (`strings.py`)

Todos los valores literales del proyecto están centralizados en `strings.py`. Ningún otro fichero contiene cadenas o números «mágicos» directamente.

### Categorías de constantes

| Categoría | Ejemplos |
|-----------|---------|
| Base de datos | `DB_NAME`, `DB_TIMEOUT`, `TABLE_INTENTS`, `COL_ID`… |
| NLP | `NLP_MODEL`, `SIMILARITY_THRESHOLD` |
| Intenciones | `INTENT_GREETING`, `INTENT_UNKNOWN`… |
| Datos semilla | `SEED_KEYWORDS`, `SEED_RESPONSES` |
| Interfaz | `PROMPT_YOU`, `PROMPT_BOT`, `MSG_BYE`, `BANNER`… |
| Errores | `ERR_NLP_LOAD`, `ERR_DB_CONNECT`… |

### Cómo añadir una nueva intención

1. Abra `strings.py` y añada la constante de nombre:
   ```python
   INTENT_HELP_ME = "help_me"
   ```
2. Añada sus keywords en `SEED_KEYWORDS`:
   ```python
   SEED_KEYWORDS = {
       ...
       INTENT_HELP_ME: ["help me", "i need help", "assist me"],
   }
   ```
3. Añada su respuesta en `SEED_RESPONSES`:
   ```python
   SEED_RESPONSES = {
       ...
       INTENT_HELP_ME: "Sure! Tell me what you need and I'll do my best.",
   }
   ```
4. **Elimine el archivo `chatbot.db`** para que la BD se regenere con los nuevos datos al siguiente arranque:
   ```bash
   rm chatbot.db      # macOS / Linux
   del chatbot.db     # Windows CMD
   ```
5. Vuelva a ejecutar `python main.py`.

---

## 13. Desactivar y eliminar el entorno virtual

### Desactivar (al terminar la sesión de trabajo)

```bash
deactivate
```

El prompt vuelve a su estado normal, sin el prefijo `(venv)`.

### Eliminar completamente el entorno virtual

Si desea liberar espacio o recrearlo desde cero, borre la carpeta `venv/`:

**macOS / Linux:**
```bash
rm -rf venv/
```

**Windows (PowerShell):**
```powershell
Remove-Item -Recurse -Force venv\
```

Para volver a usarlo, repita los pasos del apartado 3.

---

## 14. Resolución de problemas frecuentes

### El comando `python` no se reconoce

En algunos sistemas Linux/macOS el ejecutable es `python3`:

```bash
python3 -m venv venv
source venv/bin/activate
python3 main.py
```

### Error al activar el venv en PowerShell (Windows)

```
venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled
```

Ejecute primero (como administrador):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### `ModuleNotFoundError: No module named 'spacy'`

El entorno virtual no está activo. Actívelo antes de ejecutar:

```bash
# macOS / Linux
source venv/bin/activate

# Windows CMD
venv\Scripts\activate.bat
```

### `OSError: [E050] Can't find model 'en_core_web_sm'`

El modelo de spaCy no se descargó, o se descargó fuera del venv. Con el venv activo:

```bash
python -m spacy download en_core_web_sm
```

### `ModuleNotFoundError: No module named 'aiosqlite'`

Igual que el caso anterior: instale dependencias con el venv activo:

```bash
pip install -r requirements.txt
```

### La BD tiene datos incorrectos tras añadir una intención

Elimine `chatbot.db` y vuelva a ejecutar el chatbot para regenerarla:

```bash
rm chatbot.db   # (macOS/Linux) o  del chatbot.db  (Windows)
python main.py
```

---

