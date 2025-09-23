testString = input ("enter a string: ")

cleaned_text = testString.replace(" ", "").lower()

if cleaned_text == cleaned_text[::-1]: # reverse
    print("it is a palindrom!")
else:
    print("it is not a palindrom")
