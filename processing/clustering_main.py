import warnings
from clustering import (
    load_bibtex, preprocess_abstracts, calculate_tfidf_and_similarity,
    hierarchical_clustering_ward, hierarchical_clustering_agnes,
    plot_dendrogram, plot_similarity_heatmap, evaluate_clustering
)
from clustering.config import BIBTEX_FILE_PATH, CATEGORIES

# Suppress warnings
warnings.filterwarnings("ignore")

def main():
    """Execute the hierarchical clustering pipeline."""
    try:
        # Load and preprocess data
        abstracts, abstract_ids = load_bibtex(BIBTEX_FILE_PATH, sample_size=1.0, random_seed=42)
        if not abstracts:
            print("No se pudo continuar debido a la falta de abstracts.")
            return
        
        processed_abstracts = preprocess_abstracts(abstracts)
        tfidf_matrix, similarity_matrix, distance_matrix = calculate_tfidf_and_similarity(processed_abstracts)
        if distance_matrix is None:
            print("No se pudo continuar debido a errores en la vectorización.")
            return
        
        # Apply clustering
        Z1 = hierarchical_clustering_ward(distance_matrix)
        Z2 = hierarchical_clustering_agnes(distance_matrix)
        
        # Plot visualizations
        plot_dendrogram(Z1, abstract_ids, 'Ward', max_d=1.0)
        plot_dendrogram(Z2, abstract_ids, 'AGNES', max_d=1.0)
        plot_similarity_heatmap(similarity_matrix, abstract_ids, max_size=50, random_seed=42)
        
        # Evaluate clustering
        evaluate_clustering(Z1, Z2, abstracts, abstract_ids, CATEGORIES, n_clusters=5)
        
    except Exception as e:
        print(f"Error en la ejecución del pipeline: {str(e)}")

if __name__ == '__main__':
    try:
        import bibtexparser
    except ModuleNotFoundError:
        print("Error: 'bibtexparser' module not found. Please install it using 'pip install bibtexparser'.")
        exit(1)
    main()