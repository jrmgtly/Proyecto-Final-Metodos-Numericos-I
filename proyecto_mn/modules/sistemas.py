"""
Módulo 3: Sistemas de Ecuaciones Lineales
Implementa el método de Gauss-Seidel y la Factorización LU.
"""
import numpy as np


def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema lineal Ax = b mediante el método iterativo de Gauss-Seidel.

    Parámetros:
        A        -- matriz de coeficientes (n x n)
        b        -- vector de términos independientes (n)
        x0       -- aproximación inicial (default: vector de ceros)
        tol      -- tolerancia de convergencia (default 1e-6)
        max_iter -- número máximo de iteraciones

    Retorna:
        dict con solución, iteraciones, error y historial
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    # Verificar diagonal dominante (advertencia)
    diag_dom = all(
        abs(A[i, i]) >= sum(abs(A[i, j]) for j in range(n) if j != i)
        for i in range(n)
    )

    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float)

    historial = []
    error = float("inf")

    for k in range(max_iter):
        x_ant = x.copy()

        for i in range(n):
            suma = b[i]
            for j in range(n):
                if j != i:
                    suma -= A[i, j] * x[j]
            if abs(A[i, i]) < 1e-14:
                raise ValueError(f"Elemento diagonal A[{i},{i}] es cero o muy pequeño.")
            x[i] = suma / A[i, i]

        error = np.linalg.norm(x - x_ant, ord=np.inf)
        historial.append({
            "iter": k + 1,
            "x": x.copy(),
            "error": error
        })

        if error < tol:
            break

    return {
        "solucion": x,
        "iteraciones": k + 1,
        "error": error,
        "historial": historial,
        "diagonal_dominante": diag_dom,
        "convergio": error < tol
    }


def factorizacion_lu(A, b):
    """
    Resuelve un sistema lineal Ax = b mediante factorización LU con pivoteo parcial.

    Parámetros:
        A -- matriz de coeficientes (n x n)
        b -- vector de términos independientes (n)

    Retorna:
        dict con solución, matrices L y U, y vector de permutación
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    # Matrices L y U
    L = np.eye(n)
    U = A.copy()
    P = np.eye(n)  # Matriz de permutación

    # Eliminación Gaussiana con pivoteo parcial
    for k in range(n - 1):
        # Pivoteo parcial
        max_fila = k + np.argmax(abs(U[k:, k]))
        if max_fila != k:
            U[[k, max_fila]] = U[[max_fila, k]]
            P[[k, max_fila]] = P[[max_fila, k]]
            if k > 0:
                L[[k, max_fila], :k] = L[[max_fila, k], :k]

        if abs(U[k, k]) < 1e-14:
            raise ValueError(f"Matriz singular: pivote cero en posición ({k},{k}).")

        for i in range(k + 1, n):
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            U[i, k:] -= factor * U[k, k:]

    # Resolución Ly = Pb (sustitución hacia adelante)
    Pb = P @ b
    y = np.zeros(n)
    for i in range(n):
        y[i] = Pb[i] - np.dot(L[i, :i], y[:i])

    # Resolución Ux = y (sustitución hacia atrás)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if abs(U[i, i]) < 1e-14:
            raise ValueError("Matriz singular: no tiene solución única.")
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

    # Verificación del residuo
    residuo = np.linalg.norm(A @ x - b)

    return {
        "solucion": x,
        "L": L,
        "U": U,
        "P": P,
        "residuo": residuo
    }
