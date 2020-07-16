from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

email = input("Email :")
password = input("Password :")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.facebook.com/')

time.sleep(1)

#Connect to Facebook
driver.find_element_by_name("email").send_keys(email)
driver.find_element_by_name("pass").send_keys(password)
time.sleep(5)
driver.find_element_by_id("u_0_b").click()
#Open Messenger


conversation_num = input("Enter the conversation number : ")


driver.get('https://www.facebook.com/messages/t/' + conversation_num)


driver.execute_script("var scrollingInterval = setInterval(function (){document.querySelectorAll('.uiScrollableAreaWrap.scrollable')[2].scrollTop = 0;}, 500);")

time.sleep(10)

html = driver.page_source
file = open('messenger.html','w')
