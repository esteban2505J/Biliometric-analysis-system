# clustering/preprocessor.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

# Ensure NLTK resources are downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess_abstracts(abstracts):
    """
    Preprocess abstracts: lowercase, remove numbers/punctuation, tokenize, remove stopwords, lemmatize.
    
    Args:
        abstracts (list): List of abstract strings
    
    Returns:
        list: Preprocessed abstracts
    """
    if not abstracts:
        print("No hay abstracts para procesar.")
        return []
    
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    processed_abstracts = []
    
    for abstract in abstracts:
        text = abstract.lower()
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        processed_text = ' '.join(tokens)
        processed_abstracts.append(processed_text)
    
    print(f"Se han preprocesado {len(processed_abstracts)} abstracts.")
    return processed_abstracts