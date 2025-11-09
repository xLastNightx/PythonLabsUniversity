import numpy as np
from scipy.linalg import inv

def solve_linear_system(A, B):
    print("Матрица A:")
    print(A)
    print("\nВектор B:")
    print(B)
    
    # Проверка определителя
    det_A = np.linalg.det(A)
    print(f"\nОпределитель матрицы A: {det_A:.4f}")
    
    if abs(det_A) < 1e-10:
        print("Матрица A вырождена, решение невозможно")
        return None, None
    
    # Решение через обратную матрицу (scipy)
    A_inv = inv(A)
    x_exact = A_inv @ B
    
    # Округление до одного знака после запятой
    x_rounded = np.round(x_exact, 1)
    
    print("\nТочное решение:")
    for i, val in enumerate(x_exact, 1):
        print(f"x_{i} = {val:.6f}")
    
    print(f"\nОкруглённое решение (до 1 знака):")
    print(f"x = {x_rounded}")
    
    return x_rounded, x_exact

def main():
    # Данные из системы уравнений
    A = np.array([
        [-2.0, -8.5, -3.4, 3.5],
        [0.0, 2.4, 0.0, 8.2],
        [2.5, 1.6, 2.1, 3.0],
        [0.3, -0.4, -4.8, 4.6]
    ])

    B = np.array([-1.88, -3.28, -0.5, -2.83])

    x_rounded, x_exact = solve_linear_system(A, B)

if __name__ == "__main__":
    main()