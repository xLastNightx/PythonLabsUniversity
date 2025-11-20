def type_check(*types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for iterator, (arg, expectedType) in enumerate(zip(args, types)):
                if not isinstance(arg, expectedType):
                    raise TypeError(f"Аргумент {iterator} должен быть {expectedType.__name__}, получен {type(arg).__name__}")            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@type_check(int, int)
def add(a, b):
    return a + b

print("В функцию передают определенные аргументы, если они соответствуют требованиям - функция выполняется, если нет - выдает ошибку")
print("\nПравильные аргументы:")

result = add(5, 9)
print(f"add(5, 9) = ",result)

print("\nНеправильные аргументы:")
try:
    add(5, "9")
except TypeError as e:
    print(f"Ошибка: {e}")