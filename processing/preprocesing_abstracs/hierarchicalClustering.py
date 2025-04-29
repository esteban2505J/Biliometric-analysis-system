# hierarchical_clustering.py

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import silhouette_score

def single_linkage_clustering(X):
    Z = linkage(X.toarray(), method='single')
    return Z

def complete_linkage_clustering(X):
    Z = linkage(X.toarray(), method='complete')
    return Z

def plot_dendrogram(Z, labels=None, title='Dendrogram'):
    plt.figure(figsize=(12, 8))
    if labels is not None and len(labels) == Z.shape[0] + 1:  # linkage produce n-1 clusters
        dendrogram(
            Z,
            labels=labels,
            leaf_rotation=90,
            leaf_font_size=10
        )
    else:
        print("⚠️  Labels y linkage size no coinciden, se graficará sin etiquetas.")
        dendrogram(
            Z,
            leaf_rotation=90,
            leaf_font_size=10
        )
    plt.title(title)
    plt.xlabel('Abstracts')
    plt.ylabel('Distancia')
    plt.tight_layout()
    plt.show()