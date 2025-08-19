from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.common.by import By
import time




options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)
driver.get("https://www.google.com")
#driver.set_window_position(2000,0)
driver.maximize_window()
time.sleep(1)

Ruta = "https://www.google.com/search?q="
driver.get(Ruta+"a")
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("aa")
#driver.find_element_by_class_name('gLFyf gsfi').send_keys("a")
#driver.get("https://www.eltiempo.es")
#WebDriverWait(driver,5).until(EC.element_to_be_clickable(By.CSS_SELECTOR,'button.didomi-components-button.didomi-button.didomi-dismiss-button.didomi-components-button--color didomi-button-highlight highlight-button')).click()
a=driver.find_element_by_id('SIvCob').text
print(f"100dolares {a}")
driver.find_element_by_xpath("//*[@id="email"]").send_keys(123)
driver.find_element_by_xpath('//*[@id="email"]').send_keys(123)
# driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("juan")

# PATH= '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]'
# #PATH = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[3]/div[1]'
# driver.find_element_by_xpath(PATH).click()
#driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').click
#driver.find_element_by_xpath('//*[@id="u_0_d_jK"]').click()
