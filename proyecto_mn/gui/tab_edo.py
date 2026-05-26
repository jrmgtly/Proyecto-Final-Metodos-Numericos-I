"""
GUI – Pestaña: Módulo 5 - Ecuaciones Diferenciales Ordinarias
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.ecuaciones_diferenciales import euler, runge_kutta_4
from gui.pdf_export import exportar_pdf

FONT_LABEL   = ("Segoe UI", 10)
FONT_TITLE   = ("Segoe UI", 11, "bold")
COLOR_EULER  = "#C62828"
COLOR_RK4    = "#1565C0"
COLOR_EXACTO = "#2E7D32"

_estado = {"filas": [], "resultado_txt": "", "descripcion": ""}


def build_tab(parent):
    frame = ttk.Frame(parent)

    panel_ctrl = ttk.LabelFrame(frame, text=" Parámetros de la EDO ", padding=10)
    panel_ctrl.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)

    ttk.Label(panel_ctrl, text="Métodos a mostrar:", font=FONT_TITLE).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,2))
    check_euler = tk.BooleanVar(value=True)
    check_rk4   = tk.BooleanVar(value=True)
    ttk.Checkbutton(panel_ctrl, text="Euler",        variable=check_euler).grid(row=1, column=0, sticky="w")
    ttk.Checkbutton(panel_ctrl, text="Runge-Kutta 4",variable=check_rk4).grid(row=1,  column=1, sticky="w")

    ttk.Label(panel_ctrl, text="dy/dt = f(t, y):", font=FONT_TITLE).grid(row=2, column=0, columnspan=2, sticky="w", pady=(10,2))
    entrada_f = ttk.Entry(panel_ctrl, width=26); entrada_f.insert(0,"-2 * y + np.sin(t)")
    entrada_f.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,6))

    ttk.Label(panel_ctrl, text="Solución exacta y(t) (opcional):", font=FONT_LABEL).grid(row=4, column=0, columnspan=2, sticky="w")
    entrada_exacta = ttk.Entry(panel_ctrl, width=26)
    entrada_exacta.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0,6))

    pf = ttk.Frame(panel_ctrl); pf.grid(row=6, column=0, columnspan=2, sticky="ew")
    ttk.Label(pf, text="t₀:", font=FONT_LABEL).grid(row=0, column=0, sticky="w")
    entrada_t0 = ttk.Entry(pf, width=8); entrada_t0.insert(0,"0"); entrada_t0.grid(row=0,column=1,padx=4,pady=2)
    ttk.Label(pf, text="y₀:", font=FONT_LABEL).grid(row=1, column=0, sticky="w")
    entrada_y0 = ttk.Entry(pf, width=8); entrada_y0.insert(0,"0"); entrada_y0.grid(row=1,column=1,padx=4,pady=2)
    ttk.Label(pf, text="tf:", font=FONT_LABEL).grid(row=2, column=0, sticky="w")
    entrada_tf = ttk.Entry(pf, width=8); entrada_tf.insert(0,"10"); entrada_tf.grid(row=2,column=1,padx=4,pady=2)
    ttk.Label(pf, text="h (paso):", font=FONT_LABEL).grid(row=3, column=0, sticky="w")
    entrada_h  = ttk.Entry(pf, width=8); entrada_h.insert(0,"0.1"); entrada_h.grid(row=3,column=1,padx=4,pady=2)

    btn_calc = ttk.Button(panel_ctrl, text="▶  Resolver EDO")
    btn_calc.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10,4))

    btn_pdf = ttk.Button(panel_ctrl, text="🖨  Imprimir PDF")
    btn_pdf.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0,8))

    resultado_var = tk.StringVar(value="—")
    ttk.Label(panel_ctrl, text="Resumen:", font=FONT_TITLE).grid(row=9, column=0, columnspan=2, sticky="w")
    ttk.Label(panel_ctrl, textvariable=resultado_var, font=("Courier",8),
              foreground=COLOR_RK4, wraplength=220, justify="left").grid(row=10, column=0, columnspan=2, sticky="w")

    panel_der = ttk.Frame(frame)
    panel_der.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=8)

    fig = Figure(figsize=(5.8, 4.8), dpi=96, facecolor="#FAFAFA")
    ax  = fig.add_subplot(111)
    ax.set_title("Solución de la EDO", fontsize=10); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=panel_der)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    ttk.Label(panel_der, text="Tabla de valores (primeras 50 filas)", font=FONT_TITLE).pack(pady=(6,2))
    tabla_frame = ttk.Frame(panel_der); tabla_frame.pack(fill="both", expand=True)
    cols = ("t","Euler","RK4","Error Euler","Error RK4")
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
    for col in cols:
        tree.heading(col, text=col); tree.column(col, width=95, anchor="center")
    sb = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    def ejecutar():
        try:
            expr = entrada_f.get().strip()
            f    = lambda t,y: eval(expr, {"t":t,"y":y,"np":np,**vars(np)})
            t0 = float(entrada_t0.get()); y0 = float(entrada_y0.get())
            tf = float(entrada_tf.get()); h  = float(entrada_h.get())

            expr_ex    = entrada_exacta.get().strip()
            sol_exacta = (lambda t: eval(expr_ex, {"t":t,"np":np,**vars(np)})) if expr_ex else None

            res_e   = euler(f, t0, y0, tf, h)         if check_euler.get() else None
            res_rk4 = runge_kutta_4(f, t0, y0, tf, h) if check_rk4.get()   else None

            ax.clear()
            t_ref = (res_e or res_rk4)["t"]
            if sol_exacta:
                y_ex = np.array([sol_exacta(ti) for ti in t_ref])
                ax.plot(t_ref, y_ex, color=COLOR_EXACTO, lw=2, ls="--", label="Exacta", zorder=3)
            if res_e:   ax.plot(res_e["t"],   res_e["y"],   color=COLOR_EULER, lw=1.5, label="Euler", alpha=0.85)
            if res_rk4: ax.plot(res_rk4["t"], res_rk4["y"], color=COLOR_RK4,   lw=2,   label="RK4")
            ax.set_title(f"dy/dt = {expr}  |  h={h}", fontsize=9)
            ax.set_xlabel("t"); ax.set_ylabel("y(t)")
            ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
            fig.tight_layout(); canvas.draw()

            # Llenar tabla
            for row in tree.get_children(): tree.delete(row)
            filas_pdf = []
            y_e  = res_e["y"]   if res_e   else [None]*len(t_ref)
            y_rk = res_rk4["y"] if res_rk4 else [None]*len(t_ref)
            for i in range(min(len(t_ref), 50)):
                ti   = f"{t_ref[i]:.4f}"
                ei   = f"{y_e[i]:.6f}"  if res_e   else "—"
                rki  = f"{y_rk[i]:.6f}" if res_rk4 else "—"
                if sol_exacta:
                    ex = sol_exacta(t_ref[i])
                    err_e  = f"{abs(y_e[i]  - ex):.2e}" if res_e   else "—"
                    err_rk = f"{abs(y_rk[i] - ex):.2e}" if res_rk4 else "—"
                else:
                    err_e = err_rk = "—"
                tree.insert("", "end", values=(ti,ei,rki,err_e,err_rk))
                filas_pdf.append([ti, ei, rki, err_e, err_rk])

            txt = ""
            if res_e:   txt += f"Euler:  {res_e['pasos']} pasos, y(tf)={res_e['y'][-1]:.8f}\n"
            if res_rk4: txt += f"RK4:    {res_rk4['pasos']} pasos, y(tf)={res_rk4['y'][-1]:.8f}\n"
            if sol_exacta: txt += f"Exacto: y({tf})={sol_exacta(tf):.8f}"
            resultado_var.set(txt or "—")

            _estado["filas"]        = filas_pdf
            _estado["resultado_txt"]= txt.replace("\n","  |  ")
            _estado["descripcion"]  = f"dy/dt = {expr}  t∈[{t0},{tf}]  h={h}"

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def imprimir_pdf():
        if not _estado["filas"]:
            messagebox.showwarning("Sin datos","Primero resuelve la EDO.", parent=frame)
            return
        exportar_pdf(
            titulo_modulo = "Módulo 5 – Ecuaciones Diferenciales Ordinarias",
            subtitulo     = _estado["descripcion"],
            fig_fuente    = fig,
            encabezados   = list(cols),
            filas         = _estado["filas"],
            resultado_texto = _estado["resultado_txt"],
            parent_widget = frame,
        )

    btn_calc.configure(command=ejecutar)
    btn_pdf.configure(command=imprimir_pdf)
    frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=3); frame.rowconfigure(0, weight=1)
    return frame
