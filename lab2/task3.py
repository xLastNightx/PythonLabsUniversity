import datetime

def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now()
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Формируем строку для записи
            log_line = f"{time_str} - {func.__name__}"
            
            if args:
                log_line += f" args: {args}"
            if kwargs:
                log_line += f" kwargs: {kwargs}"
            
            # Записываем в файл
            with open(filename, 'a', encoding='utf-8') as funcsh:
                funcsh.write(log_line + '\n')
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_calls("log.txt")
def add(a, b):
    return a + b

@log_calls("log.txt") 
def greet(name, age=None):
    if age:
        return f"Hello {name}, age {age}"
    else:
        return f"Hello {name}"

if __name__ == "__main__":
    
    result1 = add(5, 3)
    print(f"add(5, 3) = {result1}")
    
    result2 = greet("Alice")
    print(f"greet('Alice') = {result2}")
    
    result3 = greet("Bob", age=25)
    print(f"greet('Bob', age=25) = {result3}")
    