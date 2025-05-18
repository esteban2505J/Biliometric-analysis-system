import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import re
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform
import seaborn as sns
from collections import defaultdict
import string
import os
import warnings
import traceback
import random
import sys

CLUSTERING_OUTPUT_DIR = "graphics/clustering"
os.makedirs(CLUSTERING_OUTPUT_DIR, exist_ok=True)

# Suppress warnings
warnings.filterwarnings("ignore")

# Download NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class HierarchicalClusteringAbstracts:
    """
    Clase que implementa el procesamiento de abstracts científicos y
    la aplicación de algoritmos de clustering jerárquico.
    """
    
    def __init__(self, bibtex_file_path, sample_size=None, random_seed=42):
        """
        Inicializa la clase con la ruta al archivo BibTeX
        
        Args:
            bibtex_file_path (str): Ruta al archivo BibTeX
            sample_size (int or float, optional): 
                Si es int, número exacto de abstracts a procesar.
                Si es float entre 0 y 1, proporción de abstracts a procesar.
                Si es None, se procesan todos los abstracts.
            random_seed (int, optional): Semilla para reproducibilidad al seleccionar muestras
        """
        self.bibtex_file_path = bibtex_file_path
        self.sample_size = sample_size
        self.random_seed = random_seed
        self.entries = None
        self.abstracts = []
        self.abstract_ids = []
        self.categories = self._load_categories()
        self.processed_abstracts = []
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.distance_matrix = None
        
    def _load_categories(self):
        """
        Carga las categorías y variables definidas en el proyecto
        
        Returns:
            dict: Diccionario con las categorías y sus variables
        """
        categories = {
            'Habilidades': ['Abstraction', 'Algorithm', 'Algorithmic thinking', 'Coding', 
                            'Collaboration', 'Cooperation', 'Creativity', 'Critical thinking', 
                            'Debug', 'Decomposition', 'Evaluation', 'Generalization', 'Logic', 
                            'Logical thinking', 'Modularity', 'Patterns recognition', 
                            'Problem solving', 'Programming'],
            'Conceptos Computacionales': ['Conditionals', 'Control structures', 'Directions', 
                                          'Events', 'Functions', 'Loops', 'Modular structure', 
                                          'Parallelism', 'Sequences', 'Software/hardware', 'Variables'],
            'Actitudes': ['Emotional', 'Engagement', 'Motivation', 'Perceptions', 'Persistence', 
                          'Self-efficacy', 'Self-perceived'],
            'Propiedades psicométricas': ['Classical Test Theory - CTT', 'Confirmatory Factor Analysis - CFA',
                                          'Exploratory Factor Analysis - EFA', 
                                          'Item Response Theory (IRT) - IRT', 'Reliability',
                                          'Structural Equation Model - SEM', 'Validity'],
            'Herramienta de evaluación': ['Beginners Computational Thinking test - BCTt',
                                          'Coding Attitudes Survey - ESCAS',
                                          'Collaborative Computing Observation Instrument',
                                          'Competent Computational Thinking test - cCTt',
                                          'Computational thinking skills test - CTST',
                                          'Computational concepts',
                                          'Computational Thinking Assessment for Chinese Elementary Students - CTA-CES',
                                          'Computational Thinking Challenge - CTC',
                                          'Computational Thinking Levels Scale - CTLS',
                                          'Computational Thinking Scale - CTS',
                                          'Computational Thinking Skill Levels Scale - CTS',
                                          'Computational Thinking Test - CTt',
                                          'Computational Thinking Test',
                                          'Computational Thinking Test for Elementary School Students',
                                          'Computational Thinking Test for Lower Primary - CTtLP',
                                          'Computational thinking-skill tasks on numbers and arithmetic',
                                          'Computerized Adaptive Programming Concepts Test - CAPCT',
                                          'CT Scale - CTS',
                                          'Elementary Student Coding Attitudes Survey - ESCAS',
                                          'General self-efficacy scale',
                                          'ICT competency test',
                                          'Instrument of computational identity'],
            'Diseño de investigación': ['No experimental', 'Experimental', 'Longitudinal research',
                                        'Mixed methods', 'Post-test', 'Pre-test', 'Quasi-experiments'],
            'Nivel de escolaridad': ['Upper elementary education - Upper elementary school',
                                     'Primary school - Primary education - Elementary school',
                                     'Early childhood education - Kindergarten - Preschool',
                                     'Secondary school - Secondary education',
                                     'High school - Higher education',
                                     'University - College'],
            'Medio': ['Block programming', 'Mobile application', 'Pair programming',
                      'Plugged activities', 'Programming', 'Robotics', 'Spreadsheet',
                      'STEM', 'Unplugged activities'],
            'Estrategia': ['Construct-by-self mind mapping', 'Construct-on-scaffold mind mapping',
                           'Design-based learning', 'Evidence-centred design approach',
                           'Gamification', 'Reverse engineering pedagogy',
                           'Technology-enhanced learning', 'Collaborative learning',
                           'Cooperative learning', 'Flipped classroom',
                           'Game-based learning', 'Inquiry-based learning',
                           'Personalized learning', 'Problem-based learning',
                           'Project-based learning', 'Universal design for learning'],
            'Herramienta': ['Alice', 'Arduino', 'Scratch', 'ScratchJr', 'Blockly Games',
                            'Code.org', 'Codecombat', 'CSUnplugged', 'Robot Turtles',
                            'Hello Ruby', 'Kodable', 'LightbotJr', 'KIBO robots',
                            'BEE BOT', 'CUBETTO', 'Minecraft', 'Agent Sheets',
                            'Mimo', 'Py-Learn', 'SpaceChem']
        }
        return categories
    
    def read_bibtex_file(self):
        """
        Lee el archivo BibTeX y extrae las entradas
        
        Returns:
            self: Para permitir encadenamiento de métodos
        """
        try:
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            
            with open(self.bibtex_file_path, 'r', encoding='utf-8') as bibtex_file:
                self.entries = bibtexparser.load(bibtex_file, parser=parser).entries
            
            print(f"Se han cargado {len(self.entries)} entradas del archivo BibTeX.")
            return self
        except Exception as e:
            print(f"Error al cargar el archivo BibTeX: {str(e)}")
            return self
    
    def extract_abstracts(self):
        """
        Extrae los abstracts de las entradas BibTeX
        Si se especificó sample_size, toma solo una muestra de los abstracts
        
        Returns:
            self: Para permitir encadenamiento de métodos
        """
        if not self.entries:
            print("No hay entradas BibTeX cargadas.")
            return self
        
        all_abstracts = []
        all_abstract_ids = []
        
        for entry in self.entries:
            if 'abstract' in entry and entry['abstract'].strip():
                all_abstracts.append(entry['abstract'])
                entry_id = entry.get('ID', entry.get('title', 'Unknown')[:30])
                all_abstract_ids.append(entry_id)
        
        if self.sample_size is not None:
            random.seed(self.random_seed)
            total_abstracts = len(all_abstracts)
            
            if isinstance(self.sample_size, float) and 0 < self.sample_size <= 1:
                sample_count = int(total_abstracts * self.sample_size)
            elif isinstance(self.sample_size, int) and self.sample_size > 0:
                sample_count = min(self.sample_size, total_abstracts)
            else:
                print("Tamaño de muestra inválido. Usando todos los abstracts.")
                sample_count = total_abstracts
            
            indices = random.sample(range(total_abstracts), sample_count)
            self.abstracts = [all_abstracts[i] for i in indices]
            self.abstract_ids = [all_abstract_ids[i] for i in indices]
            
            print(f"Se han extraído {len(self.abstracts)} abstracts de un total de {total_abstracts} (muestra del {(len(self.abstracts)/total_abstracts)*100:.1f}%).")
        else:
            self.abstracts = all_abstracts
            self.abstract_ids = all_abstract_ids
            print(f"Se han extraído {len(self.abstracts)} abstracts.")
        
        return self
    
    def preprocess_abstracts(self):
        """
        Preprocesa los abstracts (tokenización, eliminación de stopwords, lematización)
        
        Returns:
            self: Para permitir encadenamiento de métodos
        """
        if not self.abstracts:
            print("No hay abstracts para procesar.")
            return self
        
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        self.processed_abstracts = []
        
        for abstract in self.abstracts:
            text = abstract.lower()
            text = re.sub(r'\d+', '', text)
            text = text.translate(str.maketrans('', '', string.punctuation))
            tokens = word_tokenize(text)
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
            processed_text = ' '.join(tokens)
            self.processed_abstracts.append(processed_text)
        
        print(f"Se han preprocesado {len(self.processed_abstracts)} abstracts.")
        return self
    
    def calculate_tfidf(self):
        """
        Calcula la matriz TF-IDF para los abstracts procesados
        
        Returns:
            self: Para permitir encadenamiento de métodos
        """
        if not self.processed_abstracts:
            print("No hay abstracts procesados para calcular TF-IDF.")
            return self
        
        vectorizer = TfidfVectorizer()
        self.tfidf_matrix = vectorizer.fit_transform(self.processed_abstracts)
        
        print(f"Se ha calculado la matriz TF-IDF con forma {self.tfidf_matrix.shape}.")
        return self
    
    def calculate_similarity(self):
        """
        Calcula la matriz de similitud del coseno entre los abstracts
        
        Returns:
            self: Para permitir encadenamiento de métodos
        """
        if self.tfidf_matrix is None:
            print("No hay matriz TF-IDF calculada.")
            return self
        
        try:
            # Calculate cosine similarity
            self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
            # Ensure diagonal is exactly 1.0 to avoid numerical errors
            np.fill_diagonal(self.similarity_matrix, 1.0)
            # Convert to distance matrix
            self.distance_matrix = 1.0 - self.similarity_matrix
            # Ensure diagonal is exactly 0.0
            np.fill_diagonal(self.distance_matrix, 0.0)
            # Clip any negative values due to numerical errors
            self.distance_matrix = np.clip(self.distance_matrix, 0.0, None)
            
            print(f"Se ha calculado la matriz de similitud con forma {self.similarity_matrix.shape}.")
            return self
        except Exception as e:
            print(f"Error al calcular la matriz de similitud: {str(e)}")
            traceback.print_exc()
            return self
    
    def apply_hierarchical_clustering_1(self, method='ward'):
        """
        Implementa el primer algoritmo de clustering jerárquico usando scipy
        
        Args:
            method (str): Método de linkage ('ward', 'complete', 'average', 'single')
            
        Returns:
            linkage_matrix: Matriz de linkage resultante
        """
        if self.distance_matrix is None:
            print("No hay matriz de distancia calculada.")
            return None
        
        try:
            print("Convirtiendo matriz de distancia a formato condensado...")
            condensed_dist = squareform(self.distance_matrix)
            print(f"Aplicando clustering jerárquico con método {method}...")
            linkage_matrix = linkage(condensed_dist, method=method)
            print(f"Se ha aplicado clustering jerárquico usando el método {method}.")
            return linkage_matrix
        except Exception as e:
            print(f"Error en clustering jerárquico 1: {str(e)}")
            traceback.print_exc()
            return None
    
    def apply_hierarchical_clustering_2(self):
        """
        Implementa el segundo algoritmo de clustering jerárquico (AGNES - Agglomerative Nesting)
        
        Returns:
            linkage_matrix: Matriz de linkage resultante
        """
        if self.distance_matrix is None:
            print("No hay matriz de distancia calculada.")
            return None
        
        try:
            print("Iniciando algoritmo AGNES...")
            n = len(self.distance_matrix)
            
            if n > 1000:
                print("Conjunto de datos grande detectado. Usando implementación simplificada de AGNES...")
                condensed_dist = squareform(self.distance_matrix)
                Z = linkage(condensed_dist, method='average')
                print("Se ha aplicado clustering jerárquico AGNES (versión simplificada).")
                return Z
            
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
                                dist_sum += self.distance_matrix[idx1, idx2]
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
                condensed_dist = squareform(self.distance_matrix)
                Z = linkage(condensed_dist, method='average')
                print("Se ha aplicado clustering jerárquico AGNES (método alternativo).")
                return Z
            except Exception as e2:
                print(f"Error en método alternativo: {str(e2)}")
                return None
    
    def plot_dendrogram(self, linkage_matrix, method_name, max_d=None, color_threshold=None, truncate_mode='lastp', p=30):
        """
        Visualiza el dendrograma del clustering jerárquico
        
        Args:
            linkage_matrix: Matriz de linkage resultante del clustering
            method_name (str): Nombre del método para el título
            max_d (float, optional): Distancia máxima para línea horizontal
            color_threshold (float, optional): Umbral para colorear los clusters
            truncate_mode (str, optional): Modo de truncamiento ('lastp', 'level', None)
            p (int, optional): Número de hojas a mostrar si truncate_mode='lastp'
            
        Returns:
            self: Para permitir encadenamiento de métodos
        """
        if linkage_matrix is None:
            print(f"No se puede generar dendrograma para {method_name}: matriz de linkage no disponible.")
            return self
        
        try:
            plt.figure(figsize=(16, 10))
            plt.title(f'Dendrograma Jerárquico - Método {method_name}', fontsize=20)
            
            labels = None
            if len(self.abstract_ids) > 50:
                labels = None
            else:
                labels = self.abstract_ids
            
            dendrogram(
                linkage_matrix,
                labels=labels,
                orientation='top',
                leaf_rotation=90,
                leaf_font_size=8,
                color_threshold=color_threshold,
                truncate_mode=truncate_mode if len(self.abstract_ids) > 50 else None,
                p=p if len(self.abstract_ids) > 50 else None
            )
            
            if max_d:
                plt.axhline(y=max_d, c='k', ls='--', lw=1)
                plt.text(plt.xlim()[1], max_d, f'Distancia límite: {max_d:.2f}', 
                        va='center', ha='left', fontsize=12)
            
            plt.xlabel('Abstracts', fontsize=16)
            plt.ylabel('Distancia', fontsize=16)
            plt.tight_layout()

            plt.savefig(os.path.join(CLUSTERING_OUTPUT_DIR, f'dendrograma_{method_name.lower()}.png'), dpi=300, bbox_inches='tight')
            plt.close()
            return self
        except Exception as e:
            print(f"Error al generar dendrograma para {method_name}: {str(e)}")
            traceback.print_exc()
            return self
    
    def plot_similarity_heatmap(self, max_size=100):
        """
        Visualiza la matriz de similitud como un mapa de calor
        Para matrices grandes, muestra solo una submuestra
        
        Args:
            max_size (int): Tamaño máximo de la matriz a visualizar
            
        Returns:
            self: Para permitir encadenamiento de métodos
        """
        if self.similarity_matrix is None:
            print("No hay matriz de similitud calculada.")
            return self
        
        try:
            if self.similarity_matrix.shape[0] > max_size:
                random.seed(self.random_seed)
                indices = random.sample(range(self.similarity_matrix.shape[0]), max_size)
                sample_matrix = self.similarity_matrix[np.ix_(indices, indices)]
                sample_ids = [self.abstract_ids[i] for i in indices]
                
                print(f"Matriz muy grande. Mostrando submuestra de {max_size}x{max_size}.")
                plt.figure(figsize=(14, 12))
                sns.heatmap(sample_matrix, annot=False, cmap='viridis', 
                           xticklabels=sample_ids, yticklabels=sample_ids)
                plt.title('Mapa de Calor - Similitud entre Abstracts (Muestra)', fontsize=18)
            else:
                plt.figure(figsize=(14, 12))
                sns.heatmap(self.similarity_matrix, annot=False, cmap='viridis', 
                           xticklabels=self.abstract_ids, yticklabels=self.abstract_ids)
                plt.title('Mapa de Calor - Similitud entre Abstracts', fontsize=18)
            
            plt.xticks(rotation=90, fontsize=8)
            plt.yticks(rotation=0, fontsize=8)
            plt.tight_layout()

            plt.savefig(os.path.join(CLUSTERING_OUTPUT_DIR, 'mapa_calor_similitud.png'), dpi=300, bbox_inches='tight')
            plt.close()
            return self
        except Exception as e:
            print(f"Error al generar mapa de calor: {str(e)}")
            traceback.print_exc()
            return self
    
    def evaluate_clustering(self, Z1, Z2, n_clusters=5):
        """
        Evalúa la coherencia de los clusters con respecto a las categorías del proyecto
        
        Args:
            Z1: Matriz de linkage del primer algoritmo
            Z2: Matriz de linkage del segundo algoritmo
            n_clusters (int): Número de clusters a evaluar
            
        Returns:
            dict: Resultados de la evaluación
        """
        from scipy.cluster.hierarchy import fcluster
        
        if Z1 is None or Z2 is None:
            print("No se pueden evaluar clusters: falta al menos una matriz de linkage.")
            return {"error": "Matrices de linkage incompletas"}
        
        try:
            print(f"Calculando {n_clusters} clusters para cada algoritmo...")
            clusters1 = fcluster(Z1, n_clusters, criterion='maxclust')
            clusters2 = fcluster(Z2, n_clusters, criterion='maxclust')
            
            results = {}
            
            def analyze_categories_in_clusters(clusters):
                print("Analizando categorías en clusters...")
                cluster_categories = {}
                
                flat_categories = {}
                for cat, terms in self.categories.items():
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
                    cluster_abstracts = [self.abstracts[i] for i in cluster_indices]
                    
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
            self._visualize_category_distribution(results, 'algorithm1', 'Algoritmo 1')
            self._visualize_category_distribution(results, 'algorithm2', 'Algoritmo 2')
            
            coherence1 = self._calculate_coherence(results['algorithm1'])
            coherence2 = self._calculate_coherence(results['algorithm2'])
            
            results['coherence'] = {
                'algorithm1': coherence1,
                'algorithm2': coherence2,
                'best_algorithm': 'algorithm1' if coherence1 > coherence2 else 'algorithm2'
            }
            
            print(f"Coherencia del Algoritmo 1: {coherence1:.4f}")
            print(f"Coherencia del Algoritmo 2: {coherence2:.4f}")
            print(f"El mejor algoritmo es: {'Algoritmo 1' if coherence1 > coherence2 else 'Algoritmo 2'}")
            
            return results
        except Exception as e:
            print(f"Error en la evaluación de clusters: {str(e)}")
            traceback.print_exc()
            return {"error": str(e)}
    
    def _visualize_category_distribution(self, results, algorithm_key, algorithm_name):
        """
        Visualiza la distribución de categorías en los clusters
        
        Args:
            results: Resultados de la evaluación
            algorithm_key: Clave del algoritmo en los resultados
            algorithm_name: Nombre del algoritmo para el título
        """
        try:
            if algorithm_key not in results:
                print(f"No se encontraron datos para {algorithm_name}")
                return
                
            cluster_data = results[algorithm_key]
            categories = list(self.categories.keys())
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

            plt.savefig(os.path.join(CLUSTERING_OUTPUT_DIR, f'distribucion_categorias_{algorithm_key}.png'), dpi=300, bbox_inches='tight')
            plt.close()
        except Exception as e:
            print(f"Error al visualizar distribución de categorías para {algorithm_name}: {str(e)}")
            traceback.print_exc()
    
    def _calculate_coherence(self, cluster_data):
        """
        Calcula una medida de coherencia para los clusters
        
        Args:
            cluster_data: Datos de categorías por cluster
            
        Returns:
            float: Valor de coherencia
        """
        try:
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
            
            if coherence_scores:
                return np.mean(coherence_scores)
            return 0.0
        except Exception as e:
            print(f"Error al calcular coherencia: {str(e)}")
            traceback.print_exc()
            return 0.0

def main():
    """Main function to execute the hierarchical clustering pipeline."""
    # Define BibTeX file path
    if len(sys.argv) > 1:
        bibtex_file = sys.argv[1]
    else:
        bibtex_file = 'output/unified_cleaned.bib'  # Ruta relativa por defecto

    # Initialize the clustering class
    clusterer = HierarchicalClusteringAbstracts(bibtex_file, sample_size=None, random_seed=42)
    #bibtex_file = r'C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib'
    
    # Initialize the clustering class
    clusterer = HierarchicalClusteringAbstracts(bibtex_file, sample_size=None, random_seed=42)
    
    # Execute the pipeline
    try:
        # Read and process abstracts
        clusterer.read_bibtex_file()\
                 .extract_abstracts()\
                 .preprocess_abstracts()\
                 .calculate_tfidf()\
                 .calculate_similarity()
        
        # Apply clustering algorithms
        Z1 = clusterer.apply_hierarchical_clustering_1(method='ward')
        Z2 = clusterer.apply_hierarchical_clustering_2()
        
        # Plot dendrograms
        clusterer.plot_dendrogram(Z1, 'Ward', max_d=1.0)
        clusterer.plot_dendrogram(Z2, 'AGNES', max_d=1.0)
        
        # Plot similarity heatmap
        clusterer.plot_similarity_heatmap(max_size=50)
        
        # Evaluate clustering
        results = clusterer.evaluate_clustering(Z1, Z2, n_clusters=5)
        
        # Save cluster assignments to CSV
        if 'algorithm1' in results and 'algorithm2' in results:
            from scipy.cluster.hierarchy import fcluster
            clusters1 = fcluster(Z1, 5, criterion='maxclust')
            clusters2 = fcluster(Z2, 5, criterion='maxclust')
            
            data = {
                'Abstract_ID': clusterer.abstract_ids,
                'Cluster_Ward': clusters1,
                'Cluster_AGNES': clusters2
            }
            df = pd.DataFrame(data)
            df.to_csv(os.path.join(CLUSTERING_OUTPUT_DIR, 'cluster_assignments.csv'), index=False)
            print("Cluster assignments saved to 'cluster_assignments.csv'.")
        
    except Exception as e:
        print(f"Error en la ejecución del pipeline: {str(e)}")
        traceback.print_exc()

if __name__ == '__main__':
    try:
        import bibtexparser
    except ModuleNotFoundError:
        print("Error: 'bibtexparser' module not found. Please install it using 'pip install bibtexparser'.")
        exit(1)
    main()