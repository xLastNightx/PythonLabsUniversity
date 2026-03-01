import numpy as np
from scipy import stats

def analyze_transport_expenses():
    # Создаем массив расходов на проезд по месяцам
    np.random.seed(42)
    expenses = np.random.randint(2000, 8000, 12)
    
    print("Расходы на проезд по месяцам:")
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    
    for i, (month, expense) in enumerate(zip(months, expenses), 1): print(f"{i:2d}. {month}: {expense} руб.")
    
    # Сравнение зимнего и летнего периодов
    winter_months = [0, 1, 11]   # Январь, Февраль, Декабрь
    summer_months = [5, 6, 7]    # Июнь, Июль, Август
    
    winter_expenses = expenses[winter_months]
    summer_expenses = expenses[summer_months]
    
    winter_total = np.sum(winter_expenses)
    summer_total = np.sum(summer_expenses)
    
    print(f"\nСравнение периодов:")
    print(f"Зимние месяцы (дек, янв, фев): {winter_expenses}")
    print(f"Сумма зимой: {winter_total} руб.")
    print(f"Летние месяцы (июнь, июль, авг): {summer_expenses}")
    print(f"Сумма летом: {summer_total} руб.")
    
    if winter_total > summer_total: print("Зимой тратится БОЛЬШЕ денег на проезд")
    elif summer_total > winter_total: print("Летом тратится БОЛЬШЕ денег на проезд")
    else: print("Расходы зимой и летом ОДИНАКОВЫ")
    
    # Находим месяцы с наибольшими расходами
    max_expense = np.max(expenses)
    max_months_indices = np.where(expenses == max_expense)[0] #[0] - извлекает индексы из кортежа

    print(f"Максимальный расход: {max_expense} руб.")
    print("Месяцы с максимальными расходами:")
    for idx in max_months_indices: print(f"  - {months[idx]} (месяц №{idx + 1})")
    
    # Проверяем статистическую значимость различий с помощью t-теста
    t_stat, p_value = stats.ttest_ind(winter_expenses, summer_expenses)
    print(f"t-тест различий зимних и летних расходов: p-value = {p_value:.4f}")
    if p_value < 0.05:
        print("   Различия статистически значимы (p < 0.05)")
    else:
        print("   Различия не статистически значимы (p ≥ 0.05)")
    
    return expenses, months

if __name__ == "__main__":
    expenses, months = analyze_transport_expenses()
    print("\nАнализ завершен!")