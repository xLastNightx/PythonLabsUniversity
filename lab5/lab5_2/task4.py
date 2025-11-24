def are_anagrams(word1, word2):
    cleaned_word1 = word1.replace(" ", "").lower()
    cleaned_word2 = word2.replace(" ", "").lower()
    
    return sorted(cleaned_word1) == sorted(cleaned_word2)

def test_are_anagrams_basic():
    assert are_anagrams("listen", "silent") == True
    assert are_anagrams("triangle", "integral") == True
    assert are_anagrams("elbow", "below") == True

def test_are_anagrams_not_anagrams():
    assert are_anagrams("hello", "world") == False
    assert are_anagrams("python", "java") == False
    assert are_anagrams("test", "best") == False

def test_are_anagrams_with_spaces():
    assert are_anagrams("school master", "the classroom") == True
    assert are_anagrams("debit card", "bad credit") == True
    assert are_anagrams("eleven plus two", "twelve plus one") == True

def test_are_anagrams_case_sensitivity():
    assert are_anagrams("Listen", "Silent") == True
    assert are_anagrams("TeSt", "TSeT") == True
    assert are_anagrams("ABC", "cba") == True

def test_are_anagrams_different_length():
    assert are_anagrams("short", "longer") == False
    assert are_anagrams("a", "ab") == False

def test_are_anagrams_empty_strings():
    assert are_anagrams("", "") == True
    assert are_anagrams("", "a") == False 

def test_are_anagrams_single_char():
    assert are_anagrams("a", "a") == True
    assert are_anagrams("a", "b") == False

def test_are_anagrams_same_word():
    assert are_anagrams("test", "test") == True
    assert are_anagrams("hello", "hello") == True

def test_are_anagrams_with_numbers():
    assert are_anagrams("123", "321") == True
    assert are_anagrams("112", "121") == True
    assert are_anagrams("123", "122") == False

def test_are_anagrams_mixed_alphanumeric():
    assert are_anagrams("a1b2", "2b1a") == True
    assert are_anagrams("test123", "123test") == True

def test_are_anagrams_duplicate_letters():
    assert are_anagrams("aabb", "abab") == True
    assert are_anagrams("aabb", "aaab") == False 

def manual_test():
    word1 = input("enter the first word: ")
    word2 = input("enter the second word: ")
    
    if are_anagrams(word1, word2):
        print("it is anagrams!")
    else:
        print("it is not anagrams")

def demo_test():
    test_cases = [
        ("listen", "silent"),
        ("hello", "world"),
        ("school master", "the classroom"),
        ("Test", "test"),
        ("123", "321"),
        ("python", "java")
    ]
    
    print("Демонстрация работы функции are_anagrams:")
    print("=" * 20)
    
    for word1, word2 in test_cases:
        result = are_anagrams(word1, word2)
        status = "✓ АНАГРАММЫ" if result else "✗ НЕ АНАГРАММЫ"
        print(f"'{word1}' vs '{word2}' -> {status}")
    
    print("=" * 20)

if __name__ == "__main__":
    demo_test()
    
    # Ручное тестирование 
    # manual_test()
    
    print("\nДля запуска автоматических тестов выполните в терминале:")
    print("pytest task4.py -v")