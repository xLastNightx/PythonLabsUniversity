import random

# Загадываем число
number = random.randint(1, 100)
print("Угадай число от 1 до 100!")

# Игровой процесс
guess = 0
while guess != number:
    guess = int(input("Твоя догадка: "))
    
    if guess < number:
        print("Загаданное число БОЛЬШЕ")
    elif guess > number:
        print("Загаданное число МЕНЬШЕ")
    else:
        print("Ты угадал!")