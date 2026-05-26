"""
Aplicación Principal – Métodos Numéricos con Python
Universidad Mariano Gálvez
Facultad de Ingeniería en Sistemas de Información y Ciencias de la Computación
Proyecto Final – Código: 021  |  Métodos Numéricos – Python
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import tab_raices, tab_interpolacion, tab_sistemas, tab_derivacion, tab_edo


# ─────────────────────────────────────────────────────────────────
#  Paleta de colores y estilos
# ─────────────────────────────────────────────────────────────────
BG_HEADER   = "#1565C0"
BG_APP      = "#ECEFF1"
FG_HEADER   = "#FFFFFF"
FONT_TITULO = ("Segoe UI", 14, "bold")
FONT_SUB    = ("Segoe UI", 9)


class AplicacionMetodosNumericos:
    """Clase principal de la aplicación de Métodos Numéricos."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configurar_ventana()
        self._construir_header()
        self._construir_notebook()
        self._construir_statusbar()

    # ── Configuración de la ventana ──────────────────────────────
    def _configurar_ventana(self):
        self.root.title("Métodos Numéricos – Proyecto Final")
        self.root.geometry("1050x720")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG_APP)
        self.root.resizable(True, True)

        # Estilo ttk global
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame",       background=BG_APP)
        style.configure("TLabel",       background=BG_APP, font=("Segoe UI", 10))
        style.configure("TLabelFrame",  background=BG_APP)
        style.configure("TLabelFrame.Label", font=("Segoe UI", 10, "bold"),
                         foreground=BG_HEADER)
        style.configure("TButton",      font=("Segoe UI", 10, "bold"),
                         foreground="white", background=BG_HEADER,
                         padding=6)
        style.map("TButton",
                   background=[("active", "#0D47A1")],
                   foreground=[("active", "white")])
        style.configure("TNotebook",    background=BG_APP)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"),
                         padding=[14, 6])
        style.map("TNotebook.Tab",
                   background=[("selected", BG_HEADER), ("!selected", "#90CAF9")],
                   foreground=[("selected", "white"), ("!selected", "#0D47A1")])
        style.configure("TEntry",       font=("Segoe UI", 10))
        style.configure("TCombobox",    font=("Segoe UI", 10))
        style.configure("Treeview",     font=("Courier New", 9), rowheight=22)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                         foreground=BG_HEADER)

    # ── Encabezado de la app ─────────────────────────────────────
    def _construir_header(self):
        header = tk.Frame(self.root, bg=BG_HEADER, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header,
                  text="⚙  Métodos Numéricos con Python",
                  bg=BG_HEADER, fg=FG_HEADER,
                  font=FONT_TITULO).pack(side="left", padx=20, pady=14)

        tk.Label(header,
                  text="Universidad Mariano Gálvez  |  Facultad de Ingeniería en Sistemas",
                  bg=BG_HEADER, fg="#BBDEFB",
                  font=FONT_SUB).pack(side="right", padx=20, pady=14)

    # ── Notebook con las pestañas ────────────────────────────────
    def _construir_notebook(self):
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=6, pady=(6, 2))

        modulos = [
            ("🔍  Raíces",                    tab_raices),
            ("📈  Interpolación",             tab_interpolacion),
            ("🔢  Sistemas Lineales",         tab_sistemas),
            ("∂  Deriv. / Integración",       tab_derivacion),
            ("📉  Ecuaciones Diferenciales",  tab_edo),
        ]

        for titulo, modulo in modulos:
            tab = modulo.build_tab(nb)
            nb.add(tab, text=f"  {titulo}  ")

    # ── Barra de estado ──────────────────────────────────────────
    def _construir_statusbar(self):
        barra = tk.Frame(self.root, bg="#CFD8DC", height=24)
        barra.pack(fill="x", side="bottom")

        tk.Label(barra,
                  text="  Proyecto Final  |  Métodos Numéricos – Python  |  UMG 2024",
                  bg="#CFD8DC", fg="#37474F",
                  font=("Segoe UI", 8)).pack(side="left", padx=8)

        import numpy as np
        ver_txt = f"Python {sys.version.split()[0]}  |  NumPy {np.__version__}"
        tk.Label(barra, text=ver_txt, bg="#CFD8DC", fg="#546E7A",
                  font=("Segoe UI", 8)).pack(side="right", padx=8)


# ─────────────────────────────────────────────────────────────────
#  Punto de entrada
# ─────────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    app  = AplicacionMetodosNumericos(root)
    root.mainloop()


if __name__ == "__main__":
    main()
