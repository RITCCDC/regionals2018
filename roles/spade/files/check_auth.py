from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up driver, allow unverified TLS certs
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities['acceptSslCerts'] = True
driver = webdriver.Firefox(capabilities=capabilities)
driver.implicitly_wait(10)

# Get the page, wait for login form to display
driver.get('https://spade.team4.wildeagle.net')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'loginForm:username')))

# Find the login form elements
usernameInput = driver.find_element_by_name("loginForm:username")
passwordInput = driver.find_element_by_name("loginForm:password")
submitButton = driver.find_element_by_name("loginForm:loginButton")

# Fill out the login form and submit
usernameInput.send_keys("sam")
passwordInput.send_keys(Keys.SHIFT, "P")
passwordInput.send_keys("assw0rd")
submitButton.click()

# If we never return from this, login failed, and so we need to configure auth
returnCode = 0
try:
    WebDriverWait(driver, 5).until(EC.title_is('Gluu'))
except TimeoutException:
    returnCode = 1

driver.close()
exit(returnCode)
