# El pastor y la manada

### Punto de partida

El pastor, el lobo, el cordero y la lechuga están en la orilla izquierda del río.

### Objetivo a alcanzar

Que los cuatro (pastor, lobo, cordero, lechuga) estén en la orilla derecha del río sin que en ningún momento el lobo se coma al cordero ni el cordero se coma la lechuga.

### Cómo representar estados (inicial, final e intermedios)

Usaremos una tupla (P, W, C, L) donde cada letra toma el valor L (left / izquierda) o R (right / derecha):

- P = posición del Pastor
- W = posición del Lobo
- C = posición del Cordero
- L = posición de la Lechuga

### Estado inicial:

PWCL = LLLL

### Estado final:

PWCL = RRRR

### Enumeración de todos los estados y cuáles son prohibidos

Hay 4 elementos con 2 posiciones → 2⁴ = 16 estados posibles. 
El orden es el siguiente: P, W, C, L.  

- LLLL — (L,L,L,L) ✅
- LLLR = (L,L,L,R) ✅
- LLRL = (L,L,R,L) ✅
- LLRR = (L,L,R,R) ❌ — aquí cordero y lechuga en la derecha sin el pastor (P en L) ⇒ cordero se come la lechuga.
- LRLL = (L,R,L,L) ✅
- LRLR = (L,R,L,R) ✅
- LRRL = (L,R,R,L) ❌ — aquí lobo y cordero en la derecha sin pastor ⇒ lobo se come al cordero.
- LRRR = (L,R,R,R) ❌ — cordero y lechuga (y lobo) en derecha sin pastor ⇒ hay conflicto (cordero come lechuga or lobo come cordero).
- RLLL = (R,L,L,L) ✅
- RLLR = (R,L,L,R) ❌ — cordero y lechuga juntos en R sin pastor ⇒ cordero se come lechuga.
- RLRL = (R,L,R,L) ✅
- RLRR = (R,L,R,R) ❌ — cordero y lechuga juntos en R sin pastor.
- RRLL = (R,R,L,L) ❌ — lobo y cordero juntos en L sin pastor ⇒ lobo se come al cordero.
- RRLR = (R,R,L,R) ✅
- RRRL = (R,R,R,L) ✅
- RRRR = (R,R,R,R) ✅

#### Nota: ✅ (permitido) o ❌ (prohibido: alguien se come a otro).

### Solución:

Una solución estándar y corta:

a) Partimos de (L,L,L,L) (todos a la izquierda).

b) Pastor cruza con el cordero a la derecha.
Estado: (R, L, R, L) = RLRL.
Acción: Pastor lleva cordero → derecha.

c) Pastor vuelve solo a la izquierda.
Estado: (L, L, R, L) = LLRL.
Acción: Pastor regresa → izquierda.

d) Pastor cruza con el lobo a la derecha.
Estado: (R, R, R, L) = RRRL.
Acción: Pastor lleva lobo → derecha.

e) Pastor regresa con el cordero a la izquierda.
Estado: (L, R, L, L) = LRLL.
Acción: Pastor trae cordero de vuelta → izquierda.

f) Pastor cruza con la lechuga a la derecha.
Estado: (R, R, L, R) = RRLR.
Acción: Pastor lleva la lechuga → derecha.

g) Pastor vuelve solo a la izquierda.
Estado: (L, R, L, R) = LRLR.
Acción: Pastor regresa → izquierda.

h) Pastor cruza con el cordero a la derecha (último viaje).
Estado final: (R, R, R, R) = RRRR.
Acción: Pastor lleva cordero → derecha.

Como se puede observar, en ningún momento el lobo se ha quedado solo junto al cordero, 
al igual que el cordero nunca se ha quedado solo con la lechuga.