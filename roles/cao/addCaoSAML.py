from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Set up the driver, allowing unverified TLS certs
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities['acceptSslCerts'] = True
driver = webdriver.Firefox(capabilities=capabilities)

# Get the page and wait until the login form displays
driver.get('https://spade')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'loginForm:username')))

# Find the login form elements
usernameInput = driver.find_element_by_name("loginForm:username")
passwordInput = driver.find_element_by_name("loginForm:password")
submitButton = driver.find_element_by_name("loginForm:loginButton")

# Fill out the login form and submit
usernameInput.send_keys('admin')
passwordInput.send_keys('password')
submitButton.click()

# Wait until the next page has loaded after we auth, and then go to the trust manager page
WebDriverWait(driver, 30).until(EC.title_is('Gluu'))

driver.get('https://spade/identity/trustmanager/add')

# Find the form elements for a new trust relationship
displayName = driver.find_element_by_name('trustForm:displayName:displayNameId')
description = driver.find_element_by_name('trustForm:description:descriptionId')
entityType = Select(driver.find_element_by_name('trustForm:entityType:entityTypeId'))
metadataLocation = Select(driver.find_element_by_name('trustForm:spMetaDataSourceType:spMetaDataSourceTypeId'))

# For some reason, due to the form redraw, metadata location needs to be set first or it doesn't get changed correctly
metadataLocation.select_by_visible_text('File')

# Fill out the remaining form elements
displayName.send_keys('Cao')
description.send_keys('OTRS Server')
entityType.select_by_visible_text('Single SP')

# "Upload" the metadata file
spMetadataFile = driver.find_element_by_name('trustForm:fileWrapper:fileWrapperId')
spMetadataFile.send_keys('/tmp/metadata.saml')

# Submit the form
addButton = driver.find_element_by_name('trustForm:j_idt605')
addButton.click()

# Wait until the page reloads and the "Activate" button is present
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'trustForm:j_idt606')))

# Click the activate button to activate the relationship
activateButton = driver.find_element_by_name('trustForm:j_idt606')
activateButton.click()

driver.close()