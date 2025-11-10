import matplotlib.pyplot as plt
import numpy as np

def plot_functions():
    # Создаем массив значений x в градусах (1000 - количество точек на графике, чтобы он был не ломанным)
    x_degrees = np.linspace(-360, 360, 1000)
    
    # Переводим градусы в радианы для вычислений
    x_radians = np.radians(x_degrees)
    
    # Вычисляем функции
    f_x = np.exp(np.cos(x_radians)) + np.log(np.cos(0.6*x_radians)**2 + 1) * np.sin(x_radians)
    h_x = -np.log((np.cos(x_radians) + np.sin(x_radians))**2 + 2.5) + 10
    
    # Создаем график (ширина, длина)
    plt.figure(figsize=(12, 8))
    
    # График f(x) (b- это синий)
    plt.plot(x_degrees, f_x, 'b-', linewidth=2, label=r'$f(x) = e^{\cos x} + \ln(\cos^2(0.6x) + 1) \cdot \sin x$')
    
    # График h(x)
    plt.plot(x_degrees, h_x, 'r-', linewidth=2, label=r'$h(x) = -\ln((\cos x + \sin x)^2 + 2.5) + 10$')
    
    # Настройки графика
    plt.xlabel('Градусы', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Графики функций f(x) и h(x)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Деления на оси X каждые 90 градусов (361, чтобы показывалось 360)
    plt.xticks(np.arange(-360, 361, 90))
    
    # Оси
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # Устанавливаем пределы по y (чтобы перестраховаться)
    plt.ylim(-3, 12)
    
    plt.tight_layout()
    plt.show()

plot_functions()