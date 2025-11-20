def uniqueElements(testList):
    elementsRow = {}
    
    def countElements(lst):
        for item in lst:
            if isinstance(item, list):
                countElements(item)  
            else:
                if item in elementsRow:
                    elementsRow[item] += 1
                else:
                    elementsRow[item] = 1
    
    def collectUnique(lst):
        result = []
        for item in lst:
            if isinstance(item, list):
                listOfUnique = collectUnique(item)
                for elem in listOfUnique:
                    if elem not in result:
                        result.append(elem)
            else:
                if elementsRow[item] == 1 and item not in result:
                    result.append(item)
        return result
    
    countElements(testList)
    
    return collectUnique(testList)

listA = [1, 2, 3, [4, 3, 1], 5, [6, [7, [10], 8, [9, 2, 3]]]]

print("Начальный список:", listA)

unique_result = uniqueElements(listA)

print("\nЭлементы, встречающиеся только один раз:", unique_result)

