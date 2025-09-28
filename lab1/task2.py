testString = input("enter a string: ")
testString = testString.lower().replace("e", "").replace("u", "").replace("y", "").replace("o", "").replace("a", "").replace("i", "")
print("without eyuioa: ", testString)