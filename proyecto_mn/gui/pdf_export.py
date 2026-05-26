"""
Utilidad de exportación a PDF.
Genera un PDF con la gráfica activa y la tabla de iteraciones de cada módulo.
Solo usa matplotlib (ya requerido por el proyecto).
"""
import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend sin ventana para el PDF
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

# ── Colores corporativos ─────────────────────────────────────────
AZUL       = "#1565C0"
AZUL_CLARO = "#E3F2FD"
GRIS       = "#546E7A"
NEGRO      = "#212121"


def _encabezado(fig, titulo_modulo: str, subtitulo: str = ""):
    """Dibuja el encabezado institucional en la figura PDF."""
    fig.text(0.5, 0.97,
             "Universidad Mariano Gálvez",
             ha="center", va="top",
             fontsize=13, fontweight="bold", color=AZUL)
    fig.text(0.5, 0.945,
             "Facultad de Ingeniería en Sistemas  |  Métodos Numéricos – Python  (021)",
             ha="center", va="top",
             fontsize=8, color=GRIS)
    fig.text(0.5, 0.925,
             titulo_modulo,
             ha="center", va="top",
             fontsize=11, fontweight="bold", color=NEGRO)
    if subtitulo:
        fig.text(0.5, 0.905,
                 subtitulo,
                 ha="center", va="top",
                 fontsize=9, color=GRIS)

    fecha = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    fig.text(0.98, 0.005, f"Generado: {fecha}",
             ha="right", fontsize=7, color=GRIS)


def _dibujar_tabla(ax, encabezados, filas, titulo="Tabla de Iteraciones"):
    """
    Renderiza una tabla de datos en un Axes de matplotlib.
    Devuelve el Axes con la tabla ya dibujada.
    """
    ax.axis("off")
    ax.set_title(titulo, fontsize=9, fontweight="bold",
                 color=AZUL, pad=6, loc="left")

    if not filas:
        ax.text(0.5, 0.5, "Sin datos de iteraciones",
                ha="center", va="center", fontsize=9, color=GRIS,
                transform=ax.transAxes)
        return ax

    # Limitar a 40 filas para que quepa bien en la hoja
    filas_vis = filas[:40]
    if len(filas) > 40:
        filas_vis.append(["..." for _ in encabezados])

    tabla = ax.table(
        cellText=filas_vis,
        colLabels=encabezados,
        loc="center",
        cellLoc="center",
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(7.5)
    tabla.scale(1, 1.35)

    # Estilo encabezado
    n_cols = len(encabezados)
    for j in range(n_cols):
        cell = tabla[0, j]
        cell.set_facecolor(AZUL)
        cell.set_text_props(color="white", fontweight="bold")
        cell.set_edgecolor("white")

    # Filas alternadas
    for i, _ in enumerate(filas_vis, start=1):
        color = AZUL_CLARO if i % 2 == 0 else "white"
        for j in range(n_cols):
            cell = tabla[i, j]
            cell.set_facecolor(color)
            cell.set_edgecolor("#CFD8DC")

    return ax


def exportar_pdf(
    titulo_modulo: str,
    subtitulo: str,
    fig_fuente,          # matplotlib Figure con la gráfica original
    encabezados: list,   # columnas de la tabla
    filas: list,         # filas de la tabla  [[val, val, ...], ...]
    resultado_texto: str = "",
    parent_widget=None,
):
    """
    Abre un diálogo "Guardar como" y exporta la gráfica + tabla a un PDF.

    Parámetros:
        titulo_modulo   -- ej. "Módulo 1 – Cálculo de Raíces"
        subtitulo       -- ej. "Método: Bisección  |  Raíz ≈ 1.52137971"
        fig_fuente      -- Figure de matplotlib que se copiará al PDF
        encabezados     -- lista de strings con los nombres de columnas
        filas           -- lista de listas con los datos de la tabla
        resultado_texto -- texto de resumen opcional
        parent_widget   -- widget Tk para centrar el diálogo
    """
    ruta = filedialog.asksaveasfilename(
        parent=parent_widget,
        title="Guardar PDF",
        defaultextension=".pdf",
        filetypes=[("Archivo PDF", "*.pdf"), ("Todos", "*.*")],
        initialfile=f"{titulo_modulo.replace(' ', '_').replace('–','')}.pdf",
    )
    if not ruta:
        return  # Usuario canceló

    try:
        with PdfPages(ruta) as pdf:

            # ── Página 1: Gráfica ────────────────────────────────
            fig1 = plt.figure(figsize=(11, 8.5))  # Carta horizontal
            _encabezado(fig1, titulo_modulo, subtitulo)

            # Copiar la gráfica original redibujándola en el PDF
            # Tomamos la imagen renderizada del canvas de la app
            fig_fuente.canvas.draw()
            buf = fig_fuente.canvas.buffer_rgba()
            import numpy as _np
            img = _np.asarray(buf)

            ax_img = fig1.add_axes([0.05, 0.10, 0.90, 0.78])
            ax_img.imshow(img)
            ax_img.axis("off")

            if resultado_texto:
                fig1.text(0.05, 0.07, resultado_texto,
                          fontsize=8, color=NEGRO,
                          fontfamily="monospace",
                          verticalalignment="top")

            pdf.savefig(fig1, bbox_inches="tight")
            plt.close(fig1)

            # ── Página 2: Tabla ──────────────────────────────────
            if filas:
                fig2 = plt.figure(figsize=(11, 8.5))
                _encabezado(fig2, titulo_modulo,
                             "Tabla de iteraciones / resultados")
                ax_tab = fig2.add_axes([0.03, 0.06, 0.94, 0.82])
                _dibujar_tabla(ax_tab, encabezados, filas,
                                titulo="Historial de iteraciones")
                pdf.savefig(fig2, bbox_inches="tight")
                plt.close(fig2)

            # Metadatos del PDF
            info = pdf.infodict()
            info["Title"]   = titulo_modulo
            info["Author"]  = "Métodos Numéricos – UMG"
            info["Subject"] = subtitulo
            info["Keywords"] = "métodos numéricos, Python, UMG"

        messagebox.showinfo(
            "PDF generado",
            f"Archivo guardado correctamente:\n{ruta}",
            parent=parent_widget,
        )

    except Exception as e:
        messagebox.showerror("Error al exportar PDF", str(e), parent=parent_widget)
