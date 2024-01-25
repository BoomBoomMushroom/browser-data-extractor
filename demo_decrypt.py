import json
import os
import sys

import fernetCryptography

if len(sys.argv) < 2: exit()

filePath = sys.argv[1]
b64Key = fernetCryptography.intToB64Key( os.path.getmtime(filePath) )

with open(filePath, "rb") as f:
    bytes = f.readlines()
    
    username = fernetCryptography.decryptString(b64Key, bytes[0]).decode()
    history = json.loads(fernetCryptography.decryptString(b64Key, bytes[1]))
    topWebsites = json.loads(fernetCryptography.decryptString(b64Key, bytes[2]))
    passwordsAndFreq = json.loads(fernetCryptography.decryptString(b64Key, bytes[3]))

#print(username)
#print(history)
#print(topWebsites)
#print(passwordsAndFreq)