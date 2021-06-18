from selenium import webdriver
from time import sleep

option = webdriver.ChromeOptions()
option.binary_location = r"C:\Program Files (x86)\ChromePortable\App\Chrome\chrome.exe"
wd = webdriver.Chrome(r'D:\chromedriver.exe', options=option)
wd.maximize_window()
wd.get("http://10.20.2.73:8082/")
wd.find_element_by_name("username").send_keys("zengming")
wd.find_element_by_name("password").send_keys("123456\n")
sleep(4)
wd.switch_to.frame(wd.find_elements_by_tag_name("iframe")[0])
element = wd.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/table/tbody/tr[1]/td[3]/div/div[1]/span/span/a")
element.click()
sleep(4)
element = wd.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/table/tbody/tr[2]/td[7]/div/div[1]/a/div/div/span")
element.click()
sleep(4)
wd.switch_to.default_content()
wd.switch_to.frame(wd.find_elements_by_tag_name("iframe")[1])
wd.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div/span[5]/select/option[4]').click()
sleep(4)
element = wd.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[4]/div[2]/table/tbody/tr[1]/td/div/a[2]")
element.click()
# sleep(2)
# wd.switch_to.frame(wd.find_elements_by_tag_name("iframe")[0])
# element = wd.find_element_by_xpath('//*[@id="footnote"]')
# element.send_keys('')
# wd.find_element_by_xpath("/html/body/div/div[2]/div/button").click()


