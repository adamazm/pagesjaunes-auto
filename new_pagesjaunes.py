# Important note :
# Chrome must be open in debugging mode, normally, run chrome_debug.py on other terminal, but if did not work do this:
# 1. On command prompt, go to where chrome.exe is. example : cd C:\Program Files\Google\Chrome\Application
# 2. Then run chrome.exe on debugging mode by using the following command:
#    chrome.exe --remote-debugging-port=8989 --user-data-dir="..."
#    "..." put the path for ChromeProfile


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
from random import randint
import json


def accept_cookie(driver):  # function to click accept cookie button
    try:
        cookie_btn = driver.find_element(By.ID, "didomi-notice-agree-button")
        cookie_btn.click()
    except:
        print("Cookie button is not displayed")


def go_next_page(driver):
    report1 = driver.find_element(By.ID, "pagination-next")
    report1.click()
    sleep(0.5)


def click_show_number(driver):  # function to click the show phone number button
    all_sh_nb_btn = driver.find_elements(By.CSS_SELECTOR,
                                         "button.button.btn.btn_primary.btn_full_mob.btn_tel.normal-button")
    for sh_nb_btn in all_sh_nb_btn:  # sh_nb_btn : show number button
        try:
            sh_nb_btn.click()
        except:
            pass
        sleep(randint(0, 2))
    sleep(3)


def get_info(driver):  # get name and the phone numbers in a list in pagesjaunes.fr
    all_info = []
    all_li = driver.find_elements(By.TAG_NAME, 'li')
    for li in all_li:
        name = li.find_elements(By.TAG_NAME, "h3")
        for n in name:
            info = {"Nom": n.text}
        address = li.find_elements(By.CSS_SELECTOR, "div.bi-address.small")
        for addr in address:
            info.update({"Adresse": addr.text[:-13]})
        all_number = li.find_elements(By.CSS_SELECTOR, "div.number-contact.txt_sm")
        for number in all_number:
            key = re.findall(".*:", number.text)[0][:-2]
            value = re.findall("[0-9].*", number.text)[0]
            info.update({key: value})
            all_info.append(info)

    return all_info


def main(occupation, location):
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(service=Service(r"C:\Users\adam3\Documents\ChromeProfile\chromedriver.exe"), options=opt)  # chromedriver path
    driver.get(f"https://www.pagesjaunes.fr/")
    try:
        driver.maximize_window()
    except:
        pass
    sleep(10)  # sleep to resolve captcha
    print("10 seconds had passed")
    accept_cookie(driver)
    sleep(3)
    input_occupation = driver.find_element(By.ID, "quoiqui")
    input_occupation.send_keys(occupation)
    input_location = driver.find_element(By.ID, "ou")
    input_location.send_keys(location)
    input_location.send_keys(Keys.RETURN)
    print("Searching for %s at %s ..." % (occupation, location))
    sleep(5)
    contact_info = []
    while True:
        try:
            click_show_number(driver)
            contact_info.extend(get_info(driver))
            sleep(5)
            go_next_page(driver)
            sleep(5)
        except:
            with open(f"contact_{occupation}_{location}.json", "a", encoding="utf8") as f:
                json.dump(contact_info, f, indent=4, sort_keys=True, ensure_ascii=False)
            print("Done!")
            driver.get(f"https://www.pagesjaunes.fr/")
            break


# input_metier = input('Metier : ')  # run program
# input_loc = input('Location : ')
# print("Searching for " + input_metier + " at " + input_loc + " ...")
# main(input_metier, input_loc)

all_inp = []
while True:
    input_metier = input('Metier : ')  # run program
    input_loc = input('Location : ')
    all_inp.append([input_metier, input_loc])
    more = input("un autre? (y/n): ")
    if more == "n":
        break


for inp in all_inp:
    main(inp[0], inp[1])
print("All done!")
