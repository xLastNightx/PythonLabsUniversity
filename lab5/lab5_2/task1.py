def count_words(sentence):
    if not sentence or sentence.isspace():
        return 0
    
    words = sentence.split()
    return len(words)


# Тесты
def test_basic_sentence():
    assert count_words("Hello world this is a test") == 6

def test_empty_string():
    assert count_words("") == 0

def test_only_spaces():
    assert count_words("     ") == 0

def test_single_word():
    assert count_words("Hello") == 1

def test_multiple_spaces():
    assert count_words("Hello    world   test") == 3

def test_start_end_spaces():
    assert count_words("   Hello world   ") == 2

def test_punctuation():
    assert count_words("Hello, world! How are you?") == 5

def test_tabs_and_newlines():
    assert count_words("Hello\tworld\nhow\tare\tyou") == 5

# Дополнительно: функция для ручного тестирования
def manual_test():
    test_cases = [
        "Hello world",
        "",
        "   ",
        "Single",
        "Multiple   spaces   here",
        "   Leading and trailing   ",
        "Hello, world! Test."
    ]
    
    print("Ручное тестирование функции count_words:")
    print("_" * 20)
    
    for test in test_cases:
        result = count_words(test)
        print(f"'{test}' -> {result} слов")
    
    print("_" * 20)


if __name__ == "__main__":
    manual_test()
    
    print("\nДля запуска автоматических тестов выполните в терминале:")
    print("pytest task1.py -v")