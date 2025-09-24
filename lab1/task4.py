salary = int(input("enter amount of money: "))
amountOf100 = salary // 100
if amountOf100 > 0:
    print("amount of 100: ", amountOf100)
    salary %= 100

if salary >= 50:
    amountOf50 = 1
    print("amount of 50: ", amountOf50)
    salary -= 50

if salary >= 10:
    amountOf10 = salary // 10
    print("amount of 10: ", amountOf10)
    salary %= 10

if salary >= 5:
    amountOf5 = 1
    salary -= 5
    print("amount of 5: ", amountOf5)

if salary >= 2:
    amountOf2 = salary // 2
    salary %= 2
    print("amount of 2: ", amountOf2)

if salary == 1:
    amountOf1 = 1
    print("amount of 1: ", amountOf1)