def merge_sorted_list(list1, list2):
    result = []
    iterator1 = 0  
    iterator2 = 0 
    
    while iterator1 < len(list1) and iterator2 < len(list2):
        if list1[iterator1] <= list2[iterator2]:
            result.append(list1[iterator1])
            iterator1 += 1
        else:
            result.append(list2[iterator2])
            iterator2 += 1
    
    while iterator1 < len(list1):
        result.append(list1[iterator1])
        iterator1 += 1
    
    while iterator2 < len(list2):
        result.append(list2[iterator2])
        iterator2 += 1
    
    return result

listA = [1, 3, 5, 7]
listB = [2, 4, 6, 8, 9]

print("Первый список:", listA)

print("Второй список:", listB)

merged = merge_sorted_list(listA, listB)

print("Объединенный список:", merged)