"""
GUI – Pestaña: Módulo 1 - Cálculo de Raíces
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from modules.raices import biseccion, newton_raphson, secante
from gui.pdf_export import exportar_pdf

FONT_LABEL   = ("Segoe UI", 10)
FONT_TITLE   = ("Segoe UI", 11, "bold")
COLOR_ACCENT = "#1565C0"

# Estado compartido de la pestaña (se llena al ejecutar)
_estado = {"historial": [], "resultado_txt": "", "metodo": "", "fig": None}


def build_tab(parent):
    """Construye la pestaña completa de Cálculo de Raíces."""
    frame = ttk.Frame(parent)

    # ── Panel izquierdo ──────────────────────────────────────────
    panel_ctrl = ttk.LabelFrame(frame, text=" Parámetros ", padding=10)
    panel_ctrl.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)

    ttk.Label(panel_ctrl, text="Método:", font=FONT_TITLE).grid(row=0, column=0, sticky="w", pady=(0,4))
    metodo_var = tk.StringVar(value="Bisección")
    ttk.Combobox(panel_ctrl, textvariable=metodo_var,
                 values=["Bisección", "Newton-Raphson", "Secante"],
                 state="readonly", width=22).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,8))

    ttk.Label(panel_ctrl, text="f(x) =", font=FONT_LABEL).grid(row=2, column=0, sticky="w")
    entrada_f = ttk.Entry(panel_ctrl, width=24)
    entrada_f.insert(0, "x**3 - x - 2")
    entrada_f.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,6))

    ttk.Label(panel_ctrl, text="f'(x) = (solo Newton-Raphson)", font=FONT_LABEL).grid(row=4, column=0, columnspan=2, sticky="w")
    entrada_df = ttk.Entry(panel_ctrl, width=24)
    entrada_df.insert(0, "3*x**2 - 1")
    entrada_df.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0,6))

    pf = ttk.Frame(panel_ctrl)
    pf.grid(row=6, column=0, columnspan=2, sticky="ew")

    ttk.Label(pf, text="a / x0:",          font=FONT_LABEL).grid(row=0, column=0, sticky="w")
    entrada_a = ttk.Entry(pf, width=10);   entrada_a.insert(0,"1"); entrada_a.grid(row=0,column=1,padx=4,pady=2)
    ttk.Label(pf, text="b / x1:",          font=FONT_LABEL).grid(row=1, column=0, sticky="w")
    entrada_b = ttk.Entry(pf, width=10);   entrada_b.insert(0,"2"); entrada_b.grid(row=1,column=1,padx=4,pady=2)
    ttk.Label(pf, text="Tolerancia:",      font=FONT_LABEL).grid(row=2, column=0, sticky="w")
    entrada_tol = ttk.Entry(pf, width=10); entrada_tol.insert(0,"1e-6"); entrada_tol.grid(row=2,column=1,padx=4,pady=2)
    ttk.Label(pf, text="Máx. iteraciones:",font=FONT_LABEL).grid(row=3, column=0, sticky="w")
    entrada_iter = ttk.Entry(pf, width=10);entrada_iter.insert(0,"100"); entrada_iter.grid(row=3,column=1,padx=4,pady=2)

    btn_calcular = ttk.Button(panel_ctrl, text="▶  Calcular Raíz")
    btn_calcular.grid(row=7, column=0, columnspan=2, pady=(12,4), sticky="ew")

    btn_pdf = ttk.Button(panel_ctrl, text="🖨  Imprimir PDF")
    btn_pdf.grid(row=8, column=0, columnspan=2, pady=(0,8), sticky="ew")

    resultado_var = tk.StringVar(value="—")
    ttk.Label(panel_ctrl, text="Resultado:", font=FONT_TITLE).grid(row=9, column=0, sticky="w")
    ttk.Label(panel_ctrl, textvariable=resultado_var, font=("Courier",10),
              foreground=COLOR_ACCENT, wraplength=220).grid(row=10, column=0, columnspan=2, sticky="w")

    # ── Panel derecho ────────────────────────────────────────────
    panel_der = ttk.Frame(frame)
    panel_der.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=8)

    fig = Figure(figsize=(5.5, 3.8), dpi=96, facecolor="#FAFAFA")
    ax  = fig.add_subplot(111)
    ax.set_title("Gráfica de f(x)", fontsize=10)
    ax.set_xlabel("x"); ax.set_ylabel("f(x)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _estado["fig"] = fig

    canvas = FigureCanvasTkAgg(fig, master=panel_der)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    ttk.Label(panel_der, text="Historial de iteraciones", font=FONT_TITLE).pack(pady=(6,2))
    tabla_frame = ttk.Frame(panel_der)
    tabla_frame.pack(fill="both", expand=True, pady=(0,4))

    cols = ("Iter", "a / x0", "b / x1", "c / x_nuevo", "f(c)", "Error")
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=7)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=90, anchor="center")
    sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    # ── Lógica calcular ─────────────────────────────────────────
    def ejecutar():
        try:
            f  = lambda x: eval(entrada_f.get().strip(),  {"x":x,"np":np,**vars(np)})
            df = lambda x: eval(entrada_df.get().strip(), {"x":x,"np":np,**vars(np)})
            a   = float(entrada_a.get())
            b   = float(entrada_b.get())
            tol = float(entrada_tol.get())
            mit = int(entrada_iter.get())
            met = metodo_var.get()

            if met == "Bisección":
                res = biseccion(f, a, b, tol, mit)
            elif met == "Newton-Raphson":
                res = newton_raphson(f, df, a, tol, mit)
            else:
                res = secante(f, a, b, tol, mit)

            raiz  = res["raiz"]
            iters = res["iteraciones"]
            err   = res["error"]
            res_txt = f"Raíz ≈ {raiz:.10f}  |  Iteraciones: {iters}  |  Error: {err:.2e}"
            resultado_var.set(f"Raíz ≈ {raiz:.10f}\nIteraciones: {iters}\nError: {err:.2e}")

            # Llenar Treeview y guardar filas para PDF
            for row in tree.get_children():
                tree.delete(row)
            filas_pdf = []
            for paso in res["historial"]:
                col0 = paso.get("iter","")
                col1 = round(paso.get("a", paso.get("x",  paso.get("x0",""))),8)
                col2_raw = paso.get("b", paso.get("x1", None))
                col2 = round(col2_raw, 8) if col2_raw is not None else "—"
                col3 = round(paso.get("c", paso.get("x_nuevo", paso.get("x2",""))),8)
                col4 = f"{paso.get('f(c)', paso.get('f(x)', paso.get('f(x2)',''))):+.4e}"
                col5 = f"{paso.get('error',''):.2e}"
                vals = [col0, col1, col2, col3, col4, col5]
                tree.insert("", "end", values=vals)
                filas_pdf.append([str(v) for v in vals])

            _estado["historial"]    = filas_pdf
            _estado["resultado_txt"] = res_txt
            _estado["metodo"]       = met

            # Graficar
            ax.clear()
            x_min = min(a,b) - abs(b-a)*0.5
            x_max = max(a,b) + abs(b-a)*0.5
            xs = np.linspace(x_min, x_max, 400)
            ys = np.array([f(xi) for xi in xs])
            ax.plot(xs, ys, color=COLOR_ACCENT, lw=2, label="f(x)")
            ax.axhline(0, color="black", lw=0.8, ls="--")
            ax.axvline(raiz, color="red", lw=1.2, ls="--", label=f"Raíz ≈ {raiz:.6f}")
            ax.scatter([raiz],[f(raiz)], color="red", zorder=5)
            ax.set_title(f"Método: {met}", fontsize=10)
            ax.set_xlabel("x"); ax.set_ylabel("f(x)")
            ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
            fig.tight_layout()
            canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── Lógica PDF ───────────────────────────────────────────────
    def imprimir_pdf():
        if not _estado["historial"]:
            messagebox.showwarning("Sin datos", "Primero ejecuta un cálculo.", parent=frame)
            return
        exportar_pdf(
            titulo_modulo = "Módulo 1 – Cálculo de Raíces",
            subtitulo     = f"Método: {_estado['metodo']}  |  {_estado['resultado_txt']}",
            fig_fuente    = fig,
            encabezados   = list(cols),
            filas         = _estado["historial"],
            resultado_texto = _estado["resultado_txt"],
            parent_widget = frame,
        )

    btn_calcular.configure(command=ejecutar)
    btn_pdf.configure(command=imprimir_pdf)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)
    frame.rowconfigure(0, weight=1)
    return frame
