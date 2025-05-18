import gradio as gr
import os
import shutil
import pandas as pd

OUTPUT_DIR = "output"
GRAPHICS_DIR = "graphics"

# Variable global para saber si el archivo fue cargado
archivo_cargado = {"status": False}

def save_uploaded_file(file_path):
    save_path = os.path.join(OUTPUT_DIR, "unified_cleaned.bib")
    shutil.copy(file_path, save_path)
    archivo_cargado["status"] = True
    return save_path

def validar_archivo():
    if not archivo_cargado["status"]:
        return False, "⚠️ Por favor, sube primero el archivo BibTeX unificado."
    return True, ""

def run_estadisticas():
    valido, msg = validar_archivo()
    if not valido:
        return None, None, None, None, None, gr.update(value=msg)
    ruta = os.path.join(OUTPUT_DIR, "unified_cleaned.bib")
    os.system(f"python processing/estatistics/ranking.py {ruta}")
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
        top15_journals,
        gr.update(value="✅ Análisis estadístico realizado.")
    )

def run_nube_palabras():
    valido, msg = validar_archivo()
    if not valido:
        return [], gr.update(value=msg)
    os.system("python processing/wordscloud/requerimiento3.py")
    req3_dir = os.path.join(GRAPHICS_DIR, "requerimiento3")
    images = []
    if os.path.exists(req3_dir):
        for fname in os.listdir(req3_dir):
            if fname.endswith(".png"):
                images.append(os.path.join(req3_dir, fname))
    return images, gr.update(value="✅ Nube de palabras generada.")

def run_clustering():
    valido, msg = validar_archivo()
    if not valido:
        return [], gr.update(value=msg)
    os.system("python processing/measure_similar/requerimiento5.py")
    clustering_dir = os.path.join(GRAPHICS_DIR, "clustering")
    images = []
    if os.path.exists(clustering_dir):
        for fname in os.listdir(clustering_dir):
            if fname.endswith(".png"):
                images.append(os.path.join(clustering_dir, fname))
    return images, gr.update(value="✅ Clustering realizado.")

with gr.Blocks() as demo:
    gr.Markdown("# Sistema de Análisis Bibliométrico y Computacional")
    gr.Markdown("Carga tu archivo BibTeX unificado y ejecuta los análisis disponibles.")

    with gr.Row():
        file_input = gr.File(label="Archivo BibTeX unificado (.bib)")
        upload_btn = gr.Button("Cargar archivo")
        upload_output = gr.Textbox(label="Estado de carga")

        def cargar_archivo(file):
            if file is None:
                return "⚠️ Debes seleccionar un archivo."
            save_uploaded_file(file)
            return "Archivo cargado correctamente."

        upload_btn.click(
            fn=cargar_archivo,
            inputs=file_input,
            outputs=upload_output
        )

    gr.Markdown("## Análisis disponibles")

    with gr.Row():
        estad_btn = gr.Button("Análisis Estadístico")
        nube_btn = gr.Button("Nube de Palabras")
        cluster_btn = gr.Button("Clustering")

    autores_df = gr.Dataframe(label="📌 Top 15 Primeros Autores")
    publicaciones_df = gr.Dataframe(label="📌 Publicaciones de los Top 15 Autores por Año")
    tipo_prod_df = gr.Dataframe(label="📌 Cantidad por Tipo de Producto")
    tipo_prod_anio_df = gr.Dataframe(label="📌 Conteo por Tipo de Producto y Año")
    journals_df = gr.Dataframe(label="📌 Top 15 Journals")
    estad_status = gr.Textbox(label="Estado análisis estadístico")

    estad_btn.click(
        fn=run_estadisticas,
        outputs=[autores_df, publicaciones_df, tipo_prod_df, tipo_prod_anio_df, journals_df, estad_status]
    )

    nube_output = gr.Gallery(label="Nube de Palabras y Co-ocurrencia")
    nube_status = gr.Textbox(label="Estado nube de palabras")
    nube_btn.click(fn=run_nube_palabras, outputs=[nube_output, nube_status])

    cluster_output = gr.Gallery(label="Resultados de Clustering")
    cluster_status = gr.Textbox(label="Estado clustering")
    cluster_btn.click(fn=run_clustering, outputs=[cluster_output, cluster_status])

demo.launch(share=True)