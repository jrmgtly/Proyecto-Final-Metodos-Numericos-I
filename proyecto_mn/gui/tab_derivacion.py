"""
GUI – Pestaña: Módulo 4 - Derivación e Integración Numérica
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.derivacion_integracion import tabla_derivadas, trapecio, simpson_13, simpson_38
from gui.pdf_export import exportar_pdf

FONT_LABEL   = ("Segoe UI", 10)
FONT_TITLE   = ("Segoe UI", 11, "bold")
COLOR_ACCENT = "#1565C0"
COLOR_RED    = "#C62828"

_estado = {"filas": [], "encabezados": [], "resultado_txt": "", "op": ""}


def build_tab(parent):
    frame = ttk.Frame(parent)

    panel_ctrl = ttk.LabelFrame(frame, text=" Parámetros ", padding=10)
    panel_ctrl.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)

    ttk.Label(panel_ctrl, text="Operación:", font=FONT_TITLE).grid(row=0, column=0, sticky="w", pady=(0,2))
    op_var = tk.StringVar(value="Integración")
    ttk.Combobox(panel_ctrl, textvariable=op_var,
                 values=["Derivación","Integración"], state="readonly",
                 width=22).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,8))

    ttk.Label(panel_ctrl, text="f(x) =", font=FONT_LABEL).grid(row=2, column=0, sticky="w")
    entrada_f = ttk.Entry(panel_ctrl, width=24); entrada_f.insert(0,"np.sin(x)")
    entrada_f.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,6))

    ttk.Label(panel_ctrl, text="Punto x (derivación):", font=FONT_LABEL).grid(row=4, column=0, columnspan=2, sticky="w")
    entrada_xd = ttk.Entry(panel_ctrl, width=10); entrada_xd.insert(0,"1.0")
    entrada_xd.grid(row=5, column=0, sticky="w", pady=(0,6))
    ttk.Label(panel_ctrl, text="h:", font=FONT_LABEL).grid(row=5, column=1, sticky="w")
    entrada_h = ttk.Entry(panel_ctrl, width=8); entrada_h.insert(0,"1e-5")
    entrada_h.grid(row=5, column=1, sticky="e", pady=(0,6))

    ttk.Label(panel_ctrl, text="Límite inferior a:", font=FONT_LABEL).grid(row=6, column=0, sticky="w")
    entrada_a = ttk.Entry(panel_ctrl, width=10); entrada_a.insert(0,"0")
    entrada_a.grid(row=6, column=1, sticky="w", padx=4, pady=2)
    ttk.Label(panel_ctrl, text="Límite superior b:", font=FONT_LABEL).grid(row=7, column=0, sticky="w")
    entrada_b = ttk.Entry(panel_ctrl, width=10); entrada_b.insert(0,"3.14159265")
    entrada_b.grid(row=7, column=1, sticky="w", padx=4, pady=2)
    ttk.Label(panel_ctrl, text="Subintervalos n:", font=FONT_LABEL).grid(row=8, column=0, columnspan=2, sticky="w", pady=(4,0))
    entrada_n = ttk.Entry(panel_ctrl, width=10); entrada_n.insert(0,"100")
    entrada_n.grid(row=9, column=0, sticky="w", pady=(0,8))

    btn_calc = ttk.Button(panel_ctrl, text="▶  Calcular")
    btn_calc.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0,4))

    btn_pdf = ttk.Button(panel_ctrl, text="🖨  Imprimir PDF")
    btn_pdf.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(0,8))

    resultado_var = tk.StringVar(value="—")
    ttk.Label(panel_ctrl, text="Resultados:", font=FONT_TITLE).grid(row=12, column=0, columnspan=2, sticky="w", pady=(4,2))
    ttk.Label(panel_ctrl, textvariable=resultado_var, font=("Courier",9),
              foreground=COLOR_ACCENT, wraplength=220, justify="left").grid(row=13, column=0, columnspan=2, sticky="w")

    panel_der = ttk.Frame(frame)
    panel_der.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=8)

    fig = Figure(figsize=(5.8, 4.8), dpi=96, facecolor="#FAFAFA")
    ax  = fig.add_subplot(111)
    ax.set_title("Visualización", fontsize=10); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=panel_der)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def ejecutar():
        try:
            f  = lambda x: eval(entrada_f.get().strip(), {"x":x,"np":np,**vars(np)})
            ax.clear(); op = op_var.get()

            if op == "Derivación":
                xd = float(entrada_xd.get()); h = float(entrada_h.get())
                res = tabla_derivadas(f, xd, h)
                texto = (f"  Adelante : {res['adelante']:.10f}\n"
                         f"  Atrás    : {res['atras']:.10f}\n"
                         f"  Central  : {res['central']:.10f}\n"
                         f"  Segunda  : {res['segunda']:.10f}\n  h={h}, x={xd}")
                resultado_var.set(texto)
                _estado["filas"] = [
                    ["Adelante",  f"{res['adelante']:.10f}"],
                    ["Atrás",     f"{res['atras']:.10f}"],
                    ["Central",   f"{res['central']:.10f}"],
                    ["2ª deriv.", f"{res['segunda']:.10f}"],
                ]
                _estado["encabezados"] = ["Método", "f'(x)"]
                _estado["resultado_txt"] = texto.replace("\n","  |  ")
                _estado["op"] = f"Derivación  x={xd}  h={h}"

                xs = np.linspace(xd-2, xd+2, 400)
                ys = np.array([f(xi) for xi in xs])
                ax.plot(xs, ys, color=COLOR_ACCENT, lw=2, label="f(x)")
                pendiente = res["central"]
                tang_x = np.linspace(xd-0.8, xd+0.8, 50)
                tang_y = f(xd) + pendiente*(tang_x-xd)
                ax.plot(tang_x, tang_y, color=COLOR_RED, ls="--", lw=1.5,
                        label=f"Tangente  f'({xd})≈{pendiente:.6f}")
                ax.scatter([xd],[f(xd)], color=COLOR_RED, zorder=5, s=60)
                ax.set_title(f"Derivada de f(x) en x={xd}", fontsize=10)
                ax.legend(fontsize=8)

            else:
                a = float(entrada_a.get()); b = float(entrada_b.get()); n = int(entrada_n.get())
                r_trap = trapecio(f, a, b, n)
                r_s13  = simpson_13(f, a, b, n)
                r_s38  = simpson_38(f, a, b, n)
                texto  = (f"  Trapecio    (n={n}): {r_trap['resultado']:.10f}\n"
                          f"  Simpson 1/3 (n={n}): {r_s13['resultado']:.10f}\n"
                          f"  Simpson 3/8 (n={n}): {r_s38['resultado']:.10f}")
                resultado_var.set(texto)
                _estado["filas"] = [
                    ["Trapecio",    str(n), f"{r_trap['resultado']:.10f}"],
                    ["Simpson 1/3", str(n), f"{r_s13['resultado']:.10f}"],
                    ["Simpson 3/8", str(n), f"{r_s38['resultado']:.10f}"],
                ]
                _estado["encabezados"] = ["Método","n","Resultado"]
                _estado["resultado_txt"] = texto.replace("\n","  |  ")
                _estado["op"] = f"Integración  [{a}, {b}]  n={n}"

                xs = np.linspace(a, b, 400)
                ys = np.array([f(xi) for xi in xs])
                ax.plot(xs, ys, color=COLOR_ACCENT, lw=2, label="f(x)")
                ax.fill_between(xs, ys, alpha=0.25, color=COLOR_ACCENT,
                                label=f"Área ≈ {r_s13['resultado']:.6f}")
                ax.axhline(0, color="black", lw=0.8)
                n_vis = min(n, 20); h_vis = (b-a)/n_vis
                for i in range(n_vis):
                    xi = a+i*h_vis; xi1 = xi+h_vis
                    ax.plot([xi,xi,xi1,xi1],[0,f(xi),f(xi1),0], color=COLOR_RED, lw=0.6, alpha=0.5)
                ax.set_title(f"Integración  [{a},{b}]  n={n}", fontsize=10)
                ax.legend(fontsize=8)

            ax.set_xlabel("x"); ax.set_ylabel("f(x)"); ax.grid(True, alpha=0.3)
            fig.tight_layout(); canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def imprimir_pdf():
        if not _estado["filas"]:
            messagebox.showwarning("Sin datos","Primero ejecuta un cálculo.", parent=frame)
            return
        exportar_pdf(
            titulo_modulo = "Módulo 4 – Derivación e Integración Numérica",
            subtitulo     = _estado["op"],
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
