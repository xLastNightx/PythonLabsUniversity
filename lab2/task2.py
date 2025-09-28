rowOfNumbers = input("enter row of numbers through space: ")
massOfNumbers = []

for rowOfNumbers in rowOfNumbers.split():
    try:
        # Пробуем преобразовать в целое число
        massOfNumbers.append(int(rowOfNumbers))
    except ValueError:
        try:
            # Если не получается, пробуем преобразовать в float
            massOfNumbers.append(float(rowOfNumbers))
        except ValueError:
            print(f"⚠️  Пропущено некорректное значение: '{rowOfNumbers}'")

iterator = 0
uniqNumbs = []
nonUniqNumbs = []
even = []
odd = []
negative = []
floatNumbs = []
frequencyOfNumbs = {}
sumOfMultiplesOf5 = 0

while iterator < len(massOfNumbers):
    numb = massOfNumbers[iterator]
    if numb in frequencyOfNumbs:
        frequencyOfNumbs[numb] += 1
    else:
        frequencyOfNumbs[numb] = 1
    iterator += 1

for numb in frequencyOfNumbs:
    if frequencyOfNumbs[numb] == 1:  
        uniqNumbs.append(numb)
    else:
        nonUniqNumbs.append(numb)

for numb in massOfNumbers:
    if isinstance(numb, int) or (isinstance(numb, float) and numb.is_integer()): 
        # Преобразуем к целому для проверки четности
        int_numb = int(numb)
        if int_numb % 2 == 0:
            even.append(numb)
        else:
            odd.append(numb)

for numb in massOfNumbers:
    if numb < 0:
        negative.append(numb)

for numb in massOfNumbers:
    if isinstance(numb, float):
        floatNumbs.append(numb)

for numb in massOfNumbers:
    if numb % 5 == 0:   
        sumOfMultiplesOf5 += numb

print("massive of numbers: ", massOfNumbers)
print("unique numbers: ", uniqNumbs)
print("non-unique numbers: ", nonUniqNumbs)
print("even numbers: ", even)
print("odd numbers: ", odd)
print("negative numbers: ", negative)
print("float numbers: ", floatNumbs)
print("numbers that's multiples of 5: ", sumOfMultiplesOf5)
print("the biggest number: ", max(massOfNumbers))
print("the smolest number: ", min(massOfNumbers))