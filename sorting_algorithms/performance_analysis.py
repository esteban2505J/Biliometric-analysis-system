import time
import random
import matplotlib.pyplot as plt
from algorithms import (
    tim_sort, comb_sort, selection_sort, tree_sort, pigeonhole_sort,
    bucket_sort, quick_sort, heap_sort, bitonic_sort, gnome_sort,
    binary_insertion_sort, radix_sort
)

def measure_time(sort_func, data):
    start_time = time.time()
    sort_func(data.copy())
    end_time = time.time()
    return end_time - start_time

# Datos de ejemplo
data = [random.randint(1, 1000) for _ in range(1000)]

# Algoritmos de ordenamiento
algorithms = {
    "TimSort": tim_sort,
    "Comb Sort": comb_sort,
    "Selection Sort": selection_sort,
    "Tree Sort": tree_sort,
    "Pigeonhole Sort": pigeonhole_sort,
    "Bucket Sort": bucket_sort,
    "QuickSort": quick_sort,
    "HeapSort": heap_sort,
    "Bitonic Sort": bitonic_sort,
    "Gnome Sort": gnome_sort,
    "Binary Insertion Sort": binary_insertion_sort,
    "RadixSort": radix_sort
}

# Medir tiempos
times = {name: measure_time(func, data) for name, func in algorithms.items()}

# Mostrar resultados
for name, time_taken in times.items():
    print(f"{name}: {time_taken:.6f} segundos")

# Crear diagrama de barras
plt.figure(figsize=(12, 8))
plt.bar(times.keys(), times.values(), color='skyblue')
plt.xlabel('Algoritmos de Ordenamiento')
plt.ylabel('Tiempo (segundos)')
plt.title('Comparación de Tiempos de Algoritmos de Ordenamiento')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()