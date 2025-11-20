def cache(func):
    cacheDict = {}
    
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        
        if key in cacheDict:
            print(f"Результат из кэша для {args} {kwargs}")
            return cacheDict[key]
        else:
            result = func(*args, **kwargs)
            cacheDict[key] = result
            print(f"Вычислен результат для {args} {kwargs}")
            return result
    
    return wrapper

@cache
def multiply(a, b):
    return a * b

print("Первый вызов:")
result1 = multiply(3, 4)
print(f"Результат: {result1}")

print("\nВторой вызов с теми же аргументами:")
result2 = multiply(3, 4)
print(f"Результат: {result2}")

print("\nВызов с другими аргументами:")
result3 = multiply(5, 6)
print(f"Результат: {result3}")