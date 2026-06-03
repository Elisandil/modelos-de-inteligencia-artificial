# Sistema Experto de Diagnóstico Industrial con Redes Bayesianas

## Qué es esto

Un sistema experto que identifica qué pieza de una máquina industrial está fallando a partir de los síntomas que observa un operario. Usa una **red bayesiana** como motor de inferencia, lo que permite combinar múltiples síntomas a la vez para obtener un diagnóstico más preciso.

El sistema además **aprende**: cuando un técnico confirma qué pieza realmente falló, las probabilidades internas se ajustan automáticamente para futuros diagnósticos.

## Por qué Redes Bayesianas y no probabilidades directas

En la versión básica del ejercicio, el sistema recibe **un solo síntoma** y devuelve las probabilidades de cada pieza multiplicando directamente. Funciona, pero tiene un problema fundamental: si el operario observa vibración **y** sobrecalentamiento a la vez, no hay forma limpia de combinar esas dos evidencias.

Una red bayesiana resuelve esto. En esencia es un grafo dirigido donde cada nodo es una variable (pieza, síntoma) y las flechas indican relaciones causales. Cuando le pasas evidencia (síntomas observados), el algoritmo de inferencia aplica el Teorema de Bayes propagando las probabilidades por toda la red, no solo en una dirección.

### La estructura de nuestra red

```
         ┌─── Vibración
         │
Pieza ───┼─── Ruido Agudo
         │
         └─── Sobrecalentamiento
```

Un solo nodo padre (**Pieza**) con tres hijos (**síntomas**). Cada flecha dice "la pieza que falla influye en qué síntomas aparecen". Cuando el operario reporta síntomas, hacemos inferencia **inversa**: dado que veo estos síntomas, ¿qué pieza es la más probable?

Esto es exactamente lo que hace el Teorema de Bayes: invertir la dirección de la causalidad usando las probabilidades conocidas.

## Conceptos clave que maneja el código

### CPT (Conditional Probability Table)

Cada síntoma tiene una tabla que dice "si falla el Motor, la probabilidad de ver vibración es 0.6; si falla la Correa, 0.3; si falla el Filtro, 0.1". Estas tablas son las CPTs y son el corazón de la red. Son equivalentes a la matriz de probabilidades del enunciado, pero estructuradas para que `pgmpy` pueda operar con ellas.

### Prior (probabilidad a priori)

Antes de ver ningún síntoma, ¿qué probabilidad asignamos a que falle cada pieza? En nuestro caso usamos un prior **uniforme** (1/3 para cada una), es decir, sin información previa asumimos que cualquiera puede fallar con la misma probabilidad.

En un sistema en producción real, este prior se calcularía a partir del histórico de fallos: si el Motor falla el 50% de las veces, su prior sería 0.5.

### Eliminación de Variables

Es el algoritmo que usa `pgmpy` internamente para calcular las probabilidades posteriores. En redes pequeñas como la nuestra no se nota, pero en redes con decenas de nodos es mucho más eficiente que calcular Bayes "a mano" para cada combinación posible.

No necesitas implementarlo tú; `VariableElimination` de pgmpy lo hace. Solo necesitas saber que es el método exacto (no aproximado) de inferencia en redes bayesianas discretas.

### Factor de desgaste

Cuando una pieza supera sus horas de vida útil, multiplicamos su probabilidad en la CPT por 1.5 (acotado a 0.99 para que siga siendo una probabilidad válida). Esto simula que una pieza desgastada es más propensa a provocar síntomas. Tras aplicar el factor, se reconstruye la red para que la inferencia lo tenga en cuenta.

### Retroalimentación (aprendizaje)

Cuando el técnico confirma qué pieza falló realmente:

1. Se incrementa en un 5% la probabilidad de esa pieza para cada síntoma observado.
2. Se redistribuye proporcionalmente ese incremento entre las demás piezas para que la suma siga siendo coherente.
3. Se resetean las horas de uso de la pieza (simula sustitución).
4. Se persiste en disco el JSON actualizado.
5. Se **reconstruye la red** con las nuevas CPTs.

Esto último es importante: no basta con cambiar los números en el diccionario, hay que recrear los objetos de `pgmpy` para que la inferencia use los valores actualizados.


## Qué demuestra el notebook

El notebook tiene celdas secuenciales que verifican los tres requisitos del enunciado:

1. **Persistencia** — Borra el JSON, crea el sistema (datos por defecto), guarda, y al final recarga una segunda instancia que lee del disco y comprueba que los valores modificados persisten.

2. **Inferencia** — Tres casos: un síntoma solo, dos síntomas combinados, y los tres a la vez. Se puede ver cómo al añadir más evidencia las probabilidades se polarizan hacia la pieza más probable.

3. **Aprendizaje** — Muestra el antes/después de una retroalimentación: la CPT cambia, las horas se resetean, los fallos acumulados suben, y un nuevo diagnóstico refleja el ajuste.

4. **Factor de desgaste** — Fuerza al Motor a 5200 horas (límite: 5000), reconstruye la red, y se ve cómo la probabilidad del Motor sube en el diagnóstico.

## Dependencias

```
pgmpy
pandas
numpy
```

## Nota sobre versiones de pgmpy

En versiones recientes de `pgmpy`, la clase `BayesianNetwork` fue deprecada y renombrada a `DiscreteBayesianNetwork`. El código ya usa la versión nueva. Si usas una versión antigua de pgmpy y te da error, cambia el import:

```python
# Versiones antiguas
from pgmpy.models import BayesianNetwork

# Versiones recientes (la que usamos)
from pgmpy.models import DiscreteBayesianNetwork
```