text = input("enter a row: ")

compressed = ""
iterator = 0

while iterator < len(text):
    current_char = text[iterator]
    amountOfLetter = 1
    
    while iterator + amountOfLetter < len(text) and text[iterator + amountOfLetter] == current_char:
        amountOfLetter += 1

    compressed += current_char + str(amountOfLetter)
    iterator += amountOfLetter

print("compressed row: ", compressed)