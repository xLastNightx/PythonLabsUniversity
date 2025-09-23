testString = input ("enter ip: ")

withoutDuts = testString.replace(".", "")
partsOfString = testString.split('.')

if withoutDuts.isdigit() != True:
    print("Error: it is not an ip")
else: 
    if len(partsOfString) != 4:
        print("Error: there should be 4 parts, thats devided with .")
    else:
        part1 = int(partsOfString[0])
        part2 = int(partsOfString[1])
        part3 = int(partsOfString[2])
        part4 = int(partsOfString[3])
    if (0 <= part1 <= 255 and 0 <= part2 <= 255 and 
        0 <= part3 <= 255 and 0 <= part4 <= 255):
        print("it is correct ip!")
    else:
        print("ip parts should be between 0 and 255")
