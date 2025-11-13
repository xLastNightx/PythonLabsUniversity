import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Время выполнения: {(end - start) * 1000:.2f} мс")
        return result
    return wrapper

@timing
def calculateSum(n):
    total = 0
    for iterator in range(1, n + 1):
        total += iterator
    return total

# Пример использования
result = calculateSum(1000000)
print("Сумма чисел: ", result)