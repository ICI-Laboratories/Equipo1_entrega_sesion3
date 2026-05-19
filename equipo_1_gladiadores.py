import numpy as np
import random
import time
import pandas as pd
import math
from typing import List, Dict, Tuple

# ============================================================================
# CONFIGURACIONES DE GLADIADORES
# ============================================================================

CONFIGS = {
    'explorador': {
        'nombre': 'El Explorador',
        'seleccion': {'tipo': 'torneo', 'k': 2},
        'cruzamiento': {'tipo': 'uniforme', 'probabilidad': 0.8, 'p': 0.5},
        'mutacion': {'tipo': 'swap', 'probabilidad': 0.05},
        'elitismo': 1
    },
    'explotador': {
        'nombre': 'El Explotador',
        'seleccion': {'tipo': 'torneo', 'k': 7},
        'cruzamiento': {'tipo': 'order_crossover', 'probabilidad': 0.8},
        'mutacion': {'tipo': 'swap', 'probabilidad': 0.001},
        'elitismo': 5
    },
    'balanceado': {
        'nombre': 'El Balanceado',
        'seleccion': {'tipo': 'torneo', 'k': 4},
        'cruzamiento': {'tipo': 'order_crossover', 'probabilidad': 0.85},
        'mutacion': {'tipo': 'inversion', 'probabilidad': 0.02},
        'elitismo': 3
    }
}

# ============================================================================
# FUNCIONES DEL TSP
# ============================================================================

def cargar_ciudades(archivo):
    """Carga ciudades desde archivo CSV"""
    df = pd.read_csv(archivo)
    ciudades = []
    for index, row in df.iterrows():
        ciudades.append((row['x'], row['y']))
    return ciudades

def calcular_distancia_ruta(ruta, ciudades):
    """Calcula distancia total de una ruta regresando al origen"""
    distancia = 0.0
    num_ciudades = len(ruta)
    for i in range(num_ciudades):
        idx_actual = ruta[i]
        idx_sig = ruta[(i + 1) % num_ciudades]
        
        c1 = ciudades[idx_actual]
        c2 = ciudades[idx_sig]
        
        dist = math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2)
        distancia += dist
    return distancia

def inicializar_poblacion(num_ciudades, tam_poblacion):
    """Inicializa poblacion de rutas aleatorias"""
    poblacion = []
    base_ruta = list(range(num_ciudades))
    for _ in range(tam_poblacion):
        ruta_clon = base_ruta.copy()
        random.shuffle(ruta_clon)
        poblacion.append(ruta_clon)
    return poblacion

# ============================================================================
# OPERADORES GENÉTICOS
# ============================================================================

def seleccion_torneo(poblacion, fitness, k):
    """Selección por torneo"""
    seleccionados = random.sample(range(len(poblacion)), k)
    mejor_idx = min(seleccionados, key=lambda idx: fitness[idx])
    return poblacion[mejor_idx].copy()

def seleccionar_padres(poblacion, fitness, config):
    padres = []
    k = config['seleccion'].get('k', 3)
    for _ in range(len(poblacion)):
        padres.append(seleccion_torneo(poblacion, fitness, k))
    return padres

def cruzamiento_order(padre1, padre2):
    """Order Crossover (OX) para permutaciones"""
    size = len(padre1)
    a, b = random.sample(range(size), 2)
    start, end = min(a, b), max(a, b)
    
    hijo1 = [-1] * size
    hijo1[start:end+1] = padre1[start:end+1]
    
    ptr = (end + 1) % size
    for i in range(size):
        idx = (end + 1 + i) % size
        ciudad = padre2[idx]
        if ciudad not in hijo1:
            hijo1[ptr] = ciudad
            ptr = (ptr + 1) % size
            
    hijo2 = [-1] * size
    hijo2[start:end+1] = padre2[start:end+1]
    
    ptr = (end + 1) % size
    for i in range(size):
        idx = (end + 1 + i) % size
        ciudad = padre1[idx]
        if ciudad not in hijo2:
            hijo2[ptr] = ciudad
            ptr = (ptr + 1) % size
            
    return hijo1, hijo2

def cruzamiento_uniforme(padre1, padre2, p=0.5):
    """Cruzamiento uniforme adaptado para permutaciones (usando cruce basado en posiciones con reparacion)
    Pero para seguir fiel a la filosofia del explorador, vamos a hacer un cruce uniforme que hereda 
    posiciones de p1 con prob p, y llena el resto en orden desde p2.
    """
    size = len(padre1)
    hijo1 = [-1] * size
    hijo2 = [-1] * size
    
    # Hijo 1: toma de padre1 con probabilidad p
    for i in range(size):
        if random.random() < p:
            hijo1[i] = padre1[i]
            
    # Llenar huecos de hijo1 con padre2
    ptr = 0
    for i in range(size):
        if hijo1[i] == -1:
            while padre2[ptr] in hijo1:
                ptr += 1
            hijo1[i] = padre2[ptr]
            
    # Hijo 2: toma de padre2 con probabilidad p
    for i in range(size):
        if random.random() < p:
            hijo2[i] = padre2[i]
            
    # Llenar huecos de hijo2 con padre1
    ptr = 0
    for i in range(size):
        if hijo2[i] == -1:
            while padre1[ptr] in hijo2:
                ptr += 1
            hijo2[i] = padre1[ptr]
            
    return hijo1, hijo2

def aplicar_cruzamiento(padres, config):
    hijos = []
    prob_cruce = config['cruzamiento'].get('probabilidad', 0.8)
    tipo_cruce = config['cruzamiento']['tipo']
    
    for i in range(0, len(padres), 2):
        p1 = padres[i]
        p2 = padres[(i + 1) % len(padres)]
        
        if random.random() < prob_cruce:
            if tipo_cruce == 'order_crossover':
                h1, h2 = cruzamiento_order(p1, p2)
            elif tipo_cruce == 'uniforme':
                p_inter = config['cruzamiento'].get('p', 0.5)
                h1, h2 = cruzamiento_uniforme(p1, p2, p_inter)
            else:
                h1, h2 = p1.copy(), p2.copy()
        else:
            h1, h2 = p1.copy(), p2.copy()
            
        hijos.append(h1)
        if len(hijos) < len(padres):
            hijos.append(h2)
            
    return hijos[:len(padres)]

def mutacion_swap(ruta, prob):
    """Mutación por intercambio de dos posiciones aleatorias"""
    if random.random() < prob:
        size = len(ruta)
        idx1, idx2 = random.sample(range(size), 2)
        ruta[idx1], ruta[idx2] = ruta[idx2], ruta[idx1]
    return ruta

def mutacion_inversion(ruta, prob):
    """Mutación por inversión de un segmento continuo"""
    if random.random() < prob:
        size = len(ruta)
        idx1, idx2 = random.sample(range(size), 2)
        start, end = min(idx1, idx2), max(idx1, idx2)
        ruta[start:end+1] = reversed(ruta[start:end+1])
    return ruta

def aplicar_mutacion(hijos, config):
    prob_mut = config['mutacion']['probabilidad']
    tipo_mut = config['mutacion']['tipo']
    
    hijos_mutados = []
    for hijo in hijos:
        if tipo_mut == 'swap':
            h_mut = mutacion_swap(hijo.copy(), prob_mut)
        elif tipo_mut == 'inversion':
            h_mut = mutacion_inversion(hijo.copy(), prob_mut)
        else:
            h_mut = hijo.copy()
        hijos_mutados.append(h_mut)
    return hijos_mutados

def aplicar_elitismo(poblacion_ant, fitness_ant, hijos, config):
    num_elite = config.get('elitismo', 1)
    
    # Encontrar las mejores rutas (indices)
    indices_ordenados = np.argsort(fitness_ant)
    mejores_padres = [poblacion_ant[i].copy() for i in indices_ordenados[:num_elite]]
    
    # La nueva poblacion se queda con los n mejores padres y rellena con hijos
    nueva_poblacion = mejores_padres + hijos[:len(hijos)-num_elite]
    return nueva_poblacion

# ============================================================================
# ALGORITMO GENÉTICO
# ============================================================================

def algoritmo_genetico(ciudades, config, semilla, evaluaciones_max=10000):
    """
    Ejecuta un AG con la configuración especificada
    
    Returns:
        dict con 'mejor_ruta', 'mejor_distancia', 'distancia_promedio', 
        'desv_std', 'tiempo'
    """
    random.seed(semilla)
    np.random.seed(semilla)
    
    inicio = time.time()
    
    # Inicialización
    poblacion = inicializar_poblacion(len(ciudades), 100)
    
    evaluaciones = 0
    mejor_global = float('inf')
    mejor_ruta_global = None
    
    while evaluaciones < evaluaciones_max:
        # Evaluar población
        fitness = [calcular_distancia_ruta(ind, ciudades) for ind in poblacion]
        evaluaciones += len(poblacion)
        
        # Actualizar mejor
        idx_mejor = np.argmin(fitness)
        if fitness[idx_mejor] < mejor_global:
            mejor_global = fitness[idx_mejor]
            mejor_ruta_global = poblacion[idx_mejor].copy()
            
        if evaluaciones >= evaluaciones_max:
            break
        
        # Selección
        padres = seleccionar_padres(poblacion, fitness, config)
        
        # Cruzamiento
        hijos = aplicar_cruzamiento(padres, config)
        
        # Mutación
        hijos = aplicar_mutacion(hijos, config)
        
        # Elitismo + Reemplazo
        poblacion = aplicar_elitismo(poblacion, fitness, hijos, config)
    
    tiempo_total = time.time() - inicio
    
    # Estadísticas finales
    fitness_finales = [calcular_distancia_ruta(ind, ciudades) for ind in poblacion]
    
    return {
        'mejor_ruta': mejor_ruta_global,
        'mejor_distancia': mejor_global,
        'distancia_promedio': np.mean(fitness_finales),
        'desv_std': np.std(fitness_finales),
        'tiempo': tiempo_total
    }

# ============================================================================
# EXPERIMENTO PRINCIPAL
# ============================================================================

def ejecutar_torneo(archivo_ciudades):
    """
    Ejecuta el torneo completo: 3 gladiadores × 10 ejecuciones cada uno
    """
    ciudades = cargar_ciudades(archivo_ciudades)
    
    resultados = []
    mejores_rutas_texto = "MEJORES RUTAS ENCONTRADAS\n\n"
    
    for nombre_config, config in CONFIGS.items():
        print(f"\n{'='*60}")
        print(f"GLADIADOR: {config['nombre']}")
        print(f"{'='*60}")
        
        mejor_dist_global = float('inf')
        mejor_ruta_global = None
        mejor_ejecucion = -1
        mejor_semilla = -1
        
        for ejecucion in range(1, 11):
            semilla = 41 + ejecucion
            print(f"Ejecución {ejecucion}/10 (semilla={semilla})... ", end='', flush=True)
            
            resultado = algoritmo_genetico(ciudades, config, semilla)
            
            resultados.append({
                'Gladiador': config['nombre'],
                'Ejecucion': ejecucion,
                'Semilla': semilla,
                'Distancia_Mejor': round(resultado['mejor_distancia'], 2),
                'Distancia_Promedio': round(resultado['distancia_promedio'], 2),
                'Desv_Estandar': round(resultado['desv_std'], 2),
                'Tiempo_seg': round(resultado['tiempo'], 4)
            })
            
            print(f"> Distancia: {resultado['mejor_distancia']:.2f} km")
            
            if resultado['mejor_distancia'] < mejor_dist_global:
                mejor_dist_global = resultado['mejor_distancia']
                mejor_ruta_global = resultado['mejor_ruta']
                mejor_ejecucion = ejecucion
                mejor_semilla = semilla
                
        # Guardar mejor ruta del gladiador para txt
        mejores_rutas_texto += f"Gladiador: {config['nombre']}\n"
        mejores_rutas_texto += f"Mejor ejecución: Semilla {mejor_semilla}\n"
        mejores_rutas_texto += f"Distancia: {mejor_dist_global:.2f} km\n"
        mejores_rutas_texto += f"Ruta: {mejor_ruta_global}\n\n"
    
    # Escribir txt con las mejores rutas
    with open('equipo_1_mejores_rutas.txt', 'w', encoding='utf-8') as f:
        f.write(mejores_rutas_texto)
        
    return resultados

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    archivo = 'ciudades_30.txt'
    resultados = ejecutar_torneo(archivo)
    
    # Guardar CSV
    df = pd.DataFrame(resultados)
    df.to_csv('equipo_1_resultados.csv', index=False)
    
    print("\n" + "="*60)
    print("TORNEO COMPLETADO")
    print("="*60)
    print("Archivos generados:")
    print("- equipo_1_resultados.csv")
    print("- equipo_1_mejores_rutas.txt")
