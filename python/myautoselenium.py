from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import time

email_username = "1025096440@qq.com"
email_passwd = "Meihaode1*tian"

browser = webdriver.Firefox(
    executable_path="/home/healer/Public/code/python/geckoDriver/geckodriver")

browser.get("https://dev.azure.com/1025096440/")

email = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.ID, "i0116")))
email.send_keys(email_username)
browser.find_element_by_id("idSIButton9").click()

time.sleep(6)
passwd = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@name='passwd']")))
passwd.send_keys(email_passwd)
browser.find_element_by_xpath("//input[@type='submit']").click()

time.sleep(2)
browser.find_element_by_xpath("//input[@type='checkbox']").click()
browser.find_element_by_xpath("//input[@type='submit']").click()
# browser.quit()

time.sleep(8)
collect = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located(
        (By.XPATH,
         "//div[@class='top-row flex-row flex-noshrink flex-grow']")))
collect.click()
#browser.find_element_by_xpath(
#    "//div[@class='top-row flex-row flex-noshrink flex-grow']").click()

time.sleep(8)
info = browser.find_element_by_xpath("//div[@class='region-statsSection']")
print("finish...")
print(info)
lines1 = info.find_element_by_xpath("//div[@class='text fontSize']")
# lines = info.find_element_by_xpath('//div[@class="text*"]')
print("lines1:", lines1)
# print("lines:", lines)
# lines.get_attribute()
