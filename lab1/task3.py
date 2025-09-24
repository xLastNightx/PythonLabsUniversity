testingString = input("your password: ")
if len(testingString) < 16:
    print("too weak password")
else:
    if testingString.isalpha():
        print("you have to use numbers")
    else:
        if testingString.isdigit():
            print("you have to use letters")    
        else:
            print("well done!")