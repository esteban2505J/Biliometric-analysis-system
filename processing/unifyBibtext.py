import bibtexparser
import os



def load_bibtex_files(folder_paths):
    """Carga todos los archivos BibTeX de las carpetas especificadas."""
    entries = []
    for folder in folder_paths:
        for file in os.listdir(folder):
            if file.endswith(".bib"):
                with open(os.path.join(folder, file), encoding="utf-8") as bibfile:
                    bib_database = bibtexparser.load(bibfile)
                    entries.extend(bib_database.entries)
    return entries


def standardize_entries(entries):
    """Estandariza los campos de los registros BibTeX."""
    required_fields = {
        "article": ["title", "author", "journal", "volume", "number", "pages", "year", "doi", "url", "keywords", "abstract"],
        "inproceedings": ["title", "author", "booktitle", "pages", "year", "doi", "keywords"]
    }
    
    for entry in entries:
        entry_type = entry.get("ENTRYTYPE", "article").lower()
        
        # Definir los campos requeridos según el tipo
        fields = required_fields.get(entry_type, required_fields["article"])
        
        # Completar campos faltantes con valores vacíos
        for field in fields:
            if field not in entry:
                entry[field] = ""
    
    return entries


def save_bibtex_file(entries, output_file):
    """Guarda las entradas en un solo archivo BibTeX."""
    bib_database = bibtexparser.bibdatabase.BibDatabase()
    bib_database.entries = entries
    
    with open(output_file, "w", encoding="utf-8") as bibfile:
        bibtexparser.dump(bib_database, bibfile)
    
    print(f"BibTeX unificado guardado en: {output_file}")
    

if __name__ == "__main__":
    folder_paths = [
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\science",
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\sage",
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\IEE"
]
    output_file = "unified.bib"
    all_entries = load_bibtex_files(folder_paths)
    standardized_entries = standardize_entries(all_entries)
    save_bibtex_file(standardized_entries, output_file)