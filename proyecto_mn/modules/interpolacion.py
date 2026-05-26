"""
Módulo 2: Interpolación y Ajuste de Curvas
Implementa los polinomios de Lagrange y Newton.
"""
import numpy as np


def lagrange(x_datos, y_datos, x_interp):
    """
    Interpolación mediante el polinomio de Lagrange.

    Parámetros:
        x_datos  -- array de puntos x conocidos
        y_datos  -- array de valores y conocidos
        x_interp -- array de puntos x a interpolar

    Retorna:
        dict con y_interp (valores interpolados) y polinomio como texto
    """
    x_datos = np.array(x_datos, dtype=float)
    y_datos = np.array(y_datos, dtype=float)
    x_interp = np.array(x_interp, dtype=float)
    n = len(x_datos)

    def L(k, x):
        """Polinomio base de Lagrange L_k(x)."""
        num = np.ones_like(x, dtype=float)
        den = 1.0
        for j in range(n):
            if j != k:
                num *= (x - x_datos[j])
                den *= (x_datos[k] - x_datos[j])
        return num / den

    y_interp = np.zeros_like(x_interp, dtype=float)
    for k in range(n):
        y_interp += y_datos[k] * L(k, x_interp)

    return {
        "x_interp": x_interp,
        "y_interp": y_interp,
        "x_datos": x_datos,
        "y_datos": y_datos,
        "metodo": "Lagrange",
        "grado": n - 1
    }


def diferencias_divididas(x_datos, y_datos):
    """
    Calcula la tabla de diferencias divididas para el polinomio de Newton.

    Parámetros:
        x_datos -- array de puntos x
        y_datos -- array de valores y

    Retorna:
        tabla -- tabla completa de diferencias divididas (matriz triangular)
    """
    n = len(x_datos)
    tabla = np.zeros((n, n), dtype=float)
    tabla[:, 0] = y_datos

    for j in range(1, n):
        for i in range(n - j):
            denom = x_datos[i + j] - x_datos[i]
            if abs(denom) < 1e-14:
                raise ValueError(f"Puntos x duplicados en posición {i} y {i+j}.")
            tabla[i, j] = (tabla[i + 1, j - 1] - tabla[i, j - 1]) / denom

    return tabla


def newton_interpolacion(x_datos, y_datos, x_interp):
    """
    Interpolación mediante el polinomio de Newton (diferencias divididas).

    Parámetros:
        x_datos  -- array de puntos x conocidos
        y_datos  -- array de valores y conocidos
        x_interp -- array de puntos x a interpolar

    Retorna:
        dict con y_interp, tabla de diferencias divididas y coeficientes
    """
    x_datos = np.array(x_datos, dtype=float)
    y_datos = np.array(y_datos, dtype=float)
    x_interp = np.array(x_interp, dtype=float)

    tabla = diferencias_divididas(x_datos, y_datos)
    coef = tabla[0, :]  # Coeficientes del polinomio de Newton

    def evaluar(x):
        """Evalúa el polinomio de Newton en x usando el método de Horner."""
        n = len(coef)
        resultado = np.zeros_like(x, dtype=float)
        for i in range(n):
            termino = coef[i]
            for j in range(i):
                termino *= (x - x_datos[j])
            resultado += termino
        return resultado

    y_interp = evaluar(x_interp)

    return {
        "x_interp": x_interp,
        "y_interp": y_interp,
        "x_datos": x_datos,
        "y_datos": y_datos,
        "coeficientes": coef,
        "tabla_dd": tabla,
        "metodo": "Newton",
        "grado": len(x_datos) - 1
    }
