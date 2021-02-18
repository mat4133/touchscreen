from selenium import webdriver

driver_path = 'C:\Windows\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get('https://facebook.com')
email = driver.find_element_by_id('email')
email.send_keys('pshbutterfield@gmail.com')
password = driver.find_element_by_id('pass')
password.send_keys('*******')
cookies = driver.find_element_by_class_name('_42ft _4jy0 _9o-t _4jy3 _4jy1 selected _51sy')
cookies.click()
login = driver.find_element_by_name('login')
print(login)
login.click()

