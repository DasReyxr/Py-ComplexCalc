from selenium import webdriver
import time
import pyautogui
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.facebook.com")

time.sleep(2)
#driver.find_element_by_xpath("//*[@id="email"]").send_keys(123)
#driver.find_element_by_xpath('//*[@id="email"]').send_keys(123)
email="reyes.orlandoxv@gmail.com"
password= "#50rlaz0ne5"
driver.find_element_by_id('email').send_keys(email)
driver.find_element_by_id('pass').send_keys(password)
driver.find_element_by_name('login').click()
time.sleep(20)
pyautogui.hotkey("esc")
print("eeeeeeeepa")
time.sleep(5)
# driver["browserstack.ie.enablePopups"] = "true"

driver.find_element_by_class_name('tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41').click()
driver.find_element_by_name('New message').click()
#driver.find_element_by_name('//*[@id="mount_0_0_yZ"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[1]/span').click()
#driver.find_element_by_xpath('//*[@id="mount_0_0_xO"]/div/div[1]/div/div[5]/div/div[1]/div[2]').click()