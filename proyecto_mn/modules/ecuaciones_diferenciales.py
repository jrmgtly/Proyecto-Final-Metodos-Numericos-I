"""
Módulo 5: Ecuaciones Diferenciales Ordinarias (EDO)
Implementa los métodos de Euler y Runge-Kutta de orden 4.
"""
import numpy as np


def euler(f, t0, y0, tf, h=0.1):
    """
    Resuelve una EDO dy/dt = f(t, y) mediante el Método de Euler.

    Esquema: y_{n+1} = y_n + h·f(t_n, y_n)

    Parámetros:
        f  -- función f(t, y) de la EDO
        t0 -- tiempo inicial
        y0 -- condición inicial y(t0)
        tf -- tiempo final
        h  -- tamaño de paso (default 0.1)

    Retorna:
        dict con arrays t y y (solución aproximada) e información del método
    """
    if h <= 0:
        raise ValueError("El paso h debe ser positivo.")
    if tf <= t0:
        raise ValueError("tf debe ser mayor que t0.")

    n_pasos = int((tf - t0) / h) + 1
    t = np.linspace(t0, tf, n_pasos)
    y = np.zeros(n_pasos)
    y[0] = y0

    for i in range(n_pasos - 1):
        y[i + 1] = y[i] + h * f(t[i], y[i])

    return {
        "t": t,
        "y": y,
        "metodo": "Euler",
        "h": h,
        "pasos": n_pasos - 1
    }


def runge_kutta_4(f, t0, y0, tf, h=0.1):
    """
    Resuelve una EDO dy/dt = f(t, y) mediante Runge-Kutta de Orden 4 (RK4).

    Esquema:
        k1 = h·f(t_n, y_n)
        k2 = h·f(t_n + h/2, y_n + k1/2)
        k3 = h·f(t_n + h/2, y_n + k2/2)
        k4 = h·f(t_n + h,   y_n + k3)
        y_{n+1} = y_n + (k1 + 2k2 + 2k3 + k4) / 6

    Parámetros:
        f  -- función f(t, y) de la EDO
        t0 -- tiempo inicial
        y0 -- condición inicial y(t0)
        tf -- tiempo final
        h  -- tamaño de paso (default 0.1)

    Retorna:
        dict con arrays t, y, y los valores de k1..k4 de cada paso
    """
    if h <= 0:
        raise ValueError("El paso h debe ser positivo.")
    if tf <= t0:
        raise ValueError("tf debe ser mayor que t0.")

    n_pasos = int((tf - t0) / h) + 1
    t = np.linspace(t0, tf, n_pasos)
    y = np.zeros(n_pasos)
    y[0] = y0

    detalles_k = []

    for i in range(n_pasos - 1):
        ti, yi = t[i], y[i]

        k1 = h * f(ti,           yi)
        k2 = h * f(ti + h / 2,  yi + k1 / 2)
        k3 = h * f(ti + h / 2,  yi + k2 / 2)
        k4 = h * f(ti + h,      yi + k3)

        y[i + 1] = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6

        detalles_k.append({
            "t": ti, "y": yi,
            "k1": k1, "k2": k2, "k3": k3, "k4": k4,
            "y_nuevo": y[i + 1]
        })

    return {
        "t": t,
        "y": y,
        "metodo": "Runge-Kutta 4",
        "h": h,
        "pasos": n_pasos - 1,
        "detalles_k": detalles_k
    }


def comparar_euler_rk4(f, t0, y0, tf, h=0.1, solucion_exacta=None):
    """
    Compara las soluciones de Euler y RK4 para la misma EDO.

    Parámetros:
        f               -- función f(t, y)
        t0, y0, tf, h   -- mismos que euler/runge_kutta_4
        solucion_exacta -- función y_exacta(t) opcional para comparar error

    Retorna:
        dict con resultados de ambos métodos y error relativo si aplica
    """
    res_euler = euler(f, t0, y0, tf, h)
    res_rk4   = runge_kutta_4(f, t0, y0, tf, h)

    resultado = {
        "euler": res_euler,
        "rk4":   res_rk4,
        "t":     res_euler["t"]
    }

    if solucion_exacta is not None:
        y_exacto = np.array([solucion_exacta(ti) for ti in res_euler["t"]])
        resultado["y_exacto"]      = y_exacto
        resultado["error_euler"]   = np.abs(res_euler["y"] - y_exacto)
        resultado["error_rk4"]     = np.abs(res_rk4["y"] - y_exacto)

    return resultado
