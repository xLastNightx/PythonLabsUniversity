# помещаем в структуру (создаем) для примера несколько значений и потом находим в этой структуре делитель какого-то числа 
# (пользователь вводит число и находим делитель 6 и мы выводим 1, 2, 3, 6) если оно уже есть в структуре, если нет, то сначала добавляем, а потом выводим
# структура в структуре
# numbers = {4: {"делители": [1, 2, 4]}, 6: {"делители": [1, 2, 3, 6]}, 8: {"делители": [1, 2, 4, 8]}, 10: {"делители": [1, 2, 5, 10]}
# } 
#можно и вот так (услышала, что нудно именно сгенерировать, а не создавать, поэтому дополнила)

numbers = {}
for iter in range(2, 10, 2):
    deliteli = []

    for anotherIter in range(1, iter + 1):
        if iter % anotherIter == 0:  deliteli.append(anotherIter)  
    
    numbers[iter] = {"делители": deliteli}

number = int(input("Введите целое число и программа выдаст его делители: "))

def checkForDeliteli(numb):
    if numb in numbers:
        print("Делители: ", numbers[numb]['делители'])
    else:
        deliteli = foundDeliteli(numb)
        numbers[numb] = {"делители": deliteli}
        print("Делители вашего числа: ", deliteli)

    print("Словарь сейчас:")
    for key, value in numbers.items(): print(f"{key}: {value}")

def foundDeliteli(numb):
    deliteli = []

    for iter in range(1, numb + 1):
        if numb % iter == 0:  
            deliteli.append(iter)  

    return deliteli 

checkForDeliteli(number)


def askAboutNecessity():
    choice = input("будет еще какое-то число? \n если да - введите 1, если нет - введите 0: ")

    if choice == "1":
        number = input("Введите число и программа выдаст его делители: ")
        checkForDeliteli(int(number))
        askAboutNecessity()
    elif choice == "0": print("Удачи!")
    else: print("не правильное значение")

askAboutNecessity()