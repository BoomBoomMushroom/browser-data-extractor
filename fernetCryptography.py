from cryptography.fernet import Fernet
import base64
import hashlib
import sys
import os

def intToB64Key(intInput):
    key = round( intInput )
    sha256Bytes = hashlib.sha256(str(key).encode()).digest()[:32]
    b64Key = base64.urlsafe_b64encode(sha256Bytes)
    return b64Key

def encryptString(key, inputString):
    encrypter = Fernet( key )
    bytes = encrypter.encrypt(inputString.encode())
    return bytes

def decryptString(key, inputString):
    encrypter = Fernet( key )
    bytes = encrypter.decrypt(inputString)
    return bytes