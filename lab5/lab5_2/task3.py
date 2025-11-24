def is_palindrome(input_string):
    cleaned_text = input_string.replace(" ", "").lower()
    
    return cleaned_text == cleaned_text[::-1]

def test_is_palindrome_basic():
    assert is_palindrome("radar") == True
    assert is_palindrome("level") == True
    assert is_palindrome("madam") == True

def test_is_palindrome_not_palindrome():
    assert is_palindrome("hello") == False
    assert is_palindrome("world") == False
    assert is_palindrome("python") == False

def test_is_palindrome_with_spaces():
    assert is_palindrome("a man a plan a canal panama") == True
    assert is_palindrome("was it a car or a cat i saw") == True
    assert is_palindrome("never odd or even") == True

def test_is_palindrome_case_sensitivity():
    assert is_palindrome("Racecar") == True
    assert is_palindrome("MaDaM") == True
    assert is_palindrome("LeVeL") == True

def test_is_palindrome_numbers():
    assert is_palindrome("12321") == True
    assert is_palindrome("123321") == True
    assert is_palindrome("12345") == False

def test_is_palindrome_single_character():
    assert is_palindrome("a") == True
    assert is_palindrome("1") == True
    assert is_palindrome(" ") == True  

def test_is_palindrome_empty_string():
    assert is_palindrome("") == True

def test_is_palindrome_mixed_alphanumeric():
    assert is_palindrome("a1b2b1a") == True
    assert is_palindrome("1a2b3b2a1") == True
    assert is_palindrome("1a2b3c") == False

def test_is_palindrome_phrases():
    assert is_palindrome("A Santa at NASA") == True
    assert is_palindrome("Mr Owl ate my metal worm") == True

def manual_test():
    testString = input("enter a string: ")
    
    if is_palindrome(testString):
        print("it is a palindrom!")
    else:
        print("it is not a palindrom")

def demo_test():
    test_cases = [
        "radar",
        "hello",
        "A man a plan a canal Panama",
        "12321",
        "Racecar",
        "was it a car or a cat i saw",
        "python"
    ]
    
    print("Демонстрация работы функции is_palindrome:")
    print("=" * 20)
    
    for text in test_cases:
        result = is_palindrome(text)
        status = "✓ ПАЛИНДРОМ" if result else "✗ НЕ ПАЛИНДРОМ"
        print(f"'{text}' -> {status}")
    
    print("=" * 20)

if __name__ == "__main__":
    demo_test()
    
    # Ручное тестирование 
    # manual_test()
    
    print("\nДля запуска автоматических тестов выполните в терминале:")
    print("pytest task3.py -v")