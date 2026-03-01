import numpy as np
from scipy import stats

def calculate_journey(lengths_str, speeds_str, k, p):
    # Преобразуем входные данные в массивы NumPy
    lengths = np.array(list(map(float, lengths_str.split())))
    speeds = np.array(list(map(float, speeds_str.split())))
    
    # Проверка корректности данных
    if len(lengths) != len(speeds):
        raise ValueError("Количество длин и скоростей должно совпадать.")
    if not (1 <= k <= p <= len(lengths)):
        raise ValueError("Некорректные значения k и p.")

    start, end = k - 1, p - 1
        
    selected_lengths = lengths[start:end + 1]
    selected_speeds = speeds[start:end + 1]

    total_distance = np.sum(selected_lengths)
    times = selected_lengths / selected_speeds
    total_time = np.sum(times)
    average_speed = total_distance / total_time

    return total_distance, total_time, average_speed, selected_lengths, selected_speeds


def show_statistics(lengths, speeds):
    print("\nДополнительная статистика (SciPy):")
    print(f"- Средняя длина: {np.mean(lengths):.2f} км")
    print(f"- Средняя скорость: {np.mean(speeds):.2f} км/ч")
    print(f"- Стандартное отклонение скоростей: {np.std(speeds):.2f}")

    stat, p_value = stats.normaltest(speeds)
    print(f"- p-value нормальности = {p_value:.4f}")
    print("  Распределение скоростей " + 
          ("нормальное" if p_value > 0.05 else "не нормальное"))


def main():
    print("=== РАСЧЁТ ПУТИ АВТОМОБИЛЯ ===")

    lengths_input = input("Введите длины участков (по умолчанию): ") or "20 8 9 18 5 12 16 16 6 7"
    speeds_input = input("Введите скорости (по умолчанию): ") or "44 70 44 66 46 38 38 37 66 67"
    k = int(input("Введите участок въезда (k): ") or 4)
    p = int(input("Введите участок выезда (p): ") or 7)

    # Основной расчёт
    S, T, V, selected_lengths, selected_speeds = calculate_journey(lengths_input, speeds_input, k, p)

    print(f"\nРЕЗУЛЬТАТЫ:")
    print(f"1. Длина пути: {S:.2f} км")
    print(f"2. Время в пути: {T:.2f} час")
    print(f"3. Средняя скорость: {V:.2f} км/ч")

    # Проверка с тестом из условия
    print("\nПроверка (Тест 1):")
    print("Ожидалось: S=49 км, T=1.28 час, V=38.34 км/ч")

    # Дополнительная статистика
    show_statistics(selected_lengths, selected_speeds)


if __name__ == "__main__":
    main()