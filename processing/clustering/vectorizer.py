# clustering/vectorizer.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_tfidf_and_similarity(processed_abstracts):
    """
    Calculate TF-IDF matrix and similarity/distance matrices.
    
    Args:
        processed_abstracts (list): Preprocessed abstracts
    
    Returns:
        tuple: (tfidf_matrix, similarity_matrix, distance_matrix)
    """
    if not processed_abstracts:
        print("No hay abstracts procesados para calcular TF-IDF.")
        return None, None, None
    
    try:
        # Calculate TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(processed_abstracts)
        print(f"Se ha calculado la matriz TF-IDF con forma {tfidf_matrix.shape}.")
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        np.fill_diagonal(similarity_matrix, 1.0)  # Ensure diagonal is 1.0
        distance_matrix = 1.0 - similarity_matrix
        np.fill_diagonal(distance_matrix, 0.0)   # Ensure diagonal is 0.0
        distance_matrix = np.clip(distance_matrix, 0.0, None)  # Prevent negative values
        print(f"Se ha calculado la matriz de similitud con forma {similarity_matrix.shape}.")
        
        return tfidf_matrix, similarity_matrix, distance_matrix
    except Exception as e:
        print(f"Error al calcular TF-IDF o similitud: {str(e)}")
        return None, None, None