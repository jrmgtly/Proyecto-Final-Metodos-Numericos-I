# Métodos Numéricos con Python
### Proyecto Final – Universidad Mariano Gálvez
**Facultad de Ingeniería en Sistemas de Información y Ciencias de la Computación**
Código de Curso: 021 | Nombre: Métodos Numéricos - Python

---

## Descripción

Aplicación de escritorio desarrollada en Python con interfaz gráfica (Tkinter) que implementa
los principales métodos numéricos estudiados en el curso, organizados en 5 módulos.

## Módulos Implementados

| # | Módulo | Métodos |
|---|--------|---------|
| 1 | Cálculo de Raíces | Bisección, Newton-Raphson, Secante |
| 2 | Interpolación | Lagrange, Newton (Diferencias Divididas) |
| 3 | Sistemas Lineales | Gauss-Seidel, Factorización LU |
| 4 | Derivación e Integración | Diferencias Finitas, Trapecio, Simpson 1/3 y 3/8 |
| 5 | Ecuaciones Diferenciales | Euler, Runge-Kutta Orden 4 |

## Requisitos del Sistema

- Python 3.8 o superior
- Windows / macOS / Linux

## Instalación

### 1. Clonar / Descomprimir el proyecto

```bash
cd proyecto_metodos_numericos
```

### 2. (Recomendado) Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Estructura del Proyecto

```
proyecto_metodos_numericos/
│
├── main.py                          # Punto de entrada de la aplicación
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Este archivo
│
├── modules/                         # Lógica de los métodos numéricos
│   ├── __init__.py
│   ├── raices.py                    # Bisección, Newton-Raphson, Secante
│   ├── interpolacion.py             # Lagrange, Newton
│   ├── sistemas.py                  # Gauss-Seidel, LU
│   ├── derivacion_integracion.py    # Diferencias finitas, Trapecio, Simpson
│   └── ecuaciones_diferenciales.py  # Euler, Runge-Kutta 4
│
└── gui/                             # Interfaz gráfica (Tkinter)
    ├── __init__.py
    ├── tab_raices.py
    ├── tab_interpolacion.py
    ├── tab_sistemas.py
    ├── tab_derivacion.py
    └── tab_edo.py
```

## Guía de Uso Rápido

### Módulo 1 – Cálculo de Raíces
1. Seleccionar el método (Bisección, Newton-Raphson o Secante)
2. Ingresar la función f(x) usando sintaxis Python (ej: `x**3 - x - 2`)
3. Para Newton-Raphson, ingresar también f'(x)
4. Configurar intervalo [a, b], tolerancia e iteraciones máximas
5. Presionar **▶ Calcular Raíz**

### Módulo 2 – Interpolación
1. Ingresar puntos x e y separados por comas
2. Ingresar los puntos a interpolar
3. Seleccionar el método y presionar **▶ Interpolar**

### Módulo 3 – Sistemas Lineales
1. Ingresar la matriz A (cada fila en una línea, elementos separados por comas)
2. Ingresar el vector b
3. Seleccionar Gauss-Seidel o LU y presionar **▶ Resolver Sistema**

### Módulo 4 – Derivación e Integración
- **Derivación**: ingresar f(x) y el punto x donde calcular las derivadas
- **Integración**: ingresar f(x), límites [a, b] y número de subintervalos n

### Módulo 5 – Ecuaciones Diferenciales
1. Ingresar `dy/dt = f(t, y)` en sintaxis Python (ej: `-2 * y + np.sin(t)`)
2. Opcionalmente ingresar la solución exacta para comparar errores
3. Configurar condiciones iniciales t₀, y₀, tf y paso h
4. Presionar **▶ Resolver EDO**

## Ejemplos de Funciones

| Función matemática | Sintaxis Python |
|-------------------|-----------------|
| x³ - x - 2 | `x**3 - x - 2` |
| e^x | `np.exp(x)` |
| sin(x) | `np.sin(x)` |
| cos(x)/x | `np.cos(x)/x` |
| √x | `np.sqrt(x)` |
| ln(x) | `np.log(x)` |

---
*Proyecto desarrollado para el curso Métodos Numéricos – Python (021)*
*Universidad Mariano Gálvez – 2024*
