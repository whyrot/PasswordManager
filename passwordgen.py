import random
import string


def passgen(length):
    characters = string.digits + string.punctuation + string.ascii_letters
    return ''.join(random.choices(characters, k=length))

ask = input("would you like to generate a secure password? y/n: ")
if ask == "y":
    length = int(input("Enter the length of the random string: "))
    password = passgen(length)

    username = input("enter the username/email here: ")
    
    final = (f"{username}:{password}\n")
    print(f"{username}:{password}")
    with open("passwords.txt", "a") as file:
        file.write(final)

    print("The password and username combo has been saved to passwords.txt")
else:
    exit()
