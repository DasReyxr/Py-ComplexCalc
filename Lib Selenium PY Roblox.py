from selenium import webdriver
import time
driver = webdriver.Chrome("chromedriver.exe")
PAGE = 'https://www.roblox.com/login'
driver.get(PAGE)

print(str(driver.get_window_size()))
print(driver.title)
time.sleep(5)
#driver.find_element_by_xpath("//*[@id="email"]").send_keys(123)
#driver.find_element_by_xpath('//*[@id="email"]').send_keys(123)
email="SmartDragonPro"
password= "0rlas.Two"
print("weitin")
#driver.find_element(by=By.ID, value= 'login-username').send_keys(email)
driver.find_element_by_id('login-username').send_keys(email)
driver.find_element_by_id('login-password').send_keys(password)

#driver.find_element(by=By.)
driver.find_element_by_id("login-button").click()
time.sleep(20)
print("eeeeeeeepa")
a=driver.find_element_by_class_name('user-name-container').text
print(f"y yo siempre {a}")
#driver.find_element_by_class_name('user-name-container').click()
#driver.find_element_by_name('//*[@id="mount_0_0_yZ"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[1]/span').click()
#driver.find_element_by_xpath('//*[@id="mount_0_0_xO"]/div/div[1]/div/div[5]/div/div[1]/div[2]').click()