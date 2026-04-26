# Chatbot con ML e integración web

Chatbot de clasificación de intenciones construido con spaCy, scikit-learn y Flask, aplicando **Clean Architecture**.

## Stack

- **Python 3.13**
- **spaCy 3.8.14** — preprocesado
- **scikit-learn 1.7.2** — clasificador Naive Bayes sobre Bag of Words
- **Flask 3.1.0** — capa web

## Arquitectura
```
src/
├── domain/          → Entidades y puertos (interfaces). Sin dependencias externas.
├── application/     → Caso de uso: ChatService.
├── infrastructure/  → Implementaciones concretas (spaCy, sklearn, JSON).
└── presentation/    → Controladores Flask y HTML.
```

Las dependencias apuntan hacia adentro: `presentation → application → domain`. La infraestructura implementa los puertos definidos en el dominio.

## Decisiones de diseño

- **Dependency Inversion**: `ChatService` depende de abstracciones (`TextPreprocessor`, `IntentClassifier`, `ResponseSelector`), no de clases concretas. Cambiar Naive Bayes por SVM o JSON por MySQL no requiere tocar el dominio ni la aplicación.
- **Repository Pattern**: `JsonIntentRepository` aísla la fuente de datos.
- **Strategy**: clasificador y preprocesador intercambiables.
- **Composition Root** en `app.py`: único punto donde se instancia y cablea todo.
- **Application Factory** de Flask: facilita testing con distintas configuraciones.

## Decisiones de eficiencia

- `__slots__` en todas las clases → menor consumo de memoria, acceso más rápido a atributos.
- spaCy cargado con `disable=["ner", "parser"]` → solo tokenización, lematización y POS. Reduce tiempo de carga ~3x y uso de RAM a la mitad.
- `frozenset` para POS irrelevantes → lookup O(1).
- Tuplas inmutables donde no hay mutación.
- Pipeline sklearn (`CountVectorizer` + `MultinomialNB`) como unidad serializable.
- Umbral de confianza (0.35) → evita respuestas basura cuando el modelo no está seguro.

## Rol de spaCy

Solo preprocesado: lematización, eliminación de stopwords, puntuación y POS irrelevantes (DET, CCONJ, SCONJ, AUX). El clasificador trabaja sobre el texto normalizado.

## Instalación

```bash
py -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Ejecución

```bash
python app.py
```

Abrir `http://127.0.0.1:5000/`.

## Problema encontrado: wheels de spaCy en Python 3.13

Primer intento con `spacy==3.7.6`. Falló en instalación con este error en cadena:

``Failed to build 'thinc' → Failed to build 'blis' → Failed to build 'numpy'
ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc'], ['clang']...]
``

### Causa

spaCy 3.7.6 **no publica wheels precompilados para Python 3.13 en Windows**. Al no encontrar binario, pip descarga el `.tar.gz` e intenta compilar desde fuentes `spacy → thinc → blis → numpy`. Esto requiere un compilador C/C++ (Visual Studio Build Tools) que no estaba instalado.

### Solución

Subir a `spacy==3.8.14`, primera versión estable con **wheels precompilados para cp313-win_amd64**. Sin compilación local, instalación limpia en ~30 segundos.

### Alternativa descartada

- **Bajar a Python 3.12**: funciona, pero obliga a mantener dos versiones de Python.

### Cómo evitarlo

Antes de fijar versiones de librerías con componentes nativos (spaCy, numpy, scipy, torch), verificar en PyPI que exista wheel para tu combinación (versión de Python + SO + arquitectura). Buscar en los archivos de release: `cp313-win_amd64.whl`.

## Ampliar intents

Editar `data/intents.json`. Se reentrena automáticamente al arrancar la app.