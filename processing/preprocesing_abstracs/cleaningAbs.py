import re
import bibtexparser

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string


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
    

if __name__ == "__main__":
    abstracts_cleaned = main()
    print(abstracts_cleaned)
    
    
        
   
    
    
            
    