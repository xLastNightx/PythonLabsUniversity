theFirstRow = set(map(int, input("enter a row of numbers for the first stage through space: ").split()))
theSecondRow = set(map(int, input("enter a row of numbers for the second stage through space: ").split()))

common = theFirstRow.intersection(theSecondRow)
onlyInTheFirst = theFirstRow.difference(theSecondRow)
onlyinTheSecond = theSecondRow.difference(theFirstRow)
uniqToEach = theFirstRow.symmetric_difference(theSecondRow)

if common:
    print("common numbers: ", common)
else: 
    print("there is no common numbers")

if onlyInTheFirst:
    print("numbers, that're in the first, but no in the second: ", onlyInTheFirst)
else: 
    print("there is no numbers that're in the first, but no in the second")

if onlyinTheSecond:
    print("numbers, that're in the second, but no in the first: ", onlyinTheSecond)
else: 
    print("there is no numbers that're in the second, but no in the first")

if uniqToEach:
    print("unique numbers for each other: ", uniqToEach)
else: 
    print("there is no unique numbers")