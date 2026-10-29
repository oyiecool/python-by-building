while True:
    text = input("Enter a number from 1 to 10: ")
    if text.isdigit() and 1 <= int(text) <= 10:
        number = int(text)
        break
    print("Invalid, try again.")
print("You chose", number)
