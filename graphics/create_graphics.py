import os
import matplotlib.pyplot as plt
import numpy as np


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