import os
import hashlib
import getpass
from cryptography.fernet import Fernet

KEY_FILE = 'key.key'
PASS_FILE = 'passwords.txt'
MASTER_FILE = 'master.txt'

if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)


def load_key():
    with open(KEY_FILE, "rb") as file:
        return file.read()

def addpass():
    email = input("Enter email/username: ")
    platform = input("Enter platform/website: ")
    pw = getpass.getpass(prompt='Password: ', stream=None)

    key = load_key()
    cipher = Fernet(key)
    encrypted_pw = cipher.encrypt(pw.encode())

    with open(PASS_FILE, "a") as file:
        file.write(f"{platform}|{email}|{encrypted_pw.decode()}\n")

    print("Password saved.")

def clearpass():
    check = input('are you SURE you want to clear all passwords???\ny/n: ')
    if check == 'y':
        with open(PASS_FILE, "w") as file:
            pass
        print('passwords successfully cleared!\n')
    if check == 'n':
        pass
def openpass():
    key = load_key()
    cipher = Fernet(key)

    if not os.path.exists(PASS_FILE) or os.path.getsize(PASS_FILE) == 0:
        print("No passwords stored.")
        return

    with open(PASS_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                platform, email, encrypted_pw = line.split("|")
                decrypted_pw = cipher.decrypt(encrypted_pw.encode()).decode()
                print(f"Platform: {platform}\nEmail: {email}\nPassword: {decrypted_pw}\n\n")
            except Exception as e:
                print(f"Error decrypting entry: {e}")


if not os.path.exists(MASTER_FILE) or os.path.getsize(MASTER_FILE) == 0:
    print('No master password found. Please set a new master password.')
    enter = getpass.getpass(prompt='Set master password: ', stream=None)
    hashs = hashlib.sha256()
    hashs.update(enter.encode())
    hashedpass = hashs.hexdigest()
    with open(MASTER_FILE, 'w') as file:
        file.write(hashedpass)
    print('Master password set. Please restart the program.')
    with open(PASS_FILE, "w") as file:
        pass
    exit()

enter = getpass.getpass(prompt='Enter master password: ', stream=None)
hashs = hashlib.sha256()
hashs.update(enter.encode())
hashedpass = hashs.hexdigest()

with open(MASTER_FILE, 'r') as file:
    masterkey = file.read()

if hashedpass != masterkey:
    print('Wrong password')
    exit()

while True:
    menu = input("""

1. add a password
2. clear password list
3. open passwords
4. delete stored master password and encryption key
5. exit
: """)
    if menu == "1":
        addpass()
    elif menu == "2":
        clearpass()
    elif menu == "3":
        openpass()
    elif menu == "4":
        confirm = input('are you SURE you want to do this? it will delete your password and encryption key and you will NO LONGER be able to access your passwords.\ni reccomend clearing passwords before continuing.\ncontinue? y/n: ')
        if confirm == 'y':
            os.remove(MASTER_FILE)
            os.remove(KEY_FILE) 
            print('cleared')
        if confirm == 'n':
            exit()
    elif menu == "5":
        exit()
    else:
        print('Enter a valid input!')