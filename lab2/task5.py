word1 = input("enter the first word: ").lower().replace(" ", "")
word2 = input("enter the second word: ").lower().replace(" ", "")

if sorted(word1) == sorted(word2):
    print("it is anagrams!")
else:
    print("it is not anagrams")