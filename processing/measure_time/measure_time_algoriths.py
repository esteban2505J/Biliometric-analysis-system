import time
import copy

def measure_algorithm_time(algoritmo, datos, nombre_algoritmo, nombre_datos, n_ejecuciones=5):
    """Mide el tiempo de ejecución de un algoritmo con alta precisión en microsegundos"""
    tiempos = []
    
    try:
        for _ in range(n_ejecuciones):
            datos_copia = copy.deepcopy(datos)  # Evitar efectos secundarios
            inicio = time.perf_counter()  # Mayor precisión
            algoritmo(datos_copia)
            fin = time.perf_counter()
            tiempos.append((fin - inicio) * 1_000_000)  # Convertir a microsegundos (µs)
        
        tiempo_promedio = sum(tiempos) / len(tiempos)
        return tiempo_promedio, None  # Retorna en µs
    except Exception as e:
        print(f"Error en {nombre_algoritmo} con {nombre_datos}: {str(e)}")
        return None, str(e)
