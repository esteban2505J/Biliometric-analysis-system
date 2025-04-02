#import count_words
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

# Import utils functions
from measure_time.measure_time_algoriths import measure_algorithm_time


def main():
    file_path = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib"
    
    # Llamar la función correctamente
    counted_words = count_words_abstracts(file_path)
    
    # Verificar si counted_words es un diccionario
    if not isinstance(counted_words, dict):
        print("El resultado de count_words_abstracts no es un diccionario.")
        return
    
    # Obtener solo las frecuencias en una lista
    word_frequencies = list(counted_words.values())

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

    resultados = {}

    # Medir tiempos y ordenar frecuencias con cada algoritmo
    for nombre_alg, algoritmo in algoritmos.items():
        print(f"\nEjecutando {nombre_alg}...")

        # Crear copia de la lista original para evitar modificarla
        frequencies_copy = word_frequencies[:]

        try:
            # Aplicar el algoritmo de ordenamiento sobre la lista de frecuencias
            sorted_frequencies = algoritmo(frequencies_copy)

            # Medir tiempo de ejecución
            tiempo, error = measure_algorithm_time(algoritmo, frequencies_copy, nombre_alg, "word_frequencies")

            resultados[nombre_alg] = {
                "sorted_frequencies": sorted_frequencies,
                "tiempo": tiempo,
                "error": error
            }

            # Recuperar las palabras correspondientes a las frecuencias ordenadas
            sorted_words = sorted(counted_words.items(), key=lambda x: x[1], reverse=True)

            # Mostrar los resultados ordenados
            print(f"{'Palabra':<20} | {'Frecuencia'}")
            print("-" * 30)
            for word, freq in sorted_words[:10]:  # Mostrar solo las 10 más frecuentes
                print(f"{word:<20} | {freq}")

            if tiempo is not None:
                print(f"\nTiempo de ejecución: {tiempo:.2f} ms\n")
            else:
                print(f"\nERROR: {error}\n")

        except Exception as e:
            print(f"Error ejecutando {nombre_alg}: {e}")

if __name__ == "__main__":
    main()
