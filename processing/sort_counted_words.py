   

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.search_algorithms.prefix_trie import count_words_abstracts



# Algorithms imported
from algorithms.tim_sort import tim_sort
from algorithms.comb_sort import comb_sort
from algorithms.selection_sort import selection_sort
from algorithms.tree_sort import tree_sort
from algorithms.pigeonhole_sort import pigeonhole_sort
from algorithms.bucket_sort import bucket_sort
from algorithms.quick_sort import quick_sort
from algorithms.heap_sort import heap_sort
from algorithms.bitonic_sort import bitonic_sort
from algorithms.gnome_sort import gnome_sort
from algorithms.binary_insertion_sort import binary_insertion_sort
from algorithms.radix_sort import radix_sort
from algorithms.bubble_sort import bubble_sort
from algorithms.cocktail_shaker_sort import cocktail_shaker_sort

# Import utils functions
from measure_time.measure_time_algoriths import measure_algorithm_time
from graphics.create.create_graphics import create_graphs,create_graphs_words


def main():
    file_path = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib"
    
    # Obtener el conteo de palabras
    counted_words = count_words_abstracts(file_path)
    
    if not isinstance(counted_words, dict):
        print("El resultado de count_words_abstracts no es un diccionario.")
        return
    
    # Obtener solo las frecuencias en una lista
    word_frequencies = list(counted_words.values())

    # Diccionario inverso {frecuencia: [palabras]}
    frequency_to_words = {}
    for word, freq in counted_words.items():
        if freq not in frequency_to_words:
            frequency_to_words[freq] = []
        frequency_to_words[freq].append(word)
    
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
        "RadixSort": radix_sort,
        "BubbleSort": bubble_sort,
        "Cocktail_shaker_sort": cocktail_shaker_sort
    }

    resultados = {}

    # Medir tiempos y ordenar frecuencias con cada algoritmo
    for nombre_alg, algoritmo in algoritmos.items():
        print(f"\nEjecutando {nombre_alg}...")

        # Copia de la lista original para evitar modificarla
        frequencies_copy = word_frequencies[:]

        try:
            # Aplicar el algoritmo de ordenamiento
            sorted_frequencies = algoritmo(frequencies_copy)

            # Medir tiempo de ejecución
            tiempo, error = measure_algorithm_time(algoritmo, frequencies_copy, nombre_alg, "word_frequencies")

            resultados[nombre_alg] = {
                "sorted_frequencies": sorted_frequencies,
                "word": list(counted_words.keys()),
                "tiempo": tiempo,
                "error": error
            }
                      
    
            # Reconstruir la lista de palabras en el orden del algoritmo
            sorted_words = [(word, freq) for freq in sorted_frequencies for word in frequency_to_words[freq]]

            # Mostrar los resultados ordenados
            print(f"{'Palabra':<20} | {'Frecuencia'}")
            print("-" * 30)
            
            # Crear las gráficas
            create_graphs_words(resultados)
    
            for word, freq in sorted_words[:15]:  # Mostrar solo las 15 más frecuentes
                print(f"{word:<20} | {freq}")

            if tiempo is not None:
                print(f"\nTiempo de ejecución: {tiempo:.2f} µs\n")
            else:
                print(f"\nERROR: {error}\n")

        except Exception as e:
            print(f"Error ejecutando {nombre_alg}: {e}")

if __name__ == "__main__":
    main()