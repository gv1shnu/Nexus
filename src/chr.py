import os
import platform


def is_chrome_installed():
    global os_name
    if os_name == "Linux":
        return os.system("dpkg -l | grep google-chrome-stable") == 0
    if os_name == "Windows":
        return os.path.exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    return False


os_name = platform.system()
chrome_installed = is_chrome_installed()
if not chrome_installed:
    print("Chrome is not installed.")
