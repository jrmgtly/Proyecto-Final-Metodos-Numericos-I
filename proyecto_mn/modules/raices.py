"""
Módulo 1: Cálculo de Raíces
Implementa los métodos de Bisección, Newton-Raphson y Secante.
"""
import numpy as np


def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de bisección para encontrar raíces de funciones continuas.

    Parámetros:
        f        -- función continua en [a, b]
        a, b     -- extremos del intervalo inicial (f(a)*f(b) < 0)
        tol      -- tolerancia de error (default 1e-6)
        max_iter -- número máximo de iteraciones (default 100)

    Retorna:
        dict con raiz, iteraciones, error, historial de pasos
    """
    if f(a) * f(b) > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")

    historial = []
    error = float("inf")
    iteracion = 0

    while error > tol and iteracion < max_iter:
        c = (a + b) / 2.0
        fc = f(c)
        error = abs(b - a) / 2.0
        historial.append({
            "iter": iteracion + 1,
            "a": a, "b": b, "c": c,
            "f(c)": fc, "error": error
        })

        if abs(fc) < 1e-14:
            break
        elif f(a) * fc < 0:
            b = c
        else:
            a = c
        iteracion += 1

    return {
        "raiz": c,
        "iteraciones": iteracion,
        "error": error,
        "historial": historial
    }


def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    """
    Método de Newton-Raphson para encontrar raíces usando la derivada.

    Parámetros:
        f        -- función f(x)
        df       -- derivada f'(x)
        x0       -- valor inicial
        tol      -- tolerancia de error (default 1e-6)
        max_iter -- número máximo de iteraciones

    Retorna:
        dict con raiz, iteraciones, error, historial de pasos
    """
    x = x0
    historial = []
    error = float("inf")

    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-14:
            raise ValueError(f"Derivada cero en x={x}. El método no converge.")

        x_nuevo = x - fx / dfx
        error = abs(x_nuevo - x)

        historial.append({
            "iter": i + 1,
            "x": x,
            "f(x)": fx,
            "f'(x)": dfx,
            "x_nuevo": x_nuevo,
            "error": error
        })

        x = x_nuevo
        if error < tol:
            break

    return {
        "raiz": x,
        "iteraciones": i + 1,
        "error": error,
        "historial": historial
    }


def secante(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Método de la Secante para encontrar raíces sin necesitar la derivada.

    Parámetros:
        f        -- función f(x)
        x0, x1   -- dos valores iniciales
        tol      -- tolerancia de error (default 1e-6)
        max_iter -- número máximo de iteraciones

    Retorna:
        dict con raiz, iteraciones, error, historial de pasos
    """
    historial = []
    error = float("inf")

    for i in range(max_iter):
        f0, f1 = f(x0), f(x1)

        if abs(f1 - f0) < 1e-14:
            raise ValueError("División por cero en el método de la secante.")

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        error = abs(x2 - x1)

        historial.append({
            "iter": i + 1,
            "x0": x0,
            "x1": x1,
            "x2": x2,
            "f(x2)": f(x2),
            "error": error
        })

        x0, x1 = x1, x2
        if error < tol:
            break

    return {
        "raiz": x2,
        "iteraciones": i + 1,
        "error": error,
        "historial": historial
    }
