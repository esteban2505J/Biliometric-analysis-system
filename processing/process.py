   
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
   
# Functions imported
from extract_data.extract_data import extract_data
from measure_time.measure_time_algoriths import measure_algorithm_time
from graphics.create.create_graphics import create_graphs


#Algorithms imported
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




def main(bibtex_text):
    # Extraer datos del BibTeX
    años, titulos, dois, abstracts  = extract_data(bibtex_text)

    
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
    
    categorias = {"Años": años, "Títulos": titulos, "DOIs": dois, "Abstracts": abstracts}
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
            tiempo, error = measure_algorithm_time(algoritmo, datos, nombre_alg, categoria)
            resultados[categoria][nombre_alg] = (tiempo, error)
            
            
            if tiempo is not None:
                print(f" {tiempo:.2f} ms")
            else:
                print(f" ERROR: {error}")
    
    # Crear gráficas de rendimiento
    print("\nCreando gráficas de rendimiento...")
    create_graphs(resultados, categorias)
    
    print("\nProceso completado. Las gráficas se han guardado en el directorio 'graphics/'")
    return resultados

if __name__ == "__main__":
    # Ruta del archivo BibTeX
    archivo_bib = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib"
    
    # Leer el contenido del archivo
    with open(archivo_bib, 'r', encoding='utf-8') as f:
        bibtex_text = f.read()
    
    # Ejecutar análisis con el contenido leído
    resultados = main(bibtex_text)