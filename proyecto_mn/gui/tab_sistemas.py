"""
GUI – Pestaña: Módulo 3 - Sistemas de Ecuaciones Lineales
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.sistemas import gauss_seidel, factorizacion_lu
from gui.pdf_export import exportar_pdf

FONT_LABEL   = ("Segoe UI", 10)
FONT_TITLE   = ("Segoe UI", 11, "bold")
FONT_MONO    = ("Courier New", 9)
COLOR_ACCENT = "#1565C0"

_estado = {"filas": [], "encabezados": [], "resultado_txt": "", "metodo": ""}


def build_tab(parent):
    frame = ttk.Frame(parent)

    panel_ctrl = ttk.LabelFrame(frame, text=" Configuración del Sistema ", padding=10)
    panel_ctrl.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)

    ttk.Label(panel_ctrl, text="Método:", font=FONT_TITLE).grid(row=0, column=0, sticky="w", pady=(0,2))
    metodo_var = tk.StringVar(value="Gauss-Seidel")
    ttk.Combobox(panel_ctrl, textvariable=metodo_var,
                 values=["Gauss-Seidel","Factorización LU"],
                 state="readonly", width=22).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,8))

    ttk.Label(panel_ctrl, text="Matriz A (una fila por línea,\nelementos separados por coma):", font=FONT_LABEL).grid(row=2, column=0, columnspan=2, sticky="w", pady=(6,2))
    entrada_A = tk.Text(panel_ctrl, height=5, width=28, font=FONT_MONO)
    entrada_A.insert("1.0","10, -1, 2\n-1, 11, -1\n2, -1, 10")
    entrada_A.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,6))

    ttk.Label(panel_ctrl, text="Vector b (separado por coma):", font=FONT_LABEL).grid(row=4, column=0, columnspan=2, sticky="w")
    entrada_b = ttk.Entry(panel_ctrl, width=28); entrada_b.insert(0,"6, 25, -11")
    entrada_b.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0,6))

    ttk.Label(panel_ctrl, text="Tolerancia (Gauss-Seidel):", font=FONT_LABEL).grid(row=6, column=0, columnspan=2, sticky="w")
    entrada_tol = ttk.Entry(panel_ctrl, width=14); entrada_tol.insert(0,"1e-6")
    entrada_tol.grid(row=7, column=0, columnspan=2, sticky="w", pady=(0,4))

    ttk.Label(panel_ctrl, text="Máx. iteraciones:", font=FONT_LABEL).grid(row=8, column=0, columnspan=2, sticky="w")
    entrada_iter = ttk.Entry(panel_ctrl, width=14); entrada_iter.insert(0,"100")
    entrada_iter.grid(row=9, column=0, columnspan=2, sticky="w", pady=(0,8))

    btn_calc = ttk.Button(panel_ctrl, text="▶  Resolver Sistema")
    btn_calc.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0,4))

    btn_pdf = ttk.Button(panel_ctrl, text="🖨  Imprimir PDF")
    btn_pdf.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(0,8))

    resultado_var = tk.StringVar(value="—")
    ttk.Label(panel_ctrl, text="Solución x:", font=FONT_TITLE).grid(row=12, column=0, columnspan=2, sticky="w", pady=(4,2))
    ttk.Label(panel_ctrl, textvariable=resultado_var, font=FONT_MONO,
              foreground=COLOR_ACCENT, wraplength=220, justify="left").grid(row=13, column=0, columnspan=2, sticky="w")

    # Panel derecho
    panel_der = ttk.Frame(frame)
    panel_der.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=8)

    fig = Figure(figsize=(5.5, 3.2), dpi=96, facecolor="#FAFAFA")
    ax  = fig.add_subplot(111)
    ax.set_title("Convergencia", fontsize=10); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=panel_der)
    canvas.get_tk_widget().pack(fill="both", expand=False)

    ttk.Label(panel_der, text="Matrices L y U (Factorización LU)", font=FONT_TITLE).pack(pady=(6,2))
    txt_lu = tk.Text(panel_der, height=10, font=("Courier New",8), state="disabled", bg="#F0F0F0")
    txt_lu.pack(fill="both", expand=True, padx=4, pady=4)

    def ejecutar():
        try:
            lineas = [l.strip() for l in entrada_A.get("1.0","end").strip().split("\n") if l.strip()]
            A = np.array([[float(v.strip()) for v in l.split(",")] for l in lineas])
            b = np.array([float(v.strip()) for v in entrada_b.get().split(",")])
            if A.shape[0] != A.shape[1]: raise ValueError("A debe ser cuadrada.")
            if len(b) != A.shape[0]:     raise ValueError("b debe tener misma dimensión que A.")

            met = metodo_var.get()
            txt_lu.config(state="normal"); txt_lu.delete("1.0","end")
            ax.clear()

            if met == "Gauss-Seidel":
                tol = float(entrada_tol.get()); mit = int(entrada_iter.get())
                res = gauss_seidel(A, b, tol=tol, max_iter=mit)
                x   = res["solucion"]
                sol_txt = "  |  ".join([f"x{i+1}={xi:.6f}" for i,xi in enumerate(x)])
                resultado_var.set("\n".join([f"  x{i+1} = {xi:.8f}" for i,xi in enumerate(x)])
                                  + f"\n\nIter: {res['iteraciones']}  Error: {res['error']:.2e}")
                _estado["resultado_txt"] = sol_txt

                filas_pdf = [[str(p["iter"])] + [f"{v:.6f}" for v in p["x"]] + [f"{p['error']:.2e}"]
                             for p in res["historial"]]
                n = A.shape[0]
                encab = ["Iter"] + [f"x{i+1}" for i in range(n)] + ["Error ‖∆x‖"]
                _estado["filas"] = filas_pdf; _estado["encabezados"] = encab

                errores = [p["error"] for p in res["historial"]]
                iters   = [p["iter"]  for p in res["historial"]]
                ax.semilogy(iters, errores, color=COLOR_ACCENT, marker="o", ms=3, lw=1.5, label="Error")
                ax.axhline(tol, color="red", ls="--", lw=1, label=f"Tol={tol}")
                ax.set_title("Convergencia – Gauss-Seidel", fontsize=10)
                ax.set_xlabel("Iteración"); ax.set_ylabel("Error (log)")
                ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
                txt_lu.insert("end","(La descomposición LU no aplica en Gauss-Seidel)")

            else:
                res  = factorizacion_lu(A, b)
                x    = res["solucion"]; L = res["L"]; U = res["U"]
                sol_txt = "  |  ".join([f"x{i+1}={xi:.6f}" for i,xi in enumerate(x)])
                resultado_var.set("\n".join([f"  x{i+1} = {xi:.8f}" for i,xi in enumerate(x)])
                                  + f"\n\nResiduo ‖Ax-b‖: {res['residuo']:.2e}")
                _estado["resultado_txt"] = sol_txt

                n = A.shape[0]
                filas_pdf = []
                for i in range(n):
                    filas_pdf.append([f"fila {i+1}"] + [f"{L[i,j]:.5f}" for j in range(n)]
                                     + ["||"] + [f"{U[i,j]:.5f}" for j in range(n)])
                encab = [""] + [f"L{i+1}" for i in range(n)] + [""] + [f"U{i+1}" for i in range(n)]
                _estado["filas"] = filas_pdf; _estado["encabezados"] = encab

                txt_lu.insert("end","── Matriz L ──\n")
                for fila in L: txt_lu.insert("end","  "+"  ".join(f"{v:9.5f}" for v in fila)+"\n")
                txt_lu.insert("end","\n── Matriz U ──\n")
                for fila in U: txt_lu.insert("end","  "+"  ".join(f"{v:9.5f}" for v in fila)+"\n")

                im = ax.imshow(np.hstack([L, np.full((n,1),np.nan), U]), cmap="coolwarm", aspect="auto")
                ax.set_title("Matrices L | U", fontsize=10)
                ax.set_xticks([]); ax.set_yticks(range(n))
                ax.set_yticklabels([f"fila {i+1}" for i in range(n)])
                fig.colorbar(im, ax=ax, fraction=0.04)

            _estado["metodo"] = met
            txt_lu.config(state="disabled")
            fig.tight_layout(); canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def imprimir_pdf():
        if not _estado["filas"]:
            messagebox.showwarning("Sin datos","Primero resuelve el sistema.", parent=frame)
            return
        exportar_pdf(
            titulo_modulo = "Módulo 3 – Sistemas de Ecuaciones Lineales",
            subtitulo     = f"Método: {_estado['metodo']}  |  {_estado['resultado_txt']}",
            fig_fuente    = fig,
            encabezados   = _estado["encabezados"],
            filas         = _estado["filas"],
            resultado_texto = _estado["resultado_txt"],
            parent_widget = frame,
        )

    btn_calc.configure(command=ejecutar)
    btn_pdf.configure(command=imprimir_pdf)
    frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=3); frame.rowconfigure(0, weight=1)
    return frame
