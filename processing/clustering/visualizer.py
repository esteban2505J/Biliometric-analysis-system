# clustering/visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
import os
from scipy.cluster.hierarchy import dendrogram

# Define the output directory for saving images
OUTPUT_DIR = r'C:\Users\newUs\Documents\uni\projects\bibliometricProject\graphics\clustering'

def plot_dendrogram(linkage_matrix, abstract_ids, method_name, max_d=None, color_threshold=None, truncate_mode='lastp', p=30):
    """
    Plot and save hierarchical clustering dendrogram.
    
    Args:
        linkage_matrix (np.ndarray): Linkage matrix
        abstract_ids (list): List of abstract IDs
        method_name (str): Clustering method name
        max_d (float): Maximum distance for horizontal line
        color_threshold (float): Threshold for coloring clusters
        truncate_mode (str): Truncation mode for large datasets
        p (int): Number of leaves to show if truncated
    """
    if linkage_matrix is None:
        print(f"No se puede generar dendrograma para {method_name}: matriz de linkage no disponible.")
        return
    
    try:
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        plt.figure(figsize=(20, 12))  # Increased figure size for more clusters
        
        plt.title(f'Dendrograma Jerárquico - Método {method_name}', fontsize=20)
        
        # Dynamically set p to at least 70% of the number of abstracts
        n_abstracts = len(abstract_ids)
        p = max(30, int(n_abstracts * 0.7))  # Minimum 30, but at least 70% of abstracts
        
        labels = None
        if n_abstracts <= 50:
            labels = abstract_ids
            truncate_mode = None
        else:
            labels = None  # Labels are omitted with truncation
        
        dendrogram(
            linkage_matrix,
            labels=labels,
            orientation='top',
            leaf_rotation=90,
            leaf_font_size=8,
            color_threshold=color_threshold,
            truncate_mode=truncate_mode,
            p=p if truncate_mode else None
        )
        
        if max_d:
            plt.axhline(y=max_d, c='k', ls='--', lw=1)
            plt.text(plt.xlim()[1], max_d, f'Distancia límite: {max_d:.2f}', 
                    va='center', ha='left', fontsize=12)
        
        plt.xlabel('Abstracts', fontsize=16)
        plt.ylabel('Distancia', fontsize=16)
        plt.tight_layout()
        
        # Save to specified directory
        output_path = os.path.join(OUTPUT_DIR, f'dendrograma_{method_name.lower()}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Dendrograma guardado en: {output_path}")
    except Exception as e:
        print(f"Error al generar dendrograma para {method_name}: {str(e)}")
        
def plot_similarity_heatmap(similarity_matrix, abstract_ids, max_size=100, random_seed=42):
    """
    Plot and save similarity matrix as a heatmap.
    
    Args:
        similarity_matrix (np.ndarray): Similarity matrix
        abstract_ids (list): List of abstract IDs
        max_size (int): Maximum matrix size for visualization
        random_seed (int): Seed for subsampling
    """
    if similarity_matrix is None:
        print("No hay matriz de similitud calculada.")
        return
    
    try:
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        if similarity_matrix.shape[0] > max_size:
            random.seed(random_seed)
            indices = random.sample(range(similarity_matrix.shape[0]), max_size)
            sample_matrix = similarity_matrix[np.ix_(indices, indices)]
            sample_ids = [abstract_ids[i] for i in indices]
            print(f"Matriz muy grande. Mostrando submuestra de {max_size}x{max_size}.")
            plt.figure(figsize=(14, 12))
            sns.heatmap(sample_matrix, annot=False, cmap='viridis', 
                       xticklabels=sample_ids, yticklabels=sample_ids)
            plt.title('Mapa de Calor - Similitud entre Abstracts (Muestra)', fontsize=18)
        else:
            plt.figure(figsize=(14, 12))
            sns.heatmap(similarity_matrix, annot=False, cmap='viridis', 
                       xticklabels=abstract_ids, yticklabels=abstract_ids)
            plt.title('Mapa de Calor - Similitud entre Abstracts', fontsize=18)
        
        plt.xticks(rotation=90, fontsize=8)
        plt.yticks(rotation=0, fontsize=8)
        plt.tight_layout()
        
        # Save to specified directory
        output_path = os.path.join(OUTPUT_DIR, 'mapa_calor_similitud.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Mapa de calor guardado en: {output_path}")
    except Exception as e:
        print(f"Error al generar mapa de calor: {str(e)}")

def plot_category_distribution(cluster_data, categories, algorithm_key, algorithm_name):
    """
    Plot and save category distribution across clusters as a heatmap.
    
    Args:
        cluster_data (dict): Category scores per cluster
        categories (list): List of category names
        algorithm_key (str): Algorithm identifier
        algorithm_name (str): Algorithm name for title
    """
    try:
        if not cluster_data:
            print(f"No se encontraron datos para {algorithm_name}")
            return
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        cluster_ids = list(cluster_data.keys())
        data = np.zeros((len(categories), len(cluster_ids)))
        for j, cluster_id in enumerate(cluster_ids):
            for i, category in enumerate(categories):
                data[i, j] = cluster_data[cluster_id].get(category, 0)
        
        plt.figure(figsize=(14, 10))
        sns.heatmap(data, annot=True, fmt='.2f', cmap='YlGnBu',
                    xticklabels=[f'Cluster {c}' for c in cluster_ids],
                    yticklabels=categories)
        plt.title(f'Distribución de Categorías en Clusters - {algorithm_name}', fontsize=18)
        plt.xlabel('Clusters', fontsize=14)
        plt.ylabel('Categorías', fontsize=14)
        plt.tight_layout()
        
        # Save to specified directory
        output_path = os.path.join(OUTPUT_DIR, f'distribucion_categorias_{algorithm_key}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Distribución de categorías guardada en: {output_path}")
    except Exception as e:
        print(f"Error al visualizar distribución de categorías para {algorithm_name}: {str(e)}")