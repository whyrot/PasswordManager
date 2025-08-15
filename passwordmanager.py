import os
import hashlib
import getpass
from cryptography.fernet import Fernet
import base64
import string
import random


KEY_FILE = 'key.key'
PASS_FILE = 'passwords.txt'
MASTER_FILE = 'master.txt'

if not os.path.exists(MASTER_FILE) or os.path.getsize(MASTER_FILE) == 0:
    enter = getpass.getpass(prompt='Set master password: ', stream=None)
    hashs = hashlib.sha256()
    hashs.update(enter.encode())
    hashedpass = hashs.hexdigest()
    with open(MASTER_FILE, 'w') as file:
        file.write(hashedpass)
    key = Fernet.generate_key()
    cipher = Fernet(base64.urlsafe_b64encode(hashlib.sha256(enter.encode()).digest()))
    encrypted_key = cipher.encrypt(key)
    with open(KEY_FILE, 'wb') as file:
        file.write(encrypted_key)
    with open(PASS_FILE, "w") as file:
        pass
    print('Master password set. Please restart the program.')
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

cipher = Fernet(base64.urlsafe_b64encode(hashlib.sha256(enter.encode()).digest()))
with open(KEY_FILE, 'rb') as file:
    key = cipher.decrypt(file.read())

fernet = Fernet(key)

def passwordgen():
    length = int(input('enter length of the password you would like to generate: '))
    disallowed = set(["'", '"', '\\', '`', '<', '>', '/', '-', '_'])
    punctuation = string.punctuation
    allowed_punctuation = ''.join(ch for ch in punctuation if ch not in disallowed)
    characters = string.ascii_letters + string.digits  + allowed_punctuation
    securepass = ''.join(random.choice(characters) for _ in range(length))
    print(f'your securely generated password is: {securepass}')
def addpass():
    email = input("Enter email/username: ")
    platform = input("Enter platform/website: ")
    pw = getpass.getpass(prompt='Password: ', stream=None)
    encrypted_pw = fernet.encrypt(pw.encode())
    with open(PASS_FILE, "a") as file:
        file.write(f"{platform}|{email}|{encrypted_pw.decode()}\n")
    print("Password saved.")

def clearpass():
    check = input('are you SURE you want to clear all passwords???\ny/n: ')
    if check == 'y':
        with open(PASS_FILE, "w") as file:
            pass
        print('passwords successfully cleared!\n')

def openpass():
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
                decrypted_pw = fernet.decrypt(encrypted_pw.encode()).decode()
                print(f"Platform: {platform}\nEmail: {email}\nPassword: {decrypted_pw}\n\n")
            except:
                pass

while True:
    menu = input("""
1. add a password
2. clear password list
3. open passwords
4. delete stored master password and encryption key
5. generate a secure password
6. exit
                 
 """)
    if menu == "1":
        addpass()
    elif menu == "2":
        clearpass()
    elif menu == "3":
        openpass()
    elif menu == "4":
        confirm = input('THIS CLEARS PASSWORDS\nare you SURE you want to do this? it will delete your password and encryption key and you will NO LONGER be able to access your passwords.\ncontinue? y/n: ')
        if confirm == 'y':
            os.remove(MASTER_FILE)
            os.remove(KEY_FILE)
            print('cleared')
        if confirm == 'n':
            exit()
    elif menu == "5":
        passwordgen()
    elif menu == "6":
        exit()
    else:
        print('Enter a valid input!')
