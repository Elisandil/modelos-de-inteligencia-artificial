# 3.1 Introducción al PLN

## 1. Definición de PLN, su importancia y el rol del lingüista
El Procesamiento de Lenguaje Natural (PLN) es la disciplina que se encarga de cerrar la brecha comunicativa entre el ser humano y las máquinas. No se trata simplemente de que un ordenador procese palabras como datos, sino de que sea capaz de interpretar la intención, el contexto y los matices detrás de lo que escribimos o decimos. Es el campo donde convergen la informática, la inteligencia artificial y la lingüística para lograr que la tecnología entienda, interprete y genere lenguaje humano de forma útil.

Su importancia en la IA moderna es absoluta. La gran mayoría de la información que generamos a diario es "no estructurada": correos, mensajes de WhatsApp, vídeos, artículos médicos o contratos legales. Sin el PLN, toda esta información sería ruido ininteligible para un sistema informático. Es la tecnología que permite que funcionen desde los traductores automáticos y los filtros de spam, hasta los asistentes de voz y los chatbots de atención al cliente.

En este contexto, el rol del lingüista es insustituible. A menudo se piensa que la IA es solo terreno de ingenieros, pero en el PLN, el lingüista actúa como el arquitecto del conocimiento. Mientras el ingeniero construye el modelo matemático, el lingüista aporta la comprensión profunda de cómo funciona el idioma: la morfología, la sintaxis y, sobre todo, la pragmática. Son quienes ayudan a diseñar los datos de entrenamiento para que la máquina entienda la diferencia entre una afirmación literal y una ironía, o para evitar sesgos culturales en las respuestas. Su labor es "enseñar" a la máquina las reglas del juego de la comunicación humana para que los algoritmos no cometan errores básicos de interpretación.

## 2. Análisis de Sentimientos: Conceptos y Aplicaciones
El análisis de sentimientos, también conocido como minería de opinión, es una de las aplicaciones más prácticas y demandadas del PLN. Su objetivo principal es determinar la "polaridad" de un texto; es decir, identificar si una opinión expresada es positiva, negativa o neutral. Aunque parece sencillo, el reto es enorme porque el lenguaje humano está lleno de sutilezas: el sarcasmo, las negaciones complejas o el uso de jerga pueden cambiar totalmente el significado de una frase que, palabra por palabra, parecería positiva.

Los sistemas más básicos funcionan mediante reglas y léxicos (listas de palabras con puntuaciones asociadas), pero los más avanzados utilizan modelos de aprendizaje profundo que analizan el contexto completo de la oración. Estos sistemas modernos ya no se conforman con decir si algo es "bueno" o "malo", sino que intentan detectar emociones concretas como frustración, alegría o sorpresa.

La aplicación de esta tecnología ha transformado la manera en que las empresas y organizaciones interactúan con su público:

En el ámbito de las redes sociales y gestión de marca, el análisis de sentimientos permite monitorear la reputación en tiempo real. Las empresas ya no esperan a ver las ventas del mes; si lanzan un anuncio y el sentimiento en Twitter cae en picada, pueden reaccionar al instante para gestionar una crisis de imagen.

En cuanto a la experiencia de cliente, esta tecnología se aplica para analizar encuestas masivas o transcripciones de llamadas de soporte. Permite identificar patrones de quejas recurrentes sin tener que leer miles de formularios manualmente. Por ejemplo, una empresa de telecomunicaciones puede detectar que el sentimiento negativo se dispara cada vez que se menciona la palabra "facturación", señalando un área crítica a mejorar.

Incluso en finanzas o política, se utiliza para medir el pulso del mercado o del electorado. Los algoritmos analizan noticias y foros para predecir tendencias bursátiles basadas en el optimismo o miedo de los inversores, o para ajustar mensajes de campañas políticas según la reacción emocional de los votantes en diferentes regiones.

## 3. Herramientas de PLN en Python: NLTK y spaCy
Cuando hablamos de programar soluciones de PLN, Python es el lenguaje indiscutible gracias a su ecosistema de librerías. Aunque existen muchas opciones, dos nombres destacan sobre el resto: NLTK y spaCy. Ambas son excelentes, pero representan filosofías de trabajo muy distintas.

NLTK (Natural Language Toolkit) es la opción académica por excelencia. Es una librería inmensa, que ofrece múltiples algoritmos para realizar una misma tarea, lo que la hace perfecta para aprender, investigar y entender qué ocurre por debajo. Sin embargo, esta flexibilidad la hace más lenta y pesada, por lo que rara vez se usa en sistemas que necesitan procesar millones de datos en tiempo real. Es la herramienta ideal para la enseñanza y la exploración lingüística detallada.

Por otro lado, spaCy está diseñada para la industria. Su filosofía es ofrecer "la mejor manera de hacer algo", no todas las posibles. Es extremadamente rápida, eficiente y fácil de integrar en flujos de trabajo productivos. Utiliza modelos pre-entrenados muy robustos y maneja el texto con un enfoque orientado a objetos que simplifica mucho el código. Si tu objetivo es construir una aplicación que funcione ya, spaCy suele ser la elección correcta.

El preprocesamiento del texto Independientemente de la librería, el primer paso en cualquier proyecto es limpiar y preparar el texto. Las funciones principales incluyen:

- **Tokenización**: Romper el bloque de texto en unidades individuales (palabras o signos de puntuación).
- **Limpieza de Stopwords**: Eliminar palabras que gramaticalmente son necesarias pero aportan poco significado único (como "el", "de", "y"), para reducir el ruido.
- **Lematización**: Llevar las palabras a su raíz (convertir "comiendo", "comí", "comeré" a "comer"). Esto es vital para que la máquina entienda que todas esas formas se refieren a la misma acción.
- **Etiquetado gramatical (POS Tagging)**: Identificar si la palabra es un sustantivo, un verbo o un adjetivo, lo cual ayuda a desambiguar el significado según el contexto.

A continuación, vemos cómo se implementan estos conceptos en cada librería:

**Ejemplo con NLTK**: En NLTK el proceso es más manual y explícito. Debemos descargar los recursos y aplicar paso a paso la tokenización y el filtrado.

```python
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

texto = "Los analistas están estudiando los nuevos datos."
tokens = word_tokenize(texto, language='spanish')

palabras_vacías = set(stopwords.words('spanish'))
resultado = [p for p in tokens if p.lower() not in palabras_vacías]

print(f"Resultado NLTK: {resultado}")
# Salida probable: ['analistas', 'estudiando', 'nuevos', 'datos', '.']
```

**Ejemplo con spaCy**: spaCy abstrae mucha de la complejidad. Al cargar el texto en su modelo, este realiza automáticamente la tokenización, el análisis gramatical y la lematización en segundo plano, dejándonos el texto listo para usar.

```python
import spacy

nlp = spacy.load("es_core_news_sm")
texto = "Los analistas están estudiando los nuevos datos."
doc = nlp(texto)

print(f"{'Token':<12} {'Lema':<12} {'Tipo'}")
print("-" * 30)

for token in doc:
    if not token.is_stop and not token.is_punct:
        print(f"{token.text:<12} {token.lemma_:<12} {token.pos_}")

# spaCy detecta que "estudiando" viene de "estudiar" (VERBO) automáticamente.
```