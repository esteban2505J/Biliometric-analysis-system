import re
import bibtexparser

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# imports for clustering and similarity
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
    clean_text = ' '.join(tokens)
    
    return clean_text


    
def main():
    with open(r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib", encoding="utf-8") as file:
        bib_content = bibtexparser.load(file)
        
    abstracts = []
    for entry in bib_content.entries:
        if 'abstract' in entry:
            original_abstract = entry['abstract']
            cleaned_abstract = clean_text(original_abstract)
            title = entry['title']
            abstracts.append({'title': title, 'abstract': cleaned_abstract})
            
    return abstracts
    
    
def vectorize_abstracts(abstracts_cleaned):
    abstracts = [article['abstract'] for article in abstracts_cleaned]  # extraer solo los textos
    
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
    
    # Evitar duplicados mirando solo la parte superior de la matriz
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            pairs.append((i, j, similarities[i, j]))
    
    # Ordenar por similitud descendente
    pairs = sorted(pairs, key=lambda x: x[2], reverse=True)
    
    # Mostrar top_n pares más similares
    for idx1, idx2, sim in pairs[:top_n]:
        print(f"\nAbstract {idx1} ({abstracts_cleaned[idx1]['title']})")
        print(f"Abstract {idx2} ({abstracts_cleaned[idx2]['title']})")
        print(f"Similitud: {sim:.4f}")
        print("-" * 80)
        
        
if __name__ == "__main__":
    abstracts_cleaned = main()
    X, vectorizer = vectorize_abstracts(abstracts_cleaned)
    
    similarities = calculate_similarities(X)
    clusters = cluster_abstracts(X, num_clusters=5)
    
    show_most_similar(similarities, abstracts_cleaned, top_n=5)

    # # Mostrar resultados
    # for i, article in enumerate(abstracts_cleaned):
    #     print(f"Título: {article['title']}")
    #     print(f"Cluster asignado: {clusters[i]}")
    #     print("-" * 50)
    
        
   
    
    
            
    