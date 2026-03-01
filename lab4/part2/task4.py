import numpy as np
from scipy import integrate

# Определённый интеграл 
def f(x): return x**2 * np.sin(x)

# Пределы интегрирования
a, b = 0, np.pi

# Вычисляем интеграл
I1, _ = integrate.quad(f, a, b)

print("ОПРЕДЕЛЁННЫЙ ИНТЕГРАЛ")
print("Функция: f(x) = x^2 * sin(x)")
print(f"Интервал: [{a}, {b}]")
print(f"Значение интеграла: {I1:.5f}")

# Двойной интеграл 
def g(y, x):
    return x * np.exp(-(x**2 + y**2))

# Пределы интегрирования
x_limits = [0, 1]
y_limits = [0, 2]

# Вычисляем двойной интеграл
I2, _ = integrate.dblquad(g, *x_limits, lambda x: y_limits[0], lambda x: y_limits[1])

print("\nДВОЙНОЙ ИНТЕГРАЛ")
print("Функция: f(x, y) = x * exp(-(x^2 + y^2))")
print(f"Область: x ∈ [{x_limits[0]}, {x_limits[1]}], y ∈ [{y_limits[0]}, {y_limits[1]}]")
print(f"Значение интеграла: {I2:.5f}")
