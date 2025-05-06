# clustering/clustering_algorithms.py
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
import numpy as np
import traceback

def hierarchical_clustering_ward(distance_matrix):
    """
    Apply hierarchical clustering using Ward's method.
    
    Args:
        distance_matrix (np.ndarray): Distance matrix
    
    Returns:
        np.ndarray: Linkage matrix
    """
    if distance_matrix is None:
        print("No hay matriz de distancia calculada.")
        return None
    
    try:
        print("Convirtiendo matriz de distancia a formato condensado...")
        condensed_dist = squareform(distance_matrix)
        print("Aplicando clustering jerárquico con método Ward...")
        linkage_matrix = linkage(condensed_dist, method='ward')
        print("Se ha aplicado clustering jerárquico usando el método Ward.")
        return linkage_matrix
    except Exception as e:
        print(f"Error en clustering jerárquico Ward: {str(e)}")
        traceback.print_exc()
        return None

def hierarchical_clustering_agnes(distance_matrix):
    """
    Apply hierarchical clustering using AGNES (Agglomerative Nesting).
    
    Args:
        distance_matrix (np.ndarray): Distance matrix
    
    Returns:
        np.ndarray: Linkage matrix
    """
    if distance_matrix is None:
        print("No hay matriz de distancia calculada.")
        return None
    
    try:
        print("Iniciando algoritmo AGNES...")
        n = len(distance_matrix)
        
        if n > 1000:
            print("Conjunto de datos grande detectado. Usando implementación simplificada de AGNES...")
            condensed_dist = squareform(distance_matrix)
            linkage_matrix = linkage(condensed_dist, method='average')
            print("Se ha aplicado clustering jerárquico AGNES (versión simplificada).")
            return linkage_matrix
        
        print(f"Procesando {n} abstracts con AGNES completo...")
        clusters = [[i] for i in range(n)]
        Z = np.zeros((n-1, 4))
        cluster_dict = {i: i for i in range(n)}
        next_cluster_id = n
        
        for i in range(n-1):
            if i % 100 == 0:
                print(f"AGNES: Procesando fusión {i+1} de {n-1}...")
            
            min_dist = float('inf')
            min_i, min_j = -1, -1
            
            for ci in range(len(clusters)):
                for cj in range(ci+1, len(clusters)):
                    dist_sum = 0
                    count = 0
                    for idx1 in clusters[ci]:
                        for idx2 in clusters[cj]:
                            dist_sum += distance_matrix[idx1, idx2]
                            count += 1
                    cluster_dist = dist_sum / count
                    if cluster_dist < min_dist:
                        min_dist = cluster_dist
                        min_i, min_j = ci, cj
            
            merged_cluster = clusters[min_i] + clusters[min_j]
            Z[i, 0] = cluster_dict[min_i]
            Z[i, 1] = cluster_dict[min_j]
            Z[i, 2] = min_dist
            Z[i, 3] = len(merged_cluster)
            
            cluster_dict[next_cluster_id] = next_cluster_id
            next_cluster_id += 1
            
            clusters.pop(max(min_i, min_j))
            clusters.pop(min(min_i, min_j))
            clusters.append(merged_cluster)
        
        print("Se ha aplicado clustering jerárquico AGNES (Agglomerative Nesting).")
        return Z
    except Exception as e:
        print(f"Error en clustering jerárquico AGNES: {str(e)}")
        traceback.print_exc()
        try:
            print("Intentando método alternativo para AGNES...")
            condensed_dist = squareform(distance_matrix)
            Z = linkage(condensed_dist, method='average')
            print("Se ha aplicado clustering jerárquico AGNES (método alternativo).")
            return Z
        except Exception as e2:
            print(f"Error en método alternativo: {str(e2)}")
            return None