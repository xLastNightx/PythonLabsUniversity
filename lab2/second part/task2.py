def mergeDicts(dictA, dictB):

    for key, valueB in dictB.items():
        if key in dictA:
            # Если ключ есть в обоих словарях
            valueA = dictA[key]
            
            if isinstance(valueA, dict) and isinstance(valueB, dict):
                mergeDicts(valueA, valueB)
            else:
                dictA[key] = valueB
        else:
            # Если ключа нет в dictA, добавляем его
            dictA[key] = valueB

dictA = {"a": 1, "b": {"c": 1, "f": 4}}
dictB = {"d": 1, "b": {"c": 2, "e": 3}}

print("The first dict (dictA): ", dictA)
print("The second dict: ", dictB)

mergeDicts(dictA, dictB)

print("After merge: ", dictA)
