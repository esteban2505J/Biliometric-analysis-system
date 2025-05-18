import bibtexparser
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ruta del archivo

import sys
if len(sys.argv) > 1:
    path_file = sys.argv[1]
else:
    path_file = "output/unified_cleaned.bib"

#path_file = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib"
#output_folder = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\graphics\ranking"
output_folder = "graphics/ranking"
os.makedirs(output_folder, exist_ok=True)

# Función para graficar y guardar ranking horizontal
def graficar_ranking(serie, titulo, nombre_archivo, xlabel="Cantidad", ylabel="Elemento"):
    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    sns.barplot(x=serie.values, y=serie.index, palette="viridis")
    plt.title(titulo, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, nombre_archivo), dpi=300)
    plt.close()

# Cargar el archivo BibTeX
with open(path_file, encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

entries = bib_database.entries
df = pd.DataFrame(entries)

# Campos útiles
df['primer_autor'] = df['author'].apply(lambda x: x.split(' and ')[0] if pd.notna(x) else "Desconocido")
df['tipo'] = df['ENTRYTYPE']
df['year'] = df['year'].astype(str)

# 1. Top 15 Primeros Autores (por cantidad)
top_autores = df['primer_autor'].value_counts().head(15)
tabla_autores = top_autores.reset_index()
tabla_autores.columns = ['Autor', 'Cantidad']
print("\n📌 Top 15 Primeros Autores:\n")
print(tabulate(tabla_autores, headers='keys', tablefmt='fancy_grid'))
graficar_ranking(top_autores, "Top 15 Primeros Autores", "top_autores.png", "Cantidad de Publicaciones", "Autor")

# Evolución por año para los Top 15 autores
top_15_autores = top_autores.index.tolist()
df_top_autores = df[df['primer_autor'].isin(top_15_autores)]
autores_anio = df_top_autores.groupby(['primer_autor', 'year']).size().unstack(fill_value=0)

print("\n📌 Publicaciones de los Top 15 Autores por Año:\n")
print(autores_anio)
autores_anio.to_csv(os.path.join(output_folder, "top_15_autores_por_anio.csv"))

plt.figure(figsize=(12,8))
autores_anio.T.plot(kind='line', marker='o')
plt.title("Evolución publicaciones Top 15 Autores por Año")
plt.xlabel("Año")
plt.ylabel("Cantidad de Publicaciones")
plt.legend(title="Autor", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "top_15_autores_por_anio.png"), dpi=300)
plt.close()

# 2. Conteo por Tipo de Producto
tipo_producto = df['tipo'].value_counts()
tabla_tipo = tipo_producto.reset_index()
tabla_tipo.columns = ['Tipo de Producto', 'Cantidad']
print("\n📌 Cantidad por Tipo de Producto:\n")
print(tabulate(tabla_tipo, headers='keys', tablefmt='fancy_grid'))
graficar_ranking(tipo_producto, "Conteo por Tipo de Producto", "tipos_producto.png", "Cantidad", "Tipo de Producto")

# Conteo por Tipo y Año
tipo_anio = df.groupby(['tipo', 'year']).size().unstack(fill_value=0)
print("\n📌 Conteo por Tipo de Producto y Año:\n")
print(tipo_anio)
tipo_anio.to_csv(os.path.join(output_folder, "conteo_tipo_anio.csv"))

plt.figure(figsize=(12,8))
tipo_anio.T.plot(kind='bar', stacked=True, colormap='viridis')
plt.title("Publicaciones por Tipo de Producto y Año")
plt.xlabel("Año")
plt.ylabel("Cantidad de Publicaciones")
plt.legend(title="Tipo de Producto", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "publicaciones_tipo_producto_anio.png"), dpi=300)
plt.close()

# 3. Top 15 Journals
if 'journal' in df.columns:
    top_journals = df['journal'].value_counts().head(15)
    tabla_journals = top_journals.reset_index()
    tabla_journals.columns = ['Journal', 'Cantidad']
    print("\n📌 Top 15 Journals:\n")
    print(tabulate(tabla_journals, headers='keys', tablefmt='fancy_grid'))
    graficar_ranking(top_journals, "Top 15 Journals", "top_journals.png", "Cantidad", "Journal")

    # Evolución por año para top 15 journals
    top_15_journals = top_journals.index.tolist()
    df_top_journals = df[df['journal'].isin(top_15_journals)]
    journals_anio = df_top_journals.groupby(['journal', 'year']).size().unstack(fill_value=0)
    journals_anio.to_csv(os.path.join(output_folder, "top_15_journals_por_anio.csv"))

    plt.figure(figsize=(12,8))
    journals_anio.T.plot(kind='line', marker='o')
    plt.title("Evolución publicaciones Top 15 Journals por Año")
    plt.xlabel("Año")
    plt.ylabel("Cantidad de Publicaciones")
    plt.legend(title="Journal", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "top_15_journals_por_anio.png"), dpi=300)
    plt.close()
else:
    print("\n⚠️ No se encontró columna 'journal' en el archivo BibTeX.")

# 4. Top 15 Publishers
if 'publisher' in df.columns:
    top_publishers = df['publisher'].value_counts().head(15)
    tabla_publishers = top_publishers.reset_index()
    tabla_publishers.columns = ['Publisher', 'Cantidad']
    print("\n📌 Top 15 Publishers:\n")
    print(tabulate(tabla_publishers, headers='keys', tablefmt='fancy_grid'))
    graficar_ranking(top_publishers, "Top 15 Publishers", "top_publishers.png", "Cantidad", "Publisher")

    # Evolución por año para top 15 publishers
    top_15_publishers = top_publishers.index.tolist()
    df_top_publishers = df[df['publisher'].isin(top_15_publishers)]
    publishers_anio = df_top_publishers.groupby(['publisher', 'year']).size().unstack(fill_value=0)
    publishers_anio.to_csv(os.path.join(output_folder, "top_15_publishers_por_anio.csv"))

    plt.figure(figsize=(12,8))
    publishers_anio.T.plot(kind='line', marker='o')
    plt.title("Evolución publicaciones Top 15 Publishers por Año")
    plt.xlabel("Año")
    plt.ylabel("Cantidad de Publicaciones")
    plt.legend(title="Publisher", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "top_15_publishers_por_anio.png"), dpi=300)
    plt.close()
else:
    print("\n⚠️ No se encontró columna 'publisher' en el archivo BibTeX.")

tabla_autores.to_csv(os.path.join(output_folder, "top15_autores.csv"), index=False)
autores_anio.to_csv(os.path.join(output_folder, "publicaciones_top15_autores_por_anio.csv"))
tabla_tipo.to_csv(os.path.join(output_folder, "cantidad_tipo_producto.csv"), index=False)
tipo_anio.to_csv(os.path.join(output_folder, "conteo_tipo_producto_anio.csv"))
tabla_journals.to_csv(os.path.join(output_folder, "top15_journals.csv"), index=False)