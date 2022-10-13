import Cryptodome
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import base64
import hashlib
import os

class RSA_encryption(object):
        
    def generet_rsa_keys(self,bytes_length):
        key=RSA.generate(bytes_length)
        public=key.public_key()
        return [key.export_key('PEM'),public.export_key('PEM')]

    def import_rsa_private_key(self,private_pem):
        return RSA.import_key(private_pem)

    def import_rsa_public_key(self,public_pem):
        return RSA.import_key(public_pem).public_key()

    def rsa_encryt(self,public,data):
        if type(public)!=Cryptodome.PublicKey.RSA.RsaKey:
            public=self.import_rsa_private_key(public)
        cipher=PKCS1_OAEP.new(public)
        return base64.b64encode(cipher.encrypt(data))

    def rsa_decrypt(self,private,data):
        if type(private)!=Cryptodome.PublicKey.RSA.RsaKey:
            private=self.import_rsa_private_key(private)
        cipher=PKCS1_OAEP.new(private)
        return cipher.decrypt(base64.b64decode(data))
    
class AES_encryption(object):

    def __init__(self,key):
        self.key=key
        iv = hashlib.md5(key).digest()
        self.cipher=AES.new(key, AES.MODE_CBC, iv)

    def pad_data(self,data):
        return data + bytes(len(data)%16) + bytes([len(data)%16])

    def encrypt_data_aes(self,data):
        return base64.b64encode(self.cipher.encrypt(pad(data,AES.block_size)))

    def decrypt_data_aes(self,data):
        return unpad(self.cipher.decrypt(base64.b64decode(data)),AES.block_size)
    
    def randomKey(self):
        return os.urandom(32)
		
		
		
		