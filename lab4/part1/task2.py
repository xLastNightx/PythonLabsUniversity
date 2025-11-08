import matplotlib.pyplot as plt
import numpy as np

def plot_function():
    x = np.linspace(-10, 10, 1000)
    
    y = 5 / (x**2 - 9)

    plt.figure(figsize=(10, 6))

    plt.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = \frac{5}{x^2 - 9}$')
    
    # Настройки графика
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.title(r'График функции $f(x) = \frac{5}{x^2 - 9}$', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # точки разрыва
    plt.axvline(x=-3, color='red', linestyle='--', alpha=0.7, label='точки разрыва')
    plt.axvline(x=3, color='red', linestyle='--', alpha=0.7)
    
    # Горизонтальные линии
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # пределы по y 
    plt.ylim(-10, 10)
    
    plt.text(-3.2, 9, 'x = -3', fontsize=10, color='red')
    plt.text(2.8, 9, 'x = 3', fontsize=10, color='red')
    
    plt.tight_layout()
    plt.show()

plot_function()