# clustering/evaluator.py
from scipy.cluster.hierarchy import fcluster
from collections import defaultdict
import numpy as np
import pandas as pd
from clustering.visualizer import plot_category_distribution

def evaluate_clustering(linkage_matrix_1, linkage_matrix_2, abstracts, abstract_ids, categories, n_clusters=5):
    """
    Evaluate clustering coherence and save assignments.
    
    Args:
        linkage_matrix_1 (np.ndarray): Linkage matrix for algorithm 1
        linkage_matrix_2 (np.ndarray): Linkage matrix for algorithm 2
        abstracts (list): List of abstracts
        abstract_ids (list): List of abstract IDs
        categories (dict): Dictionary of categories and terms
        n_clusters (int): Number of clusters
    
    Returns:
        dict: Evaluation results
    """
    if linkage_matrix_1 is None or linkage_matrix_2 is None:
        print("No se pueden evaluar clusters: falta al menos una matriz de linkage.")
        return {"error": "Matrices de linkage incompletas"}
    
    try:
        print(f"Calculando {n_clusters} clusters para cada algoritmo...")
        clusters1 = fcluster(linkage_matrix_1, n_clusters, criterion='maxclust')
        clusters2 = fcluster(linkage_matrix_2, n_clusters, criterion='maxclust')
        
        results = {}
        
        def analyze_categories_in_clusters(clusters):
            print("Analizando categorías en clusters...")
            cluster_categories = {}
            flat_categories = {}
            for cat, terms in categories.items():
                flat_terms = []
                for term in terms:
                    if ' - ' in term:
                        for subterm in term.split(' - '):
                            flat_terms.append(subterm.lower())
                    else:
                        flat_terms.append(term.lower())
                flat_categories[cat] = flat_terms
            
            for cluster_id in range(1, n_clusters + 1):
                print(f"Analizando cluster {cluster_id}...")
                cluster_indices = [i for i, c in enumerate(clusters) if c == cluster_id]
                cluster_abstracts = [abstracts[i] for i in cluster_indices]
                category_counts = defaultdict(int)
                
                for abstract in cluster_abstracts:
                    abstract_lower = abstract.lower()
                    for cat, terms in flat_categories.items():
                        for term in terms:
                            if term in abstract_lower:
                                category_counts[cat] += 1
                                break
                
                if cluster_abstracts:
                    for cat in category_counts:
                        category_counts[cat] /= len(cluster_abstracts)
                
                cluster_categories[cluster_id] = dict(category_counts)
            
            return cluster_categories
        
        print("Analizando categorías para algoritmo 1...")
        results['algorithm1'] = analyze_categories_in_clusters(clusters1)
        print("Analizando categorías para algoritmo 2...")
        results['algorithm2'] = analyze_categories_in_clusters(clusters2)
        
        print("Visualizando resultados...")
        plot_category_distribution(results['algorithm1'], list(categories.keys()), 'algorithm1', 'Algoritmo 1')
        plot_category_distribution(results['algorithm2'], list(categories.keys()), 'algorithm2', 'Algoritmo 2')
        
        def calculate_coherence(cluster_data):
            coherence_scores = []
            for cluster_id, category_scores in cluster_data.items():
                values = list(category_scores.values())
                if values:
                    variance = np.var(values)
                    max_variance = np.var([1.0] + [0.0] * (len(values) - 1))
                    if max_variance > 0:
                        normalized_variance = variance / max_variance
                    else:
                        normalized_variance = 0.0
                    coherence_scores.append(normalized_variance)
                else:
                    coherence_scores.append(0.0)
            return np.mean(coherence_scores) if coherence_scores else 0.0
        
        coherence1 = calculate_coherence(results['algorithm1'])
        coherence2 = calculate_coherence(results['algorithm2'])
        
        results['coherence'] = {
            'algorithm1': coherence1,
            'algorithm2': coherence2,
            'best_algorithm': 'algorithm1' if coherence1 > coherence2 else 'algorithm2'
        }
        
        print(f"Coherencia del Algoritmo 1: {coherence1:.4f}")
        print(f"Coherencia del Algoritmo 2: {coherence2:.4f}")
        print(f"El mejor algoritmo es: {'Algoritmo 1' if coherence1 > coherence2 else 'Algoritmo 2'}")
        
        # Save cluster assignments
        data = {
            'Abstract_ID': abstract_ids,
            'Cluster_Ward': clusters1,
            'Cluster_AGNES': clusters2
        }
        df = pd.DataFrame(data)
        df.to_csv('cluster_assignments.csv', index=False)
        print("Cluster assignments saved to 'cluster_assignments.csv'.")
        
        return results
    except Exception as e:
        print(f"Error en la evaluación de clusters: {str(e)}")
        return {"error": str(e)}