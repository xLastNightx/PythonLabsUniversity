firstNumber = int(input("enter 1 number: "))

secondNumber = int(input("enter 2 number: "))

print(f"sum: {firstNumber} + {secondNumber} = {firstNumber + secondNumber}")
print(f"difference: {firstNumber} - {secondNumber} = {firstNumber - secondNumber}")
print(f"product: {firstNumber} * {secondNumber} = {firstNumber * secondNumber}")

# Проверка деления на ноль
if secondNumber != 0:
    print(f"quotient: {firstNumber} ÷ {secondNumber} = {firstNumber / secondNumber}")
    print(f"remainder from division: {firstNumber} % {secondNumber} = {firstNumber % secondNumber}")
else:
    print("you can't divid on 0!")

# Возведение в степень
print(f"power: {firstNumber} ^ {secondNumber} = {firstNumber ** secondNumber}")
