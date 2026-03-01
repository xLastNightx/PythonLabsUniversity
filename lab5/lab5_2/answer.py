# найти сумму всех четных чисел от 0 до n
# тесты все возможные
# передаем в функцию только n, числа целые
# 0, 1, учитываем еще отрицательные числа, при не правильно вводе тоже обрабатывать
import pytest

class Incorrect_Input(Exception):
    """Не правильный ввод в текстовое поле"""
    pass

class Incorrect_Number(Exception):
    """Не положительное число"""
    pass

class Must_Be_Only_One_Number(Exception):
    """Должно быть 1 число"""
    pass

class Too_Low(Exception):
    """Слишком низкое значение"""
    pass


def find_sum_of_chetnye(last_number):
    try:
        if isinstance(last_number, str):
            last_number = last_number.strip()
            
            parts = last_number.split()
            if len(parts) != 1:
                raise Must_Be_Only_One_Number("Должно быть только одно число")
            
            if not last_number or not last_number.lstrip('-').isdigit():
                raise Incorrect_Input("Должно быть целое число")
            
            last_number = int(last_number)
        
        elif not isinstance(last_number, int):
            raise Incorrect_Input("Должно быть целое число")
        
        if last_number < 0:
            raise Incorrect_Number("Число должно быть положительным")
        
        if last_number <= 1:
            raise Too_Low("Слишком низкое значение, программа выводит сумму четных")
        
        # Вычисляем сумму четных чисел
        total = 0
        current = 2
        while current <= last_number:
            total += current
            current += 2
        
        return total
        
    except (Incorrect_Number, Incorrect_Input, Must_Be_Only_One_Number, Too_Low) as e:
        print(str(e))
        return False
    except Exception:
        print("Не правильное значение, должно быть одно положительное число")
        return False


# Тесты
@pytest.mark.basic
def test_basic():
    """Тест основных случаев"""
    assert find_sum_of_chetnye("10") == 30
    
    assert find_sum_of_chetnye("22") == 132
    
    assert find_sum_of_chetnye(9) == 20
    
    assert find_sum_of_chetnye(5) == 6

    assert find_sum_of_chetnye(2) == 2
    
    assert find_sum_of_chetnye(3) == 2
    
    assert find_sum_of_chetnye(100) == 2550
    print("Основные тесты пройдены")

@pytest.fixture
def fixtured_function():
    return [(5, 6), (10, 30)]

def test_with_fixture(fixtured_function):
    for input, output in fixtured_function:
        assert find_sum_of_chetnye(input) == output

@pytest.fixture
def base_test(autouse=True):
    print("Strat")
    yield
    print("End")

def test_of_base_test():
    assert find_sum_of_chetnye(10) == 30

@pytest.mark.parametrize("input_value, output_value", [(5, 6), (10, 30)])
def test_with_parametrize(input_value, output_value):
    assert find_sum_of_chetnye(input_value) == output_value

@pytest.mark.performance
def test_performance_large_numbers():
    """Тесты с большими числами для проверки производительности"""
    assert find_sum_of_chetnye(1000000) == 250000500000
    assert find_sum_of_chetnye("1000000") == 250000500000

def test_incorrect():
    """Тест некорректного ввода"""
    assert find_sum_of_chetnye("22 33 66") == False

    assert find_sum_of_chetnye("0") == False
    
    assert find_sum_of_chetnye("-2") == False
    
    assert find_sum_of_chetnye("") == False
    
    assert find_sum_of_chetnye("   ") == False
    
    assert find_sum_of_chetnye("abc") == False
    
    assert find_sum_of_chetnye("10.5") == False

    assert find_sum_of_chetnye([10]) == False
    print("Тесты некорректного ввода пройдены")

def manual_test():
    print("Ручное тестирование функции find_sum_of_chetnye:")
    print("_" * 50)
    
    test_cases = [
        ("10", "30"),
        ("22", "132"),
        ("5", "6"),
        ("2", "2"),
        ("0", "False (слишком низкое)"),
        ("1", "False (слишком низкое)"),
        ("-5", "False (отрицательное)"),
        ("22 33", "False (много чисел)"),
        ("abc", "False (не число)"),
        ("10.5", "False (дробное)"),
    ]
    
    for test_input, expected in test_cases:
        result = find_sum_of_chetnye(test_input)
        print(f"Ввод: '{test_input}' Результат: {result} (ожидается: {expected})")

if __name__ == "__main__":
    print("Запуск автоматических тестов...")
    test_basic()
    test_incorrect()
    print("Все автоматические тесты пройдены успешно!")
    
    # Запуск ручного тестирования
    manual_test()

    print("для запуска: pytest answer.py -v или pytest answer.py -m basic -v")
