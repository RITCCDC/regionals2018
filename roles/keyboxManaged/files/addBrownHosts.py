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
parser.add_argument('-n', dest='name', help='the name of the system to add', required=True)
parser.add_argument('-s', dest='system', help='the IP or hostname of the system to add', required=True)

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

# Ignore a two factor auth setup warning
skipOtpButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-danger')))
skipOtpButton.click()

# Find and navigate to the Systems page. Need to do this because a CSRF token is embedded in the link.
systemsPageButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Systems')))
driver.get(systemsPageButton.get_attribute('href'))

# Check to see if the system is already present. If it's there, we're done. Else add it in.
try:
  existingSystem = driver.find_element(By.XPATH, "//div[text()='" + args.name + "']")
  driver.close()
  quit()
except Exception as e:
  # Open the Add System dialog
  addSystemButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'add_btn')))
  addSystemButton.click()

  # Find the various inputs in the Add System dialog, fill out, and submit
  displayNameField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'hostSystem.displayNm')))
  displayNameField.send_keys(args.name)
  hostField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'hostSystem.host')))
  hostField.send_keys(args.system)
  submitSystemButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'submit_btn')))
  submitSystemButton.click()
  driver.close()
  quit()