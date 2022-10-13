from cryptography.fernet import Fernet
from hashlib import sha256
from base64 import b64encode
from os.path import isfile
from getpass import getpass

def genKey(password):
    return b64encode(sha256(password).digest())

def encrypt(data,key):
    fer = Fernet(key)
    return fer.encrypt(data)

def decrypt(data,key):
    fer = Fernet(key)
    return fer.decrypt(data)

def encryptFile(path,key):
    assert(isfile(path))
    data = open(path,'rb').read()
    with open(path,'wb') as f:
        f.write(encrypt(data,key))

def decryptFile(path,key):
    assert(isfile(path))
    data = open(path,'rb').read()
    with open(path,'wb') as f:
        f.write(decrypt(data,key))

def displaytext(path,key):
    return decrypt(open(path,'rb').read(),key)

def main():
    key = getpass('enter your password encryption: ').encode('utf-8')
    ask = input('to encrypt file 1\nto decrypt file 2\nto display cipher in clear 3\n: ')
    path = input('please enter path: ')
    if ask == '1':
        encryptFile(path,genKey(key))
        print('\nSuccessfully completed')
    elif ask == '2':
        decryptFile(path,genKey(key))
        print('\nSuccessfully completed')
    else:
        print(displaytext(path,genKey(key)).decode())



if __name__ == "__main__":
    main()