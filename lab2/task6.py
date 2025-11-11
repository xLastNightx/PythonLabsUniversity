listOfWords = input("enter your list of some word through space: ")
cleanedList = listOfWords.split()

uniqList = []
for item in cleanedList:
    if item not in uniqList:
        uniqList.append(item)

print("Список без дубликатов: ", uniqList)