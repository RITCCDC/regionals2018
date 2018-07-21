from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from sys import exit

parser = ArgumentParser('Add a host to SSH Keybox')
parser.add_argument('-k', dest='host', help='the Brown host', required=True)
parser.add_argument('-u', dest='username', help='the username for the Keybox web interface', required=True)
parser.add_argument('-p', dest='password', help='the password for the Keybox web interface', required=True)

args = parser.parse_args()

# Set up the driver, allowing unverified TLS certs
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities['acceptSslCerts'] = True
driver = webdriver.Firefox(capabilities=capabilities)

# Get the page and wait until the login form displays
driver.get('https://' + args.host + ':8443')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'auth.username')))

# Find the login form elements
usernameInput = driver.find_element_by_name("auth.username")
passwordInput = driver.find_element_by_name("auth.password")
submitButton = driver.find_element_by_id("login_btn")

# Fill out the login form and submit
usernameInput.send_keys(args.username)
passwordInput.send_keys(args.password)
submitButton.click()

skipOtpButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-danger')))
skipOtpButton.click()

systemsPageButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Systems')))

driver.get(systemsPageButton.get_attribute('href'))
