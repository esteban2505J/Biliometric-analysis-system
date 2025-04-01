import time
import copy

def medir_tiempo(algoritmo, datos, nombre_algoritmo, nombre_datos, n_ejecuciones=3):
    """Mide el tiempo de ejecución de un algoritmo con manejo de excepciones"""
    tiempos = []
    
    try:
        for _ in range(n_ejecuciones):
            datos_copia = copy.deepcopy(datos)  # Evitar efectos secundarios
            inicio = time.time()
            algoritmo(datos_copia)
            fin = time.time()
            tiempos.append((fin - inicio) * 1000)  # Convertir a milisegundos
        
        tiempo_promedio = sum(tiempos) / len(tiempos)
        return tiempo_promedio, None
    except Exception as e:
        print(f"Error en {nombre_algoritmo} con {nombre_datos}: {str(e)}")
        return None, str(e)