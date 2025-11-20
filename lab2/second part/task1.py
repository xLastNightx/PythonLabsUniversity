def flattenList(lst):

    iterator = 0
    while iterator < len(lst):
        if isinstance(lst[iterator], list):
            # Рекурсивное сглаживание
            flattenList(lst[iterator])
            
            currentElement = lst[iterator]
            lst[iterator:iterator+1] = currentElement
        else:
            iterator += 1

list1 = [1, 2, 3, [4], 5, [6, [7, [], 8, [9]]]]
print("before: ", list1)

flattenList(list1)
print("after:  ", list1)

list2 = [1, [2, [3, [4]]]]
print("before: ", list2)

flattenList(list2)
print("after:  ", list2)
    
