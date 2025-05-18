import gradio as gr
import os
import shutil

OUTPUT_DIR = "output"
GRAPHICS_DIR = "graphics"


def save_uploaded_file(file_path):
    # file_path es una ruta a un archivo temporal
    save_path = os.path.join(OUTPUT_DIR, "unified_cleaned.bib")
    shutil.copy(file_path, save_path)
    return save_path

import pandas as pd

def run_estadisticas():
    # Ejecuta el análisis estadístico
    ruta = os.path.join(OUTPUT_DIR, "unified_cleaned.bib")
    os.system(f"python processing/estatistics/ranking.py {ruta}")

    # Lee los resultados generados por ranking.py
    top15_autores = pd.read_csv("graphics/ranking/top15_autores.csv")
    publicaciones_top15 = pd.read_csv("graphics/ranking/publicaciones_top15_autores_por_anio.csv", index_col=0)
    cantidad_tipo_producto = pd.read_csv("graphics/ranking/cantidad_tipo_producto.csv")
    conteo_tipo_producto_anio = pd.read_csv("graphics/ranking/conteo_tipo_producto_anio.csv", index_col=0)
    top15_journals = pd.read_csv("graphics/ranking/top15_journals.csv")

    return (
        top15_autores,
        publicaciones_top15,
        cantidad_tipo_producto,
        conteo_tipo_producto_anio,
        top15_journals
    )


def run_nube_palabras():
    # Ejecuta el análisis de nube de palabras
    os.system("python processing/wordscloud/requerimiento3.py")
    # Devuelve las imágenes generadas
    req3_dir = os.path.join(GRAPHICS_DIR, "requerimiento3")
    images = []
    if os.path.exists(req3_dir):
        for fname in os.listdir(req3_dir):
            if fname.endswith(".png"):
                images.append(os.path.join(req3_dir, fname))
    return images

def run_clustering():
    # Ejecuta el análisis de clustering
    os.system("python processing/measure_similar/requerimiento5.py")
    # Devuelve las imágenes generadas
    images = []
    for fname in os.listdir(GRAPHICS_DIR):
        if "dendrograma" in fname and fname.endswith(".png"):
            images.append(os.path.join(GRAPHICS_DIR, fname))
    if os.path.exists("cluster_assignments.csv"):
        images.append("cluster_assignments.csv")
    return images

with gr.Blocks() as demo:
    gr.Markdown("# Sistema de Análisis Bibliométrico y Computacional")
    gr.Markdown("Carga tu archivo BibTeX unificado y ejecuta los análisis disponibles.")

    with gr.Row():
        file_input = gr.File(label="Archivo BibTeX unificado (.bib)")
        upload_btn = gr.Button("Cargar archivo")
        upload_output = gr.Textbox(label="Estado de carga")

        upload_btn.click(
        fn=lambda f: "Archivo cargado correctamente." if save_uploaded_file(f) else "Error al cargar.",
        inputs=file_input,
        outputs=upload_output
    )

    gr.Markdown("## Análisis disponibles")

    with gr.Row():
        estad_btn = gr.Button("Análisis Estadístico")
        nube_btn = gr.Button("Nube de Palabras")
        cluster_btn = gr.Button("Clustering")

    # Salidas para las tablas
    autores_df = gr.Dataframe(label="📌 Top 15 Primeros Autores")
    publicaciones_df = gr.Dataframe(label="📌 Publicaciones de los Top 15 Autores por Año")
    tipo_prod_df = gr.Dataframe(label="📌 Cantidad por Tipo de Producto")
    tipo_prod_anio_df = gr.Dataframe(label="📌 Conteo por Tipo de Producto y Año")
    journals_df = gr.Dataframe(label="📌 Top 15 Journals")


    estad_btn.click(
        fn=run_estadisticas,
        outputs=[autores_df, publicaciones_df, tipo_prod_df, tipo_prod_anio_df, journals_df]
    )

    nube_output = gr.Gallery(label="Nube de Palabras y Co-ocurrencia")
    cluster_output = gr.Gallery(label="Resultados de Clustering")

    nube_btn.click(fn=run_nube_palabras, outputs=nube_output)
    cluster_btn.click(fn=run_clustering, outputs=cluster_output)

demo.launch(share=True)