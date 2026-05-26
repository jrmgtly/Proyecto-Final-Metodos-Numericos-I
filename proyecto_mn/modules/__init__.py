"""
Paquete de módulos numéricos para el Proyecto Final de Métodos Numéricos.
Universidad Mariano Gálvez – Facultad de Ingeniería en Sistemas.
"""
from .raices import biseccion, newton_raphson, secante
from .interpolacion import lagrange, newton_interpolacion
from .sistemas import gauss_seidel, factorizacion_lu
from .derivacion_integracion import (
    tabla_derivadas, trapecio, simpson_13, simpson_38
)
from .ecuaciones_diferenciales import euler, runge_kutta_4, comparar_euler_rk4
