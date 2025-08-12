import random
import string


def generate_random_string(length):
    characters = string.digits + string.punctuation + string.ascii_letters
    return ''.join(random.choices(characters, k=length))

ask = input("would you like to generate a secure password? y/n: ")
if ask == "y":
    length = int(input("Enter the length of the random string: "))
    random_string = generate_random_string(length)


    print(f"Generated Random String: {random_string}")
    with open("passwords.txt", "w") as file:
        file.write(random_string)

    print("The random string has been saved to passwords.txt")
else:
    exit()
