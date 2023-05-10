import os
from time import sleep


def run_chrome_debug():  # run chrome on debugging mode
    chrome_path = r"C:\Program Files\Google\Chrome\Application"  # chrome.exe path
    chrome_profile = r"C:\Users\ChromeProfile"  # create a folder name ChromeProfile to dump all of debugging folders
    os.chdir(chrome_path)
    os.system("chrome.exe --remote-debugging-port=8989 --user-data-dir=" + chrome_profile)
    sleep(3)


run_chrome_debug()
