number = int(input("enter a number: "))
if number % 7 == 0:
    print("it is a magic number!")
else:
    # если делать только из if - то вот:

    # num = abs(number)  # работаем с модулем числа
    # sum_digits = 0
    
    # if num >= 1000:
    #     sum_digits += num // 1000
    #     num = num % 1000
    
    # if num >= 100:
    #     sum_digits += num // 100
    #     num = num % 100
    
    # if num >= 10:
    #     sum_digits += num // 10
    #     num = num % 10
    
    # sum_digits += num  
    
    # print(f"Сумма цифр: {sum_digits}")

#если делать через цикл (вы уточняли, что в одном задании необходимо), то вот, и оно подходит для всех чисел:
    lengthOfNumber = len(str(number))
    sum = 0
    while lengthOfNumber > 0:
        sum += number % 10
        number //= 10
        lengthOfNumber -= 1
    print ("sum of each number: ", sum)
