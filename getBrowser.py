import re
from winreg import HKEY_CURRENT_USER, HKEY_CLASSES_ROOT, OpenKey, QueryValueEx

def get_browser_name() -> str:
    register_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
    with OpenKey(HKEY_CURRENT_USER, register_path) as key:
        return str(QueryValueEx(key, "ProgId")[0])

def format_cmd(s:str) -> str:
    exe_path = re.sub(r"(^.+exe)(.*)", r"\1", s)
    return exe_path.replace('"', "")

def get_exe_path(name:str) -> str:
    register_path = r'{}\shell\open\command'.format(name)
    fullpath = ""
    with OpenKey(HKEY_CLASSES_ROOT, register_path) as key:
        cmd = str(QueryValueEx(key, "")[0])
        fullpath = format_cmd(cmd)
    return fullpath

def main():
    prog_name = get_browser_name()
    return get_exe_path(prog_name)



def getChromiumParams():
    """
    {
        "MicrosoftEdge": "msedge.exe",
        "GoogleChrome": "chrome.exe",
        "OperaGX": "OperaGX\\Launcher.exe"
    }
    """
    defaultBrowserPath = get_exe_path(get_browser_name())
    
    envPath = "LOCALAPPDATA"
    profileAppention = "Default"
    path = ""
    company = ""

    if defaultBrowserPath.endswith("msedge.exe"):
        path = "Microsoft\\Edge\\User Data"
        company = "MicrosoftEdge"
        #return ("LOCALAPPDATA", "Default", "Microsoft\\Edge\\User Data", "MicrosoftEdge")
    elif defaultBrowserPath.endswith("chrome.exe"):
        path = "Google\\Chrome\\User Data"
        company = "GoogleChrome"
        #return ("LOCALAPPDATA", "Default", "Google\\Chrome\\User Data", "GoogleChrome")
    elif defaultBrowserPath.endswith("Opera GX\\Launcher.exe"):
        envPath = "APPDATA"
        profileAppention = ""
        path = "Opera Software\\Opera GX Stable"
        company = "OperaGX"
        #return ("APPDATA", "", "Opera Software\\Opera GX Stable", "OperaGX")
    
    #print(company)
    return envPath, profileAppention, path, company

if __name__ == '__main__':
    print(main())