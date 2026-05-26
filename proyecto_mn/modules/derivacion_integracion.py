"""
Módulo 4: Derivación e Integración Numérica
Implementa diferencias finitas y métodos de Trapecio y Simpson.
"""
import numpy as np


# ─────────────────────────────────────────────
#  DERIVACIÓN NUMÉRICA – Diferencias Finitas
# ─────────────────────────────────────────────

def derivada_adelante(f, x, h=1e-5):
    """
    Aproximación de la primera derivada por diferencia finita hacia adelante.
    Orden O(h).

    f'(x) ≈ [f(x+h) - f(x)] / h
    """
    return (f(x + h) - f(x)) / h


def derivada_atras(f, x, h=1e-5):
    """
    Aproximación de la primera derivada por diferencia finita hacia atrás.
    Orden O(h).

    f'(x) ≈ [f(x) - f(x-h)] / h
    """
    return (f(x) - f(x - h)) / h


def derivada_central(f, x, h=1e-5):
    """
    Aproximación de la primera derivada por diferencia finita central.
    Orden O(h²) — más precisa que adelante/atrás.

    f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def segunda_derivada(f, x, h=1e-5):
    """
    Aproximación de la segunda derivada por diferencias finitas centrales.
    Orden O(h²).

    f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h²
    """
    return (f(x + h) - 2 * f(x) + f(x - h)) / h ** 2


def tabla_derivadas(f, x, h=1e-5):
    """
    Calcula todas las aproximaciones de derivadas en un punto dado.

    Retorna dict con todos los métodos y sus valores.
    """
    return {
        "adelante":  derivada_adelante(f, x, h),
        "atras":     derivada_atras(f, x, h),
        "central":   derivada_central(f, x, h),
        "segunda":   segunda_derivada(f, x, h),
        "x": x,
        "h": h
    }


# ─────────────────────────────────────────────
#  INTEGRACIÓN NUMÉRICA
# ─────────────────────────────────────────────

def trapecio(f, a, b, n=100):
    """
    Integración numérica mediante la Regla del Trapecio Compuesta.

    ∫f(x)dx ≈ (h/2)[f(x₀) + 2f(x₁) + ... + 2f(xₙ₋₁) + f(xₙ)]

    Parámetros:
        f -- función a integrar
        a -- límite inferior
        b -- límite superior
        n -- número de subintervalos (default 100)

    Retorna:
        dict con resultado, pasos y nodos evaluados
    """
    if n < 1:
        raise ValueError("n debe ser al menos 1.")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])

    integral = h / 2 * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])

    return {
        "resultado": integral,
        "n": n,
        "h": h,
        "x": x,
        "y": y,
        "metodo": "Trapecio Compuesto"
    }


def simpson_13(f, a, b, n=100):
    """
    Integración numérica mediante la Regla de Simpson 1/3 Compuesta.
    n debe ser par.

    ∫f(x)dx ≈ (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + f(xₙ)]

    Parámetros:
        f -- función a integrar
        a -- límite inferior
        b -- límite superior
        n -- número de subintervalos (debe ser par, default 100)

    Retorna:
        dict con resultado, pasos y nodos evaluados
    """
    if n % 2 != 0:
        n += 1  # Asegurar que n sea par

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])

    integral = y[0] + y[-1]
    integral += 4 * np.sum(y[1:-1:2])   # Índices impares
    integral += 2 * np.sum(y[2:-2:2])   # Índices pares (excepto extremos)
    integral *= h / 3

    return {
        "resultado": integral,
        "n": n,
        "h": h,
        "x": x,
        "y": y,
        "metodo": "Simpson 1/3 Compuesto"
    }


def simpson_38(f, a, b, n=99):
    """
    Integración numérica mediante la Regla de Simpson 3/8 Compuesta.
    n debe ser múltiplo de 3.

    Parámetros:
        f -- función a integrar
        a -- límite inferior
        b -- límite superior
        n -- número de subintervalos (múltiplo de 3, default 99)

    Retorna:
        dict con resultado, pasos y nodos evaluados
    """
    while n % 3 != 0:
        n += 1

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])

    integral = y[0] + y[-1]
    for i in range(1, n):
        if i % 3 == 0:
            integral += 2 * y[i]
        else:
            integral += 3 * y[i]
    integral *= 3 * h / 8

    return {
        "resultado": integral,
        "n": n,
        "h": h,
        "x": x,
        "y": y,
        "metodo": "Simpson 3/8 Compuesto"
    }


def comparar_integracion(f, a, b, n=100):
    """
    Compara los tres métodos de integración implementados.

    Retorna dict con resultados de Trapecio, Simpson 1/3 y Simpson 3/8.
    """
    return {
        "trapecio":    trapecio(f, a, b, n)["resultado"],
        "simpson_13":  simpson_13(f, a, b, n)["resultado"],
        "simpson_38":  simpson_38(f, a, b, n)["resultado"],
        "a": a, "b": b, "n": n
    }
