text = input("enter your text: ")

cleanedWordsTuple = tuple(text.replace(",", "").replace(".", "").replace(";", "").replace(":", "").replace("?", "").replace("!", "").replace("(", "").replace(")", "").lower().split())

uniqWords = 0
frequencyOfWord = {}
iterator = 0

while iterator < len(cleanedWordsTuple):
    word = cleanedWordsTuple[iterator]
    if word in frequencyOfWord:
        frequencyOfWord[word] += 1
    else:
        frequencyOfWord[word] = 1
    iterator += 1

for word in frequencyOfWord:
    if frequencyOfWord[word] == 1:  
        uniqWords += 1

print("this is how many times we have met different words: ", frequencyOfWord)
print("how many unique words: ", uniqWords)