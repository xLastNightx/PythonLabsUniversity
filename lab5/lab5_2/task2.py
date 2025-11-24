def find_unique_words(text):
    # Очистка текста от знаков препинания и приведение к нижнему регистру
    cleanedWordsTuple = tuple(text.replace(",", "").replace(".", "").replace(";", "").replace(":", "").replace("?", "").replace("!", "").replace("(", "").replace(")", "").lower().split())

    uniqWords = 0
    frequencyOfWord = {}
    iterator = 0

    # Подсчет частот слов
    while iterator < len(cleanedWordsTuple):
        word = cleanedWordsTuple[iterator]
        if word in frequencyOfWord:
            frequencyOfWord[word] += 1
        else:
            frequencyOfWord[word] = 1
        iterator += 1

    # Подсчет уникальных слов
    for word in frequencyOfWord:
        if frequencyOfWord[word] == 1:  
            uniqWords += 1

    return uniqWords, frequencyOfWord

def test_find_unique_words_basic():
    uniq_count, freq_dict = find_unique_words("hello world hello test")
    assert uniq_count == 2  
    assert freq_dict == {'hello': 2, 'world': 1, 'test': 1}

def test_find_unique_words_all_unique():
    uniq_count, freq_dict = find_unique_words("apple banana cherry")
    assert uniq_count == 3
    assert freq_dict == {'apple': 1, 'banana': 1, 'cherry': 1}

def test_find_unique_words_all_duplicates():
    uniq_count, freq_dict = find_unique_words("word word word")
    assert uniq_count == 0
    assert freq_dict == {'word': 3}

def test_find_unique_words_empty_text():
    uniq_count, freq_dict = find_unique_words("")
    assert uniq_count == 0
    assert freq_dict == {}

def test_find_unique_words_with_punctuation():
    uniq_count, freq_dict = find_unique_words("Hello, world! Hello? Test.")
    assert uniq_count == 2 
    assert freq_dict == {'hello': 2, 'world': 1, 'test': 1}

def test_find_unique_words_case_sensitivity():
    uniq_count, freq_dict = find_unique_words("Hello hello HELLO")
    assert uniq_count == 0 
    assert freq_dict == {'hello': 3}

def test_find_unique_words_single_word():
    uniq_count, freq_dict = find_unique_words("test")
    assert uniq_count == 1
    assert freq_dict == {'test': 1}

def test_find_unique_words_mixed_punctuation():
    uniq_count, freq_dict = find_unique_words("Hello (world); hello: test? yes!")
    assert uniq_count == 3 
    assert freq_dict == {'hello': 2, 'world': 1, 'test': 1, 'yes': 1}


# Функция для ручного тестирования 
def manual_test():
    text = input("enter your text: ")
    uniq_count, frequencyOfWord = find_unique_words(text)
    
    print("this is how many times we have met different words: ", frequencyOfWord)
    print("how many unique words: ", uniq_count)


# Функция для демонстрации работы
def demo_test():
    test_cases = [
        "hello world hello test",
        "apple banana cherry",
        "word word word",
        "Hello, world! Hello? Test.",
        "test"
    ]
    
    print("Демонстрация работы функции find_unique_words:\n")
    
    for text in test_cases:
        uniq_count, freq_dict = find_unique_words(text)
        print(f"Текст: '{text}'")
        print(f"Уникальных слов: {uniq_count}")
        print(f"Словарь частот: {freq_dict}")
        print("-" * 60)


if __name__ == "__main__":
    demo_test()
    
    # Ручное тестирование 
    # manual_test()
    
    print("\nДля запуска автоматических тестов выполните в терминале:")
    print("pytest task2.py -v")