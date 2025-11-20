rowOfNumbers = input("enter a row of numbers through space: ")

# применяет указанную функцию к каждому элементу итерируемого объекта (списка, кортежа и т.д.) и возвращает итератор
# map(функция, итерируемый_объект)
uniqNumbers = sorted(set(map(int, rowOfNumbers.split())))

if len(uniqNumbers) < 2:
    print("there should be more numbers, than 1")
else:
    secondLargest = uniqNumbers[-2]
    print("the second largest number is: ", secondLargest)