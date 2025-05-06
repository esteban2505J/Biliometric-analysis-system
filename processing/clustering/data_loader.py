# clustering/data_loader.py
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import random

def load_bibtex(file_path, sample_size=None, random_seed=42):
    """
    Load BibTeX file and extract abstracts.
    
    Args:
        file_path (str): Path to BibTeX file
        sample_size (int or float): Number or proportion of abstracts to sample
        random_seed (int): Seed for reproducibility
    
    Returns:
        tuple: (abstracts, abstract_ids)
    """
    try:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        with open(file_path, 'r', encoding='utf-8') as bibtex_file:
            entries = bibtexparser.load(bibtex_file, parser=parser).entries
        print(f"Se han cargado {len(entries)} entradas del archivo BibTeX.")
        
        all_abstracts = []
        all_abstract_ids = []
        for entry in entries:
            if 'abstract' in entry and entry['abstract'].strip():
                all_abstracts.append(entry['abstract'])
                entry_id = entry.get('ID', entry.get('title', 'Unknown')[:30])
                all_abstract_ids.append(entry_id)
        
        if not all_abstracts:
            print("No hay abstracts válidos en el archivo BibTeX.")
            return [], []
        
        if sample_size is not None:
            random.seed(random_seed)
            total_abstracts = len(all_abstracts)
            if isinstance(sample_size, float) and 0 < sample_size <= 1:
                sample_count = int(total_abstracts * sample_size)
            elif isinstance(sample_size, int) and sample_size > 0:
                sample_count = min(sample_size, total_abstracts)
            else:
                print("Tamaño de muestra inválido. Usando todos los abstracts.")
                sample_count = total_abstracts
            
            indices = random.sample(range(total_abstracts), sample_count)
            abstracts = [all_abstracts[i] for i in indices]
            abstract_ids = [all_abstract_ids[i] for i in indices]
            print(f"Se han extraído {len(abstracts)} abstracts de un total de {total_abstracts} "
                  f"(muestra del {(len(abstracts)/total_abstracts)*100:.1f}%).")
        else:
            abstracts = all_abstracts
            abstract_ids = all_abstract_ids
            print(f"Se han extraído {len(abstracts)} abstracts.")
        
        return abstracts, abstract_ids
    except Exception as e:
        print(f"Error al cargar el archivo BibTeX: {str(e)}")
        return [], []