from hierarchicalClustering import (
    single_linkage_clustering,
    complete_linkage_clustering,
    plot_dendrogram)

import re
import bibtexparser

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

# Inicializar stopwords y stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


def clean_text(text):
    # 1. Minúsculas
    text = text.lower()
    
    # 2. Eliminar números y signos de puntuación
    text = re.sub(r'\d+', '', text)  # eliminar números
    text = text.translate(str.maketrans('', '', string.punctuation))  # eliminar puntuación
    
    # 3. Tokenizar
    tokens = nltk.word_tokenize(text)
    
    # 4. Eliminar stopwords
    tokens = [word for word in tokens if word not in stop_words]
    
    # 5. Stemming
    tokens = [stemmer.stem(word) for word in tokens]
    
    # 6. Unir tokens limpios en una cadena de nuevo
    clean_text_result = ' '.join(tokens)
    
    return clean_text_result


def main():
    with open(r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib", encoding="utf-8") as file:
        bib_content = bibtexparser.load(file)

    abstracts = []
    for entry in bib_content.entries:
        if 'abstract' in entry and entry['abstract'].strip():  # <-- Asegura que no esté vacío
            original_abstract = entry['abstract']
            cleaned_abstract = clean_text(original_abstract)
            title = entry['title']
            abstracts.append({'title': title, 'abstract': cleaned_abstract})
    return abstracts


def vectorize_abstracts(abstracts_cleaned):
    abstracts = [article['abstract'] for article in abstracts_cleaned]
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(abstracts)
    
    return X, vectorizer


def calculate_similarities(X):
    return cosine_similarity(X)


def cluster_abstracts(X, num_clusters=5):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    return labels


def show_most_similar(similarities, abstracts_cleaned, top_n=5):
    n = similarities.shape[0]
    pairs = []
    
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((i, j, similarities[i, j]))
    
    pairs = sorted(pairs, key=lambda x: x[2], reverse=True)
    
    for idx1, idx2, sim in pairs[:top_n]:
        print(f"\nAbstract {idx1} ({abstracts_cleaned[idx1]['title']})")
        print(f"Abstract {idx2} ({abstracts_cleaned[idx2]['title']})")
        print(f"Similitud: {sim:.4f}")
        print("-" * 80)


if __name__ == "__main__":
    # Paso 1: Cargar y limpiar abstracts
    abstracts_cleaned = main()
    
    # Paso 2: Vectorizar
    X, vectorizer = vectorize_abstracts(abstracts_cleaned)
    
    # Paso 3: Calcular similitudes
    similarities = calculate_similarities(X)
    
    # Paso 4: Clustering con KMeans
    clusters = cluster_abstracts(X, num_clusters=5)
    
    # Paso 5: Mostrar abstracts más similares
    show_most_similar(similarities, abstracts_cleaned, top_n=5)
    
    # ---- Clustering Jerárquico ----
    Z_single = single_linkage_clustering(X)
    Z_complete = complete_linkage_clustering(X)

    # Extraer títulos para los dendrogramas
    titles = [article['title'] for article in abstracts_cleaned]
    
    print(f"Número de abstracts: {len(abstracts_cleaned)}")
    print(f"Shape de X: {X.shape}")
    print(f"Número de títulos: {len(titles)}")

    # Plot Dendrogramas
    plot_dendrogram(Z_single, labels=titles, title='Single Linkage Dendrogram')
    plot_dendrogram(Z_complete, labels=titles, title='Complete Linkage Dendrogram')

