"""
GUI – Pestaña: Módulo 2 - Interpolación y Ajuste de Curvas
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.interpolacion import lagrange, newton_interpolacion
from gui.pdf_export import exportar_pdf

FONT_LABEL   = ("Segoe UI", 10)
FONT_TITLE   = ("Segoe UI", 11, "bold")
COLOR_ACCENT = "#1565C0"

_estado = {"filas": [], "resultado_txt": "", "metodo": ""}


def build_tab(parent):
    frame = ttk.Frame(parent)

    panel_ctrl = ttk.LabelFrame(frame, text=" Datos de Entrada ", padding=10)
    panel_ctrl.grid(row=0, column=0, sticky="nsew", padx=10, pady=8)

    ttk.Label(panel_ctrl, text="Método:", font=FONT_TITLE).grid(row=0, column=0, sticky="w", pady=(0,2))
    metodo_var = tk.StringVar(value="Lagrange")
    ttk.Combobox(panel_ctrl, textvariable=metodo_var,
                 values=["Lagrange","Newton"], state="readonly",
                 width=22).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,8))

    ttk.Label(panel_ctrl, text="Puntos x (separados por coma):", font=FONT_LABEL).grid(row=2, column=0, columnspan=2, sticky="w")
    entrada_x = ttk.Entry(panel_ctrl, width=26); entrada_x.insert(0,"0, 1, 2, 3, 4")
    entrada_x.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0,6))

    ttk.Label(panel_ctrl, text="Valores f(x) (separados por coma):", font=FONT_LABEL).grid(row=4, column=0, columnspan=2, sticky="w")
    entrada_y = ttk.Entry(panel_ctrl, width=26); entrada_y.insert(0,"1, 2.7, 7.4, 20.1, 54.6")
    entrada_y.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0,6))

    ttk.Label(panel_ctrl, text="Punto(s) a interpolar (coma):", font=FONT_LABEL).grid(row=6, column=0, columnspan=2, sticky="w")
    entrada_xi = ttk.Entry(panel_ctrl, width=26); entrada_xi.insert(0,"0.5, 1.5, 2.5, 3.5")
    entrada_xi.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0,8))

    btn_calc = ttk.Button(panel_ctrl, text="▶  Interpolar")
    btn_calc.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0,4))

    btn_pdf = ttk.Button(panel_ctrl, text="🖨  Imprimir PDF")
    btn_pdf.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0,8))

    resultado_var = tk.StringVar(value="—")
    ttk.Label(panel_ctrl, text="Valores interpolados:", font=FONT_TITLE).grid(row=10, column=0, columnspan=2, sticky="w", pady=(4,2))
    ttk.Label(panel_ctrl, textvariable=resultado_var, font=("Courier",9),
              foreground=COLOR_ACCENT, wraplength=220, justify="left").grid(row=11, column=0, columnspan=2, sticky="w")

    ttk.Label(panel_ctrl, text="Tabla Diferencias Divididas:", font=FONT_TITLE).grid(row=12, column=0, columnspan=2, sticky="w", pady=(10,2))
    txt_tabla = tk.Text(panel_ctrl, height=7, width=28, font=("Courier",8), state="disabled", bg="#F0F0F0")
    txt_tabla.grid(row=13, column=0, columnspan=2, sticky="ew")

    # Panel derecho
    panel_der = ttk.Frame(frame)
    panel_der.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=8)

    fig = Figure(figsize=(5.5, 4.5), dpi=96, facecolor="#FAFAFA")
    ax  = fig.add_subplot(111)
    ax.set_title("Interpolación", fontsize=10); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=panel_der)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def ejecutar():
        try:
            x_datos  = [float(v.strip()) for v in entrada_x.get().split(",")]
            y_datos  = [float(v.strip()) for v in entrada_y.get().split(",")]
            xi_lista = [float(v.strip()) for v in entrada_xi.get().split(",")]
            if len(x_datos) != len(y_datos):
                raise ValueError("Los vectores x e y deben tener el mismo tamaño.")

            met = metodo_var.get()
            res = lagrange(x_datos, y_datos, xi_lista) if met == "Lagrange" else newton_interpolacion(x_datos, y_datos, xi_lista)

            lineas = [f"  x = {xi:.4f}  →  f(x) ≈ {yi:.6f}" for xi,yi in zip(res["x_interp"],res["y_interp"])]
            resultado_var.set("\n".join(lineas))

            # Tabla DD
            txt_tabla.config(state="normal"); txt_tabla.delete("1.0","end")
            filas_pdf = []
            if met == "Newton" and "tabla_dd" in res:
                tabla = res["tabla_dd"]; n = len(x_datos)
                txt_tabla.insert("end", "  " + "  ".join([f"DD{j}" for j in range(n)]) + "\n")
                for i in range(n):
                    fila = f"{x_datos[i]:5.2f}  " + "  ".join(f"{tabla[i,j]:8.4f}" for j in range(n-i))
                    txt_tabla.insert("end", fila+"\n")
                    filas_pdf.append([f"{x_datos[i]:.4f}"] + [f"{tabla[i,j]:.6f}" for j in range(n-i)])
            else:
                txt_tabla.insert("end","(Solo disponible en método Newton)")
                filas_pdf = [[f"{xi:.4f}", f"{yi:.6f}"] for xi,yi in zip(res["x_interp"],res["y_interp"])]
            txt_tabla.config(state="disabled")

            _estado["filas"]       = filas_pdf
            _estado["resultado_txt"] = "  |  ".join(lineas)
            _estado["metodo"]      = met

            # Graficar
            ax.clear()
            x_arr = np.array(x_datos); y_arr = np.array(y_datos)
            x_plot = np.linspace(min(x_arr)-0.3, max(x_arr)+0.3, 300)
            res_plot = (lagrange if met=="Lagrange" else newton_interpolacion)(x_datos, y_datos, x_plot)
            ax.plot(x_plot, res_plot["y_interp"], color=COLOR_ACCENT, lw=2, label=f"Polinomio {met}")
            ax.scatter(x_arr, y_arr, color="red", zorder=5, s=60, label="Datos originales")
            ax.scatter(res["x_interp"], res["y_interp"], color="green", zorder=5, s=50, marker="^", label="Interpolados")
            ax.set_title(f"Interpolación – {met} (grado {res['grado']})", fontsize=10)
            ax.set_xlabel("x"); ax.set_ylabel("f(x)")
            ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
            fig.tight_layout(); canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def imprimir_pdf():
        if not _estado["filas"]:
            messagebox.showwarning("Sin datos","Primero ejecuta una interpolación.", parent=frame)
            return
        met = _estado["metodo"]
        cols = ["x","DD0","DD1","DD2","DD3","DD4"] if met=="Newton" else ["x","f(x)"]
        exportar_pdf(
            titulo_modulo = "Módulo 2 – Interpolación y Ajuste de Curvas",
            subtitulo     = f"Método: {met}",
            fig_fuente    = fig,
            encabezados   = cols,
            filas         = _estado["filas"],
            resultado_texto = _estado["resultado_txt"],
            parent_widget = frame,
        )

    btn_calc.configure(command=ejecutar)
    btn_pdf.configure(command=imprimir_pdf)
    frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=3); frame.rowconfigure(0, weight=1)
    return frame
