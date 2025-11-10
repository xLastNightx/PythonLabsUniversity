# помещаем в структуру (создаем) для примера несколько значений и потом находим в этой структуре делитель какого-то числа 
# (пользователь вводит число и находим делитель 6 и мы выводим 1, 2, 3, 6) если оно уже есть в структуре, если нет, то сначала добавляем, а потом выводим
# структура в структуре
deliteli = {"1":2, "2":3, "3":1, "4":4, "5":5}
sortedDeliteli = sorted(deliteli)
iter = 0
#print(iter == (len(sortedDeliteli) - 1))
#print((int(numb) / int(iter) >= 2))

number = input("Введите число и программа выдаст его делители: ")

def foundDeliteli(numb):

    for iter in sortedDeliteli:
        if  int(numb) / int(iter) < 2:
            sortedDeliteli.append(str(numb))
            print("делитель ", numb)

            break

        elif iter == (len(sortedDeliteli) - 1) and (int(numb) / int(iter) >= 2):
            print("делитель ", iter)

            while int(numb) / int(iter) >= 2:
                iter += 1
                if int(numb) % int(iter) == 0: 
                    print("делитель ", iter)

        elif numb == iter: break

        else: 
            if int(numb) % int(iter) == 0: 
                print("делитель ", iter)

    print(sortedDeliteli)  

foundDeliteli(int(number))

choice = print("будет еще какое-то число? \n если да - введите 1, если нет - введите 0")

if choice == 1:
    number = input("Введите число и программа выдаст его делители: ")
    foundDeliteli(int(number))
elif choice == 0: print("Удачи!")
else: print("не правильное значение")