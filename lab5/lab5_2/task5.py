def combine_dicts(dictA, dictB):
    for key, valueB in dictB.items():
        if key in dictA:
            # Если ключ есть в обоих словарях
            valueA = dictA[key]
            
            if isinstance(valueA, dict) and isinstance(valueB, dict):
                # Рекурсивно объединяем вложенные словари
                combine_dicts(valueA, valueB)
            else:
                # Заменяем значение из dictA значением из dictB
                dictA[key] = valueB
        else:
            # Если ключа нет в dictA, добавляем его
            dictA[key] = valueB
    
    return dictA

def test_combine_dicts_basic():
    dictA = {"a": 1, "b": 2}
    dictB = {"c": 3, "d": 4}
    result = combine_dicts(dictA, dictB)
    assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

def test_combine_dicts_overwrite():
    dictA = {"a": 1, "b": 2}
    dictB = {"b": 20, "c": 3}
    result = combine_dicts(dictA, dictB)
    assert result == {"a": 1, "b": 20, "c": 3}

def test_combine_dicts_nested():
    dictA = {"a": 1, "b": {"c": 1, "f": 4}}
    dictB = {"d": 1, "b": {"c": 2, "e": 3}}
    result = combine_dicts(dictA, dictB)
    assert result == {"a": 1, "b": {"c": 2, "f": 4, "e": 3}, "d": 1}

def test_combine_dicts_deep_nested():
    dictA = {"level1": {"level2": {"level3": {"a": 1, "b": 2}}}}
    dictB = {"level1": {"level2": {"level3": {"b": 20, "c": 3}}}}
    result = combine_dicts(dictA, dictB)
    expected = {"level1": {"level2": {"level3": {"a": 1, "b": 20, "c": 3}}}}
    assert result == expected

def test_combine_dicts_mixed_types():
    dictA = {"a": 1, "b": "hello", "c": [1, 2, 3]}
    dictB = {"b": "world", "c": [4, 5], "d": {"nested": "value"}}
    result = combine_dicts(dictA, dictB)
    expected = {"a": 1, "b": "world", "c": [4, 5], "d": {"nested": "value"}}
    assert result == expected

def test_combine_dicts_empty_dicts():
    dictA = {}
    dictB = {}
    result = combine_dicts(dictA, dictB)
    assert result == {}

def test_combine_dicts_first_empty():
    dictA = {}
    dictB = {"a": 1, "b": 2}
    result = combine_dicts(dictA, dictB)
    assert result == {"a": 1, "b": 2}

def test_combine_dicts_second_empty():
    dictA = {"a": 1, "b": 2}
    dictB = {}
    result = combine_dicts(dictA, dictB)
    assert result == {"a": 1, "b": 2}

def test_combine_dicts_nested_overwrite_with_non_dict():
    dictA = {"a": {"b": 1, "c": 2}}
    dictB = {"a": "not_a_dict"}
    result = combine_dicts(dictA, dictB)
    assert result == {"a": "not_a_dict"}

def test_combine_dicts_non_dict_overwrite_with_dict():
    dictA = {"a": "not_a_dict"}
    dictB = {"a": {"b": 1, "c": 2}}
    result = combine_dicts(dictA, dictB)
    assert result == {"a": {"b": 1, "c": 2}}

def test_combine_dicts_multiple_nested_levels():
    dictA = {"l1": {"l2a": {"l3a": 1}, "l2b": 2}}
    dictB = {"l1": {"l2a": {"l3b": 3}, "l2c": 4}}
    result = combine_dicts(dictA, dictB)
    expected = {"l1": {"l2a": {"l3a": 1, "l3b": 3}, "l2b": 2, "l2c": 4}}
    assert result == expected

def manual_test():
    dictA = {"a": 1, "b": {"c": 1, "f": 4}}
    dictB = {"d": 1, "b": {"c": 2, "e": 3}}

    print("The first dict (dictA): ", dictA)
    print("The second dict: ", dictB)

    result = combine_dicts(dictA, dictB)

    print("After merge: ", result)

def demo_test():
    test_cases = [
        ({"a": 1, "b": 2}, {"c": 3, "d": 4}),
        ({"a": 1, "b": 2}, {"b": 20, "c": 3}),
        ({"a": 1, "b": {"c": 1, "f": 4}}, {"d": 1, "b": {"c": 2, "e": 3}}),
        ({}, {"a": 1, "b": 2}),
        ({"a": 1, "b": 2}, {})
    ]
    
    print("Демонстрация работы функции combine_dicts:")
    print("=" * 20)
    
    for i, (dictA, dictB) in enumerate(test_cases, 1):
        # Создаем копии для демонстрации
        dictA_copy = dictA.copy()
        if isinstance(dictA, dict):
            # Глубокая копия для вложенных словарей
            import copy
            dictA_copy = copy.deepcopy(dictA)
        
        result = combine_dicts(dictA_copy, dictB)
        print(f"Тест {i}:")
        print(f"  dictA: {dictA}")
        print(f"  dictB: {dictB}")
        print(f"  Результат: {result}")
        print("-" * 40)


if __name__ == "__main__":
    demo_test()
    
    # Ручное тестирование 
    # manual_test()
    
    print("\nДля запуска автоматических тестов выполните в терминале:")
    print("pytest task5.py -v")