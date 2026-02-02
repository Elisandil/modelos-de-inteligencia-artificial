### ¿Podemos asegurar que el camino es óptimo?
En este caso concreto, sí, hemos encontrado un camino de coste 6 que es muy bajo. Sin embargo, teóricamente, no podríamos asegurarlo al 100% solo confiando en el algoritmo, porque para que $A^*$ garantice optimalidad, la heurística debe ser admisible, y aquí no lo es.

### ¿Es admisible la función $h$ propuesta?
No, no es admisible.

### ¿Por qué?
Para que una heurística sea admisible, debe cumplirse siempre que $h(n) \le h^*(n)$ (el coste real estimado nunca debe ser mayor al real).

* **El fallo:** Un movimiento de Salto tiene un coste de 2. Sin embargo, este único movimiento puede avanzar el hueco 2 posiciones (restando 2 a $v$) y además arreglar una moneda incorrecta (restando 1 a $p$).
* Esto significa que la heurística puede bajar en 3 puntos tras una acción que solo cuesta 2. Al bajar más rápido que el coste real, significa que en el estado anterior estábamos sobreestimando el coste.