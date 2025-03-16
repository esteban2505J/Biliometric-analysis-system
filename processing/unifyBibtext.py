import bibtexparser
import os

# Directorios con archivos .bib
folder_paths = [
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\science",
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\sage",
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\IEE"
]

# Archivos de salida
output_cleaned = "unified_cleaned.bib"
output_duplicates = "duplicates.bib"

# Campos requeridos por tipo de entrada
required_fields = {
    "article": ["title", "author", "journal", "year", "doi"],
    "inproceedings": ["title", "author", "booktitle", "year", "doi"],
    "book": ["title", "author", "publisher", "year", "isbn"],
}

def load_bibtex_files(folder_paths):
    """Carga todos los archivos BibTeX de las carpetas especificadas."""
    entries = []
    for folder in folder_paths:
        if not os.path.exists(folder):
            print(f"⚠️ La carpeta {folder} no existe, omitiendo...")
            continue
        for file in os.listdir(folder):
            if file.endswith(".bib"):
                with open(os.path.join(folder, file), encoding="utf-8") as bibfile:
                    bib_database = bibtexparser.load(bibfile)
                    entries.extend(bib_database.entries)
    return entries

def get_identifier(entry):
    """Extrae un identificador único basado en DOI o título."""
    return entry.get("doi", entry.get("title", "")).strip().lower()

def detect_duplicates(entries):
    """Detecta y separa duplicados basados en DOI o título."""
    seen = {}
    duplicates = []

    for entry in entries:
        identifier = get_identifier(entry)
        if identifier:
            if identifier in seen:
                duplicates.append(entry)
            else:
                seen[identifier] = entry

    # Filtrar los únicos (sin duplicados)
    unique_entries = list(seen.values())
    return unique_entries, duplicates

def clean_entries(entries):
    """Mantiene solo los campos esenciales según el tipo de entrada."""
    cleaned = []
    for entry in entries:
        entry_type = entry.get("ENTRYTYPE", "").lower()
        required = required_fields.get(entry_type, ["title", "author", "year"])  # Si no está definido, usa estos por defecto
        cleaned_entry = {key: entry[key] for key in required if key in entry}
        cleaned_entry["ENTRYTYPE"] = entry_type  # Asegurar que se mantiene el tipo
        cleaned_entry["ID"] = entry.get("ID", "")  # Mantener el identificador
        cleaned.append(cleaned_entry)
    return cleaned

def save_bibtex_file(entries, output_file):
    """Guarda las entradas en un archivo BibTeX."""
    if entries:
        bib_database = bibtexparser.bibdatabase.BibDatabase()
        bib_database.entries = entries
        with open(output_file, "w", encoding="utf-8") as bibfile:
            bibtexparser.dump(bib_database, bibfile)
        print(f"✅ Guardado en: {output_file}")
    else:
        print(f"⚠️ No hay entradas para guardar en {output_file}")

if __name__ == "__main__":
    all_entries = load_bibtex_files(folder_paths)
    
    # Detectar duplicados
    unique_entries, duplicate_entries = detect_duplicates(all_entries)

    # Limpiar entradas pero manteniendo los campos clave según el tipo de entrada
    cleaned_entries = clean_entries(unique_entries)
    cleaned_duplicates = clean_entries(duplicate_entries)

    # Guardar resultados
    save_bibtex_file(cleaned_entries, output_cleaned)
    save_bibtex_file(cleaned_duplicates, output_duplicates)
