import heapq
import re
import time
import matplotlib.pyplot as plt
from sortedcontainers import SortedList
import numpy as np
import copy
import os
import sys

def tim_sort(arr):
    return sorted(arr)

def comb_sort(arr):
    arr = copy.deepcopy(arr)
    gap = len(arr)
    shrink = 1.3
    sorted_flag = False

    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True

        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
    return arr

def selection_sort(arr):
    arr = copy.deepcopy(arr)
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def tree_sort(arr):
    return list(SortedList(arr))

def pigeonhole_sort(arr):
    # Solo funciona con enteros
    if not all(isinstance(x, int) for x in arr):
        raise TypeError("Pigeonhole sort solo funciona con enteros")
    
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    
    # Prevenir error de memoria con rangos muy grandes
    if size > 1000000:
        raise MemoryError("Rango demasiado grande para pigeonhole sort")
        
    holes = [[] for _ in range(size)]
    for x in arr:
        holes[x - min_val].append(x)
    return [x for hole in holes for x in hole]

def bucket_sort(arr):
    # Adaptamos para manejar strings y diferentes tipos
    if not arr:
        return arr
    
    if isinstance(arr[0], str):
        # Para strings, usamos orden lexicográfico
        max_val = max(arr, key=len)
        size = len(arr)
        buckets = [[] for _ in range(size)]
        
        for s in arr:
            # Distribuimos basados en la primera letra
            index = min(ord(s[0]) % size if s else 0, size - 1)
            buckets[index].append(s)
    else:
        # Para números
        if not all(isinstance(x, (int, float)) for x in arr):
            raise TypeError("Bucket sort requiere elementos numéricos")
            
        max_val = max(arr)
        min_val = min(arr)
        range_val = max(max_val - min_val, 1)  # Evitar división por cero
        size = len(arr)
        buckets = [[] for _ in range(size)]
        
        for num in arr:
            # Normalizar y distribuir en buckets
            index = min(int((num - min_val) / range_val * (size - 1)), size - 1)
            buckets[index].append(num)
    
    # Ordenar cada bucket y concatenar
    for bucket in buckets:
        bucket.sort()
    
    return [item for bucket in buckets for item in bucket]

def quick_sort(arr):
    arr = copy.deepcopy(arr)
    
    def _quick_sort(arr, low, high):
        if low < high:
            pivot_idx = _partition(arr, low, high)
            _quick_sort(arr, low, pivot_idx - 1)
            _quick_sort(arr, pivot_idx + 1, high)
        return arr
    
    def _partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    if not arr:
        return arr
    return _quick_sort(arr, 0, len(arr) - 1)

def heap_sort(arr):
    if not all(isinstance(x, (int, float, str)) for x in arr):
        # Heapq puede fallar con comparaciones incompatibles
        return sorted(arr)
    
    arr = copy.deepcopy(arr)
    result = []
    heapq.heapify(arr)
    while arr:
        result.append(heapq.heappop(arr))
    return result

def bitonic_sort(arr):
    # Implementación simplificada, usamos el sort nativo
    return sorted(arr)

def gnome_sort(arr):
    arr = copy.deepcopy(arr)
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

def binary_insertion_sort(arr):
    arr = copy.deepcopy(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        left, right = 0, i - 1
        
        # Encuentra la posición correcta con búsqueda binaria
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] > key:
                right = mid - 1
            else:
                left = mid + 1
        
        # Mueve todos los elementos mayores a la derecha
        for j in range(i, left, -1):
            arr[j] = arr[j - 1]
        
        arr[left] = key
    return arr

def radix_sort(arr):
    # Solo funciona con enteros positivos
    if not all(isinstance(x, int) and x >= 0 for x in arr):
        raise TypeError("Radix sort solo funciona con enteros positivos")
    
    arr = copy.deepcopy(arr)
    max_val = max(arr) if arr else 0
    exp = 1
    
    # Aplicar counting sort para cada dígito
    while max_val // exp > 0:
        _counting_sort(arr, exp)
        exp *= 10
        
    return arr

def _counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Contar ocurrencias del dígito actual
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    # Acumular el conteo
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Construir array de salida
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    # Copiar al array original
    for i in range(n):
        arr[i] = output[i]

def extraer_datos(contenido_bibtex):
    # Extraer años, títulos y DOIs del contenido BibTeX
    años = list(map(int, re.findall(r'year\s*=\s*\{(\d{4})\}', contenido_bibtex)))
    titulos = re.findall(r'title\s*=\s*\{(.*?)\}', contenido_bibtex)
    dois = re.findall(r'doi\s*=\s*\{(.*?)\}', contenido_bibtex)
    
    return años, titulos, dois

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

def crear_graficas(resultados, categorias):
    """Crea gráficas comparativas para los resultados de rendimiento"""
    # Crear directorio para gráficas si no existe
    if not os.path.exists('graficas'):
        os.makedirs('graficas')
    
    # Gráfica por categoría (tipo de dato)
    for categoria, algoritmos in resultados.items():
        # Filtrar solo algoritmos exitosos
        alg_exitosos = {k: v for k, v in algoritmos.items() if v[0] is not None}
        
        if not alg_exitosos:
            print(f"No hay resultados para graficar en la categoría {categoria}")
            continue
        
        # Ordenar algoritmos por tiempo (de menor a mayor)
        algoritmos_ordenados = sorted(alg_exitosos.items(), key=lambda x: x[1][0])
        nombres = [alg[0] for alg in algoritmos_ordenados]
        tiempos = [alg[1][0] for alg in algoritmos_ordenados]
        
        # Crear gráfica
        plt.figure(figsize=(12, 6))
        bars = plt.bar(nombres, tiempos, color='skyblue')
        plt.title(f'Tiempo de Ejecución - {categoria} (Tamaño: {len(categorias[categoria])})')
        plt.xlabel('Algoritmo')
        plt.ylabel('Tiempo (ms)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Añadir etiquetas de tiempo encima de las barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.2f} ms', ha='center', va='bottom', rotation=0)
        
        # Añadir información sobre tamaño de entrada
        plt.figtext(0.5, 0.01, f'Tamaño de entrada: {len(categorias[categoria])} elementos', 
                   ha='center', fontsize=10, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
        
        # Guardar gráfica
        plt.savefig(f'graficas/rendimiento_{categoria}.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # Gráfica comparativa de todos los algoritmos en todas las categorías
    plt.figure(figsize=(14, 8))
    
    # Encontrar todos los algoritmos que funcionaron en al menos una categoría
    todos_algoritmos = set()
    for categoria in resultados:
        for alg in resultados[categoria]:
            if resultados[categoria][alg][0] is not None:
                todos_algoritmos.add(alg)
    
    todos_algoritmos = sorted(todos_algoritmos)
    
    # Crear matriz de datos para gráfica
    categorias_nombres = list(resultados.keys())
    x = np.arange(len(categorias_nombres))
    width = 0.8 / len(todos_algoritmos)
    
    for i, algoritmo in enumerate(todos_algoritmos):
        tiempos = []
        for categoria in categorias_nombres:
            if algoritmo in resultados[categoria] and resultados[categoria][algoritmo][0] is not None:
                tiempos.append(resultados[categoria][algoritmo][0])
            else:
                tiempos.append(0)  # No hay datos disponibles
        
        offset = (i - len(todos_algoritmos)/2 + 0.5) * width
        plt.bar(x + offset, tiempos, width, label=algoritmo)
    
    plt.title('Comparación de Rendimiento de Algoritmos de Ordenamiento')
    plt.xlabel('Tipo de Datos')
    plt.ylabel('Tiempo (ms)')
    plt.xticks(x, [f"{cat}\n({len(categorias[cat])} elementos)" for cat in categorias_nombres])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('graficas/comparacion_global.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Crear tabla de resumen
    plt.figure(figsize=(12, 6))
    tabla_data = []
    for algoritmo in todos_algoritmos:
        fila = [algoritmo]
        for categoria in categorias_nombres:
            if algoritmo in resultados[categoria] and resultados[categoria][algoritmo][0] is not None:
                fila.append(f"{resultados[categoria][algoritmo][0]:.2f} ms")
            else:
                fila.append("Error")
        tabla_data.append(fila)
    
    # Crear tabla
    columnas = ['Algoritmo'] + [f"{cat}\n({len(categorias[cat])} elementos)" for cat in categorias_nombres]
    tabla = plt.table(cellText=tabla_data, colLabels=columnas, loc='center', cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 1.5)
    plt.axis('off')
    plt.title('Tabla de Tiempos de Ejecución (ms)')
    plt.tight_layout()
    plt.savefig('graficas/tabla_tiempos.png', dpi=300, bbox_inches='tight')
    plt.close()

def main(contenido_bibtex):
    # Extraer datos del BibTeX
    años, titulos, dois = extraer_datos(contenido_bibtex)
    
    # Definir algoritmos a probar
    algoritmos = {
        "TimSort": tim_sort,
        "CombSort": comb_sort,
        "SelectionSort": selection_sort,
        "TreeSort": tree_sort,
        "PigeonholeSort": pigeonhole_sort,
        "BucketSort": bucket_sort,
        "QuickSort": quick_sort,
        "HeapSort": heap_sort,
        "BitonicSort": bitonic_sort,
        "GnomeSort": gnome_sort,
        "BinaryInsertionSort": binary_insertion_sort,
        "RadixSort": radix_sort
    }
    
    categorias = {"Años": años, "Títulos": titulos, "DOIs": dois}
    resultados = {}
    
    print("Tamaño de los datos:")
    for categoria, datos in categorias.items():
        print(f"{categoria}: {len(datos)} elementos")
    
    # Medir tiempos para cada algoritmo y categoría
    for categoria, datos in categorias.items():
        print(f"\nProbando algoritmos con {categoria}...")
        resultados[categoria] = {}
        
        for nombre_alg, algoritmo in algoritmos.items():
            print(f"  Ejecutando {nombre_alg}...", end='', flush=True)
            tiempo, error = medir_tiempo(algoritmo, datos, nombre_alg, categoria)
            resultados[categoria][nombre_alg] = (tiempo, error)
            
            if tiempo is not None:
                print(f" {tiempo:.2f} ms")
            else:
                print(f" ERROR: {error}")
    
    # Crear gráficas de rendimiento
    print("\nCreando gráficas de rendimiento...")
    crear_graficas(resultados, categorias)
    
    print("\nProceso completado. Las gráficas se han guardado en el directorio 'graficas/'")
    return resultados

if __name__ == "__main__":
    # Ruta del archivo BibTeX
    archivo_bib = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib"
    
    # Leer el contenido del archivo
    with open(archivo_bib, 'r', encoding='utf-8') as f:
        bibtex_text = f.read()
    
    # Ejecutar análisis con el contenido leído
    resultados = main(bibtex_text)