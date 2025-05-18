import re
from collections import Counter, defaultdict
import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import itertools
import bibtexparser
import sys

# --- CONFIGURACIÓN ---
output_folder = "graphics/requerimiento3"
os.makedirs(output_folder, exist_ok=True)

# --- CATEGORÍAS Y VARIABLES ---
categories = {
    'Skills': [
        'abstraction', 'algorithm', 'algorithmic thinking', 'coding', 'collaboration',
        'cooperation', 'creativity', 'critical thinking', 'debug', 'decomposition',
        'evaluation', 'generalization', 'logic', 'logical thinking', 'modularity',
        'patterns recognition', 'problem solving', 'programming'
    ],
    'Computational Concepts': [
        'conditionals', 'control structures', 'directions', 'events', 'functions',
        'loops', 'modular structure', 'parallelism', 'sequences', 'software', 'hardware', 'variables'
    ],
    'Attitudes': [
        'emotional engagement', 'motivation', 'perceptions', 'persistence',
        'self-efficacy', 'self-perceived'
    ],
    'Psychometric Properties': [
        'classical test theory', 'ctt', 'confirmatory factor analysis', 'cfa',
        'exploratory factor analysis', 'efa', 'item response theory', 'irt',
        'reliability', 'structural equation model', 'sem', 'validity'
    ],
    'Assessment Tools': [
        'beginners computational thinking test', 'bctt', 'coding attitudes survey', 'escas',
        'collaborative computing observation instrument', 'competent computational thinking test',
        'cctt', 'computational thinking skills test', 'ctst',
        'computational thinking assessment for chinese elementary students', 'cta-ces',
        'computational thinking challenge', 'ctc',
        'computational thinking levels scale', 'ctls',
        'computational thinking scale', 'cts',
        'computational thinking skill levels scale', 'computational thinking test',
        'computational thinking test for elementary school students',
        'computational thinking test for lower primary', 'cttlp',
        'computational thinking-skill tasks on numbers and arithmetic',
        'computerized adaptive programming concepts test', 'capct',
        'elementary student coding attitudes survey', 'general self-efficacy scale',
        'ict competency test', 'instrument of computational identity',
        'kbit fluid intelligence subtest', 'mastery of computational concepts test and an algorithmic test',
        'multidimensional 21st century skills scale', 'self-efficacy scale',
        'stem learning attitude scale', 'the computational thinking scale'
    ],
    'Research Design': [
        'non experimental', 'experimental', 'longitudinal research', 'mixed methods',
        'post-test', 'pre-test', 'quasi-experiments'
    ],
    'Education Level': [
        'upper elementary education', 'upper elementary school', 'primary school',
        'primary education', 'elementary school', 'early childhood education',
        'kindergarten', 'preschool', 'secondary school', 'secondary education',
        'high school', 'higher education', 'university', 'college'
    ],
    'Tools': [
        'alice', 'arduino', 'scratch', 'scratchjr', 'blockly games', 'code.org',
        'codecombat', 'csunplugged', 'robot turtles', 'hello ruby', 'kodable',
        'lightbotjr', 'kibo robots', 'bee bot', 'cubetto', 'minecraft',
        'agent sheets', 'mimo', 'py-learn', 'spacechem'
    ],
    'Other': [
        'block programming', 'mobile application', 'pair programming',
        'plugged activities', 'robotics', 'spreadsheet', 'stem',
        'unplugged activities'
    ],
    'Strategies': [
        'construct-by-self mind mapping', 'construct-on-scaffold mind mapping',
        'design-based learning', 'evidence-centred design approach', 'gamification',
        'reverse engineering pedagogy', 'technology-enhanced learning',
        'collaborative learning', 'cooperative learning', 'flipped classroom',
        'game-based learning', 'inquiry-based learning', 'personalized learning',
        'problem-based learning', 'project-based learning', 'universal design for learning'
    ]
}

# Sinónimos para unificación (todas las claves y valores en minúscula)
synonyms = {
    'functions': 'function',
    'debugging': 'debug',
    'self efficacy': 'self-efficacy',
    'program': 'programming',
    'programs': 'programming',
    'loops': 'loop',
    'software/hardware': 'software',
    'hardware/software': 'hardware',
    'coding attitudes survey - escas': 'coding attitudes survey',
    'computational thinking test for lower primary': 'computational thinking test for lower primary',
    'computational thinking test for lower primary - cttlp': 'computational thinking test for lower primary',
}

# --- FUNCIONES ---

def normalize_term(term):
    term = term.lower()
    return synonyms.get(term, term)

def preprocess_text(text):
    # Si el texto es NaN o no es una cadena, devolver cadena vacía
    if not isinstance(text, str) or pd.isna(text):
        return ""
    # Pasa todo a minúsculas
    text = text.lower()
    # Elimina caracteres especiales que no afectan palabras
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    # Reemplaza múltiples espacios por uno solo
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def count_frequencies(df, categories):
    freq_by_category = {cat: Counter() for cat in categories}
    total_counter = Counter()

    # Asegurarse de que la columna 'abstract' exista
    if 'abstract' not in df.columns:
        df['abstract'] = ""

    for abstract in df['abstract']:
        text = preprocess_text(abstract)

        # Contar ocurrencias para cada término por categoría
        for cat, terms in categories.items():
            for term in terms:
                norm_term = normalize_term(term)
                # Para términos compuestos (más de una palabra) usamos regex para contar ocurrencias exactas
                pattern = r'\b' + re.escape(norm_term) + r'\b'
                matches = re.findall(pattern, text)
                count = len(matches)
                if count > 0:
                    freq_by_category[cat][norm_term] += count
                    total_counter[norm_term] += count

    return freq_by_category, total_counter

def create_frequency_tables(freq_by_category):
    dfs = {}
    for cat, counter in freq_by_category.items():
        df_cat = pd.DataFrame(counter.items(), columns=['Variable', 'Frequency'])
        df_cat = df_cat.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
        dfs[cat] = df_cat
    return dfs

def generate_wordcloud(freq_counter, title, filename):
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_counter)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def build_cooccurrence_network(df, categories):
    # Preparar términos unificados para búsqueda en cada abstract
    all_terms = []
    for terms in categories.values():
        all_terms.extend([normalize_term(t) for t in terms])
    all_terms = list(set(all_terms))  # eliminar duplicados

    # Construir matriz de co-ocurrencia (usaremos diccionario de diccionarios)
    cooccurrence = defaultdict(lambda: defaultdict(int))

    # Asegurarse de que la columna 'abstract' exista
    if 'abstract' not in df.columns:
        df['abstract'] = ""

    for abstract in df['abstract']:
        text = preprocess_text(abstract)
        found_terms = set()
        for term in all_terms:
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, text):
                found_terms.add(term)
        # Actualizar co-ocurrencias
        for term1, term2 in itertools.combinations(sorted(found_terms), 2):
            cooccurrence[term1][term2] += 1
            cooccurrence[term2][term1] += 1

    # Crear grafo con NetworkX
    G = nx.Graph()
    for term1, edges in cooccurrence.items():
        for term2, weight in edges.items():
            if weight > 0:
                G.add_edge(term1, term2, weight=weight)
    return G

def plot_cooccurrence_network(G, filename, min_weight=2):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.3)
    edges = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] >= min_weight]
    weights = [G[u][v]['weight'] for u, v in edges]

    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=[w*0.5 for w in weights])
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title("Co-word Network (min weight = {})".format(min_weight))
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# --- EJECUCIÓN PRINCIPAL ---

def main(df):
    # Asegurarse de que la columna 'abstract' exista
    if 'abstract' not in df.columns:
        df['abstract'] = ""

    # Contar frecuencias
    freq_by_category, total_freq = count_frequencies(df, categories)

    # Crear tablas de frecuencia
    freq_tables = create_frequency_tables(freq_by_category)

    # Guardar tablas como Excel
    with pd.ExcelWriter(os.path.join(output_folder, "frequencies_by_category.xlsx")) as writer:
        for cat, df_cat in freq_tables.items():
            df_cat.to_excel(writer, sheet_name=cat[:31], index=False)  # Excel limita a 31 caracteres para sheets
        pd.DataFrame(total_freq.items(), columns=['Variable', 'Frequency']).sort_values(by='Frequency', ascending=False)\
            .to_excel(writer, sheet_name="Total", index=False)

    # Generar nubes de palabras por categoría y total
    for cat, counter in freq_by_category.items():
        if len(counter) > 0:
            generate_wordcloud(counter, f"Word Cloud - {cat}", os.path.join(output_folder, f"wordcloud_{cat}.png"))
    generate_wordcloud(total_freq, "Word Cloud - Total", os.path.join(output_folder, "wordcloud_total.png"))

    # Construir y graficar red de co-ocurrencias
    G = build_cooccurrence_network(df, categories)
    plot_cooccurrence_network(G, os.path.join(output_folder, "co_word_network.png"), min_weight=2)

    print(f"Proceso terminado. Resultados guardados en {output_folder}")

# --- EJEMPLO DE USO ---

if __name__ == "__main__":

    
    if len(sys.argv) > 1:
        path_file = sys.argv[1]
    else:
        path_file = "output/unified_cleaned.bib"

    #path_file = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib"
    
    # Validar si el archivo existe
    if os.path.exists(path_file):
        try:
            with open(path_file, encoding="utf-8") as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
            
            # Verifica si hay entradas en el archivo
            if bib_database.entries:
                df = pd.DataFrame(bib_database.entries)
                main(df)
            else:
                print("⚠️ El archivo BibTeX no contiene entradas.")
        except Exception as e:
            print(f"❌ Error al cargar el archivo BibTeX: {e}")
    else:
        print(f"❌ Archivo no encontrado en la ruta especificada: {path_file}")