# ANÁLISIS DE GLADIADORES - EQUIPO 1

## Resumen de Resultados

| Gladiador | Mejor Distancia | Distancia Promedio | Ranking | Puntos |
|-----------|-----------------|-------------------|---------|--------|
| Balanceado | 507.19 km | 565.20 km | #1 | 50 pts |
| Explorador | 541.32 km | 639.20 km | #2 | 35 pts |
| Explotador | 619.42 km | 718.16 km | #3 | 25 pts |


**Puntuación Total del Equipo:** 110 pts

---

## Gladiador 1: El Explorador 🔍

### Resultados Obtenidos
- **Ranking:** #2 de 3 (interno)
- **Mejor distancia:** 541.32 km
- **Distancia promedio:** 639.20 km (±58.72)
- **Tiempo promedio:** 0.20 segundos

### Análisis de Desempeño

**¿Por qué funcionó/falló de esta manera?**
El Explorador tuvo un desempeño sumamente volátil. Debido a su bajísima presión selectiva (torneo k=2) y su alta tasa de mutación (swap al 5%), el algoritmo fue incapaz de converger hacia una única región del espacio de búsqueda. En algunas iteraciones, la aleatoriedad le permitió tropezar con soluciones moderadamente buenas (541.32 km), pero en promedio falló en capitalizar esos descubrimientos debido a la constante disrupción de sus propios genes.

**¿Qué se observó durante las ejecuciones?**
- Altísima variabilidad: Su desviación estándar (58.72) fue la segunda más alta, lo que demuestra su incapacidad de mantener consistencia.
- Tiempos de ejecución ligeramente menores debido a que el cruzamiento uniforme con reparación es rápido.

**Lecciones aprendidas:**
1. Una exploración excesiva en un problema combinatorio complejo como el TSP termina pareciéndose a una búsqueda puramente aleatoria.
2. Un elitismo de 1 no es suficiente para proteger las mejores rutas encontradas contra una mutación del 5%.

---

## Gladiador 2: El Explotador ⚔️

### Resultados Obtenidos
- **Ranking:** #3 de 3 (interno)
- **Mejor distancia:** 619.42 km
- **Distancia promedio:** 718.16 km (±0.35)
- **Tiempo promedio:** 0.20 segundos

### Análisis de Desempeño

**¿Por qué funcionó/falló de esta manera?**
El Explotador fue víctima de una severa convergencia prematura. Con un torneo de tamaño k=7, las mejores soluciones iniciales (que en la generación 0 siguen siendo muy ineficientes) dominaron rápidamente a toda la población. Como la mutación era casi inexistente (0.1%), el algoritmo perdió toda su diversidad genética en las primeras generaciones y se estancó en óptimos locales muy pobres, sin forma de escapar de ellos.

**¿Qué se observó durante las ejecuciones?**
- Estancamiento casi inmediato. La variabilidad (0.35) fue casi nula no por estabilidad real, sino porque se atascaba enseguida dependiendo de la suerte de la semilla inicial. Si la población inicial era mala, se quedaba atascado en un óptimo local pésimo.
- Desempeño promedio desastroso (718.16 km), probando que en el TSP no se puede depender solo de la recombinación (OX) sin inyectar nuevo material genético (mutación).

**Lecciones aprendidas:**
1. Presión selectiva excesiva (k=7) aniquila la diversidad antes de que el algoritmo pueda mapear el espacio.
2. Tasas de mutación menores al 1% son peligrosas en problemas donde los óptimos locales son muy profundos, como el TSP.

---

## Gladiador 3: El Balanceado ⚖️

### Configuración Elegida

**Justificación de diseño:**
Diseñamos un equilibrio matemático que ataca la naturaleza específica del TSP:
- **Torneo k=4:** Presión moderada. Suficiente para empujar soluciones buenas, pero no tan agresiva como k=7.
- **Order Crossover (OX) al 85%:** El mejor operador para TSP, ya que preserva la adyacencia y sub-rutas relativas entre ciudades.
- **Mutación por Inversión (2%):** A diferencia del *Swap*, la *Inversión* toma un segmento de la ruta y lo voltea. Esto es geométricamente equivalente a "des-cruzar" líneas que se intersecan en el mapa. Una tasa de 2% es suficiente para explorar vecindades sin destruir el progreso.
- **Elitismo 3:** Protege un pequeño núcleo de soluciones top para no perder los des-cruces exitosos.

### Resultados Obtenidos
- **Ranking:** #1 de 3 (interno)
- **Mejor distancia:** 507.19 km
- **Distancia promedio:** 565.20 km (±16.34)
- **Tiempo promedio:** 0.23 segundos

### Análisis de Desempeño

**¿Cumplió las expectativas?**
Totalmente. Superó a los otros dos gladiadores de forma absoluta, tanto en el mejor caso como en el promedio.

**¿Por qué funcionó/falló?**
Funcionó porque logró el *trade-off* perfecto. El OX construyó y combinó sub-rutas sólidas, mientras que la mutación por Inversión pulió geométricamente las soluciones eliminando cruces ineficientes. El k=4 y elitismo 3 mantuvieron la presión justa para permitir que la mutación hiciera su trabajo antes de que la población convergiera.

**Lecciones aprendidas:**
1. Para el TSP, el *tipo* de mutación importa más que la tasa. La Inversión es superior al Swap.
2. La consistencia (desviación estándar de solo 16.34) sumada al mejor resultado global, es el verdadero indicador de un algoritmo genético bien diseñado.

---

## Comparación entre Gladiadores

### Tabla Comparativa

| Aspecto | Explorador | Explotador | Balanceado |
|---------|-----------|-----------|-----------|
| Mejor solución | 541.32 km | 619.42 km | 507.19 km |
| Consistencia (std) | 58.72 | 0.35 | 16.34 |
| Velocidad convergencia | Muy Lenta / Nula | Muy Rápida (Prematura) | Moderada |
| Diversidad final | Alta | Nula | Media |

### Análisis Cruzado

**¿Qué estrategia funcionó mejor para este problema específico?**
La estrategia de explotación balanceada con operadores guiados geométricamente (Inversión) fue, por mucho, la mejor. El Explorador demostró que la diversidad sin dirección es inútil, y el Explotador demostró que la convergencia sin diversidad es una trampa. 

**¿Qué patrones observaste?**
1. **El peligro de los óptimos locales:** El TSP es un terreno minado de óptimos locales. El Explotador cayó en ellos constantemente debido a su nula mutación.
2. **Importancia del operador:** Reemplazar el `swap` por `inversión` fue el diferenciador principal para acortar las distancias en la etapa final del refinamiento.

---

## Conclusiones Generales

### Principales Hallazgos

1. **La Inversión es la reina del TSP:** Operar sobre segmentos contiguos respeta mucho más la estructura del problema que intercambiar ciudades sueltas.
2. **Convergencia prematura es el peor enemigo:** Es preferible tener una búsqueda caótica (Explorador) que una convergencia inmediata a una mala solución (Explotador).
3. **Sinergia de parámetros:** El elitismo de 3 funcionó perfecto en tándem con un torneo de k=4 para garantizar que la mejora generacional fuera constante pero no asfixiante.

### Si pudieras diseñar un 4º gladiador

```python
config_mejorado = {
    'seleccion': {'tipo': 'torneo', 'k': 5},
    'cruzamiento': {'tipo': 'order_crossover', 'probabilidad': 0.90},
    'mutacion': {'tipo': 'inversion', 'probabilidad': 0.05},
    'elitismo': 5
}
```
**Justificación:** Implementaría un gladiador con un poco más de agresividad en la explotación (k=5, elitismo 5, OX al 90%) pero compensando el riesgo de estancamiento elevando la mutación por Inversión a un 5%. De esta manera, el algoritmo convergería más rápido hacia un óptimo, pero las continuas inversiones asegurarían que las peores ineficiencias locales (cruces de rutas) sean constantemente deshechas.
