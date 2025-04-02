import re

def extract_data(contenido_bibtex):
    # Extraer años, títulos y DOIs del contenido BibTeX
    años = list(map(int, re.findall(r'year\s*=\s*\{(\d{4})\}', contenido_bibtex)))
    titulos = re.findall(r'title\s*=\s*\{(.*?)\}', contenido_bibtex)
    dois = re.findall(r'doi\s*=\s*\{(.*?)\}', contenido_bibtex)
    abstracts = re.findall(r'abstract\s*=\s*\{(.*?)\}', contenido_bibtex, re.DOTALL)
    
    return años,titulos,dois,abstracts