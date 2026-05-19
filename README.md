# Torneo de Configuraciones: La Batalla de los Operadores (Equipo 1)

Este repositorio contiene la solución del Equipo 1 para la actividad **4.5 Torneo de Configuraciones: La Batalla de los Operadores** enfocada en Algoritmos Genéticos y Evolutivos.

## 🎯 Objetivo
Diseñar, implementar y competir con tres configuraciones diferentes de algoritmos genéticos ("gladiadores") para resolver el problema del TSP (Traveling Salesman Problem) de 30 ciudades, comparando estrategias de exploración vs explotación.

## 🗂️ Estructura del Repositorio

- `equipo_1_gladiadores.py`: Código principal que contiene las 3 configuraciones de algoritmos genéticos (Explorador, Explotador y Balanceado) junto con las funciones del TSP y operadores genéticos.
- `equipo_1_analisis.md`: Análisis post-mortem de los resultados obtenidos durante la competencia de los tres gladiadores.
- `equipo_1_resultados.csv`: Resultados tabulados de todas las ejecuciones (10 semillas por cada uno de los 3 gladiadores).
- `equipo_1_mejores_rutas.txt`: Las rutas más óptimas (cortas) generadas por cada gladiador en su respectiva mejor ejecución.
- `ciudades_30.txt`: Conjunto de datos aleatorio de 30 ciudades (coordenadas x, y) con el cual fue evaluado el algoritmo.
- `validacion_1.txt`: Reporte generado por el validador automático comprobando la integridad y correcto funcionamiento del código (100% de los puntos).
- `equipo_1_entrega_sesion3.zip`: Archivo empaquetado para la entrega oficial en ELinea.

## 🛠️ Ejecución
Para ejecutar el experimento, asegúrate de tener instaladas las bibliotecas `numpy` y `pandas`:

```bash
pip install numpy pandas
```

Posteriormente, ejecuta el archivo principal:
```bash
python equipo_1_gladiadores.py
```

## 🏆 Estrategias (Gladiadores)
1. **El Explorador**: Alta tasa de mutación y baja presión selectiva. Busca ampliamente en todo el espacio de búsqueda.
2. **El Explotador**: Baja tasa de mutación y altísima presión selectiva. Refina rápidamente buenas soluciones (con riesgo a caer en óptimos locales prematuramente).
3. **El Balanceado**: Nuestra configuración estelar. Mezcla presión selectiva balanceada con Order Crossover y mutación por Inversión, logrando evadir los problemas de convergencia prematura de manera muy efectiva.
