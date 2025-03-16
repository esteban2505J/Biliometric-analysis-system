import os
import re

# Directorios donde están los archivos
folder_paths = [
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\science",
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\sage",
    r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\downloads\IEE"
]

def extract_variables_from_file(file_path):
    """Extrae las variables de un archivo .bib"""
    variables = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r'\s*(\w+)\s*=\s*', line)
                if match:
                    variables.add(match.group(1))  # Guarda el nombre de la variable
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
    return variables

def find_common_variables(folder_paths):
    """Encuentra las variables comunes en todos los archivos"""
    common_variables = None  # Inicialmente no hay un conjunto base
    
    for folder in folder_paths:
        if not os.path.exists(folder):
            print(f"⚠️ La carpeta {folder} no existe, omitiendo...")
            continue
        
        for file in os.listdir(folder):
            if file.endswith(".bib"):  # Verifica si es un archivo .bib
                file_path = os.path.join(folder, file)
                file_variables = extract_variables_from_file(file_path)
                
                if common_variables is None:
                    common_variables = file_variables
                else:
                    common_variables.intersection_update(file_variables)  # Mantiene solo las comunes
    
    return common_variables

# Ejecutar el script
common_vars = find_common_variables(folder_paths)
print("📌 Variables comunes en todos los archivos:", common_vars)
