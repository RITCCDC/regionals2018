from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from sys import exit

parser = ArgumentParser('Upload a SAML certificate to Gluu')
parser.add_argument('-g', dest='host', help='the Gluu server host', required=True)
parser.add_argument('-u', dest='username', help='the username for the Gluu web interface', required=True)
parser.add_argument('-p', dest='password', help='the password for the Gluu web interface', required=True)
parser.add_argument('-n', dest='name', help='the name of the trust relationship', required=True)
parser.add_argument('-d', dest='description', help='the description for the trust relationship', required=True)
parser.add_argument('-f', dest='metadataFile', help='path to the metadata file to upload', required=True)

args = parser.parse_args()

# Set up the driver, allowing unverified TLS certs
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities['acceptSslCerts'] = True
driver = webdriver.Firefox(capabilities=capabilities)

# Get the page and wait until the login form displays
driver.get('https://' + args.host)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'loginForm:username')))

# Find the login form elements
usernameInput = driver.find_element_by_name("loginForm:username")
passwordInput = driver.find_element_by_name("loginForm:password")
submitButton = driver.find_element_by_name("loginForm:loginButton")

# Fill out the login form and submit
usernameInput.send_keys(args.username)
passwordInput.send_keys(args.password)
submitButton.click()

# Wait until the next page has loaded after we auth, and then go to the trust manager page
WebDriverWait(driver, 30).until(EC.title_is('Gluu'))

# Go to the trust relationship page
driver.get('https://spade/identity/trustmanager/relationships')

# Check to see if there is an existing relationship. If yes, close driver and exit. Else continue
try:
  WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, args.name)))
  driver.close()
  exit()
except Exception as e:
  pass

driver.get('https://spade/identity/trustmanager/add')

# Find the form elements for a new trust relationship
displayName = driver.find_element_by_name('trustForm:displayName:displayNameId')
description = driver.find_element_by_name('trustForm:description:descriptionId')
entityType = Select(driver.find_element_by_name('trustForm:entityType:entityTypeId'))
metadataLocation = Select(driver.find_element_by_name('trustForm:spMetaDataSourceType:spMetaDataSourceTypeId'))

# For some reason, due to the form redraw, metadata location needs to be set first or it doesn't get changed correctly
metadataLocation.select_by_visible_text('File')

# Fill out the remaining form elements
displayName.send_keys(args.name)
description.send_keys(args.description)
entityType.select_by_visible_text('Single SP')

# "Upload" the metadata file
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'trustForm:fileWrapper:fileWrapperId')))
spMetadataFile = driver.find_element_by_name('trustForm:fileWrapper:fileWrapperId')
spMetadataFile.send_keys(args.metadataFile)

# Release the username attribute to the SP
usernameAttribute = driver.find_element_by_name('trustForm:j_idt368:0:j_idt371:32:j_idt373')
usernameAttribute.click()

# Submit the form
addButton = driver.find_element_by_name('trustForm:j_idt605')
addButton.click()

# Force a 5 second wait due to a race condition in Gluu. The "Activate" button will appear immediately, but clicking it won't actually activate the relationship, presumably due to a race condition in the relationship creation
try:
  WebDriverWait(driver, 5)
except:
  pass

# Ensure that the "Activate" button is present
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'trustForm:j_idt606')))

# Click the activate button to activate the relationship
activateButton = driver.find_element_by_xpath('//input[@value = "Activate"]')
activateButton.click()

driver.close()