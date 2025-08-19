from tabnanny import check
from telnetlib import EC
from selenium import webdriver

import time

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)

def select_chat(nombre: str):
    print("searching chat")
    elements = driver.find_elements_by_id("pane-side")
    print(elements)
    for el in elements:
        if(el.text == nombre):
            el.click()
            print(f"entro al chata de {el}")
            return True
        return False
def checkQR():
    try:
        element = driver.find_element_by_tag_name('canvas')
    except: 
        return False
    return True


def WA():
    driver.get("https://web.whatsapp.com")
    time.sleep(5)

    wait = True
    while wait:
        print("waitin")
        wait = checkQR()
        time.sleep(2)
        if wait == False:
            print("yajalo")
            break
    chat=select_chat("Type 1.5")
WA()
