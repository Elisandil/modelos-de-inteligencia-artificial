# Algoritmo A* para Búsqueda de Rutas Óptimas entre Capitales de Provincia Españolas

Este proyecto implementa el **algoritmo de búsqueda A*** para encontrar la ruta más corta entre capitales de provincia y ciudades autónomas de España, utilizando coordenadas geográficas reales y distancias calculadas mediante la fórmula de Haversine.

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Uso del Programa](#uso-del-programa)
- [Funcionamiento Detallado](#funcionamiento-detallado)
- [Ciudades Disponibles](#ciudades-disponibles)
- [Limitaciones](#limitaciones)

## Descripción General

El programa calcula la ruta más corta entre dos ciudades españolas utilizando:

- **Algoritmo A***: Un algoritmo de búsqueda informada que combina el coste real acumulado con una heurística para encontrar el camino óptimo de forma eficiente.
- **Fórmula de Haversine**: Para calcular distancias reales entre coordenadas geográficas (latitud y longitud) sobre la superficie terrestre.
- **Grafo de conexiones**: Cada ciudad está conectada con sus 5 vecinos más cercanos, simulando una red de carreteras.

## Uso del Programa

### Proceso de Interacción

1. **Inicio del Programa**:
   ```
   === Cálculo de Ruta Óptima entre Capitales de Provincia (A*) ===
   Total de ciudades disponibles: 51
   Ejemplos: Madrid, Barcelona, Sevilla, Valencia, Bilbao, A Coruña...
   ```

2. **Introducir Ciudad de Origen**:
   ```
   Introduce la ciudad de origen: madrid
   ```
   *Nota: El programa normaliza automáticamente el texto (capitaliza cada palabra)*

3. **Introducir Ciudad de Destino**:
   ```
   Introduce la ciudad de destino: barcelona
   ```

4. **Resultado**:
   El programa mostrará:
   - La ruta encontrada (secuencia de ciudades)
   - La distancia total estimada en kilómetros

## Funcionamiento Detallado

### 1. Base de Datos de Ciudades

El programa incluye **51 ciudades españolas** con sus coordenadas GPS exactas (latitud y longitud). Estas coordenadas son esenciales para:
- Calcular distancias reales entre ciudades
- Aplicar la heurística del algoritmo A*

### 2. Generación del Grafo de Conexiones

El grafo de conexiones se genera dinámicamente

**Proceso**:
1. Para cada ciudad, se calculan las distancias a todas las demás ciudades usando Haversine
2. Se seleccionan las **5 ciudades más cercanas** como vecinos
3. Se crea una conexión bidireccional (si A conecta con B, B conecta con A)

Esto simula una red de carreteras realista donde las ciudades están conectadas principalmente con sus vecinos cercanos.

### 3. Cálculo de Distancias con Haversine

La **fórmula de Haversine** calcula la distancia del círculo máximo entre dos puntos en una esfera (El radio de la Tierra es de 6371Km):

```python
R = 6371 

a = sin²(Δφ/2) + cos(φ1) × cos(φ2) × sin²(Δλ/2)
c = 2 × atan2(√a, √(1−a))
distancia = R × c
```

Donde:
- `φ` = latitud
- `λ` = longitud
- `Δφ` = diferencia de latitudes
- `Δλ` = diferencia de longitudes

Esta fórmula proporciona distancias muy precisas considerando la curvatura de la Tierra.

### 4. Algoritmo A*

El algoritmo A* es un algoritmo de búsqueda informada que encuentra el camino más corto de forma eficiente.

#### Componentes Principales

**a) Función de Evaluación**:
```
f(n) = g(n) + h(n)
```
- `g(n)`: Coste real desde el inicio hasta el nodo n
- `h(n)`: Heurística (estimación del coste desde n hasta el objetivo)
- `f(n)`: Coste total estimado

**b) Heurística**:
La heurística utilizada es la **distancia en línea recta** (Haversine) desde el nodo actual hasta el objetivo. Esta heurística es:
- **Admisible**: Nunca sobreestima el coste real
- **Consistente**: Satisface la desigualdad triangular

**c) Proceso del Algoritmo**:

1. **Inicialización**:
   - Se crea un nodo inicial con g=0
   - Se calcula la heurística h al objetivo
   - Se añade a la lista abierta (cola de prioridad)

2. **Iteración**:
   - Se extrae el nodo con menor f(n) de la lista abierta
   - Si es el objetivo, se reconstruye y devuelve el camino
   - Si no, se exploran sus vecinos:
     - Se calcula el coste tentativo g para cada vecino
     - Si es mejor que el coste anterior, se actualiza y se añade a la lista abierta

3. **Terminación**:
   - Se encuentra el objetivo: devuelve el camino y la distancia
   - La lista abierta queda vacía: no hay camino posible

#### Estructuras de Datos

- **Lista abierta**: Implementada con `heapq` (min-heap) para extraer eficientemente el nodo con menor f(n)
- **Conjunto cerrado**: Almacena nodos ya explorados para evitar ciclos
- **Diccionario g_costs**: Mantiene el mejor coste g encontrado para cada nodo

### 5. Reconstrucción del Camino

Una vez encontrado el objetivo, se reconstruye el camino siguiendo los punteros `parent` desde el nodo objetivo hasta el nodo inicial

## Ciudades Disponibles

El programa incluye las siguientes **51 ciudades**:

| Región | Ciudades |
|--------|----------|
| **Andalucía** | Almería, Cádiz, Córdoba, Granada, Huelva, Jaén, Málaga, Sevilla |
| **Aragón** | Huesca, Teruel, Zaragoza |
| **Asturias** | Oviedo |
| **Islas Baleares** | Palma |
| **Islas Canarias** | Santa Cruz de Tenerife |
| **Cantabria** | Santander |
| **Castilla y León** | Ávila, Burgos, León, Palencia, Salamanca, Segovia, Soria, Valladolid, Zamora |
| **Castilla-La Mancha** | Albacete, Ciudad Real, Cuenca, Guadalajara, Toledo |
| **Cataluña** | Barcelona, Girona, Lleida, Tarragona |
| **Comunidad Valenciana** | Alicante, Castellón, Valencia |
| **Extremadura** | Badajoz, Cáceres |
| **Galicia** | A Coruña, Lugo, Ourense, Pontevedra |
| **Comunidad de Madrid** | Madrid |
| **Región de Murcia** | Murcia |
| **Comunidad Foral de Navarra** | Pamplona |
| **País Vasco** | Bilbao, San Sebastián, Vitoria |
| **La Rioja** | Logroño |
| **Ciudades Autónomas** | Ceuta, Melilla |

## Limitaciones

### 1. Conexiones Limitadas
- Cada ciudad solo está conectada con sus 5 vecinos más cercanos
- Esto significa que algunas rutas reales por carretera podrían no estar representadas
- Ciudades muy lejanas o islas pueden no tener rutas disponibles

### 2. Distancia en Línea Recta vs. Carreteras Reales
- Las distancias calculadas son "en línea recta" (ortodrómicas)
- Las carreteras reales suelen ser más largas debido a montañas, ríos, etc.
- La distancia mostrada es una **estimación conservadora** (mínima posible)

### 3. Islas
- **Santa Cruz de Tenerife** (Canarias) y **Palma** (Baleares) pueden no tener rutas disponibles debido a su lejanía
- **Ceuta** y **Melilla** también pueden tener conectividad limitada

### 4. Sensibilidad a Mayúsculas
- El programa normaliza a capitalización de cada palabra
- Debe coincidir exactamente con el formato en la base de datos
- Ej: "A Coruña" (no "La Coruña")
