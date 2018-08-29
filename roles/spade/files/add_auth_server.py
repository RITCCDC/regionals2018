from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Set up driver, allow unverified TLS certs
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities['acceptSslCerts'] = True
driver = webdriver.Firefox(capabilities=capabilities)
driver.implicitly_wait(10)

# Get the page, wait for login form to display
driver.get('https://spade')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'loginForm:username')))

# Find the login form elements
usernameInput = driver.find_element_by_name("loginForm:username")
passwordInput = driver.find_element_by_name("loginForm:password")
submitButton = driver.find_element_by_name("loginForm:loginButton")

# Fill out the login form and submit
usernameInput.send_keys("admin")
passwordInput.send_keys("password")
submitButton.click()


# Wait until the next page has loaded after we auth
WebDriverWait(driver, 30).until(EC.title_is('Gluu'))

# Go to authentication page
driver.get('https://spade/identity/authentication/configuration')

# Populate authentication data
addServerLink = driver.find_element_by_name('customAuthenticationForm:j_idt342')
addServerLink.click()

nameField = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div/div/div[1]/div/div[1]/div/span/table/tbody/tr[2]/td/div/div[1]/div[2]/span/input')
bindDNField = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div/div/div[1]/div/div[1]/div/span/table/tbody/tr[2]/td/div/span/div/div[2]/span/input')
maxConnectionsAuth = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div/div/div[1]/div/div[1]/div/span/table/tbody/tr[2]/td/div/div[2]/div[2]/span/input')
primaryKeyField = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div/div/div[1]/div/div[1]/div/span/table/tbody/tr[2]/td/div/div[3]/div[2]/span/input')
localPrimaryKeyField = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div/div/div[1]/div/div[1]/div/span/table/tbody/tr[2]/td/div/div[4]/div[2]/span/input')
level = driver.find_element_by_name('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt236:j_idt237')
addServerAuthLink = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt248:j_idt250:j_idt262')
baseDNAuthLink = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt275:j_idt277:j_idt289')
changeBindPasswordAuthLink = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt302:j_idt303')

nameField.send_keys('auth_ldap_server')
bindDNField.send_keys('CN=GLUU,CN=Users,DC=team4,DC=wildeagle,DC=local')
maxConnectionsAuth.send_keys('5')
# sAMAccountName
primaryKeyField.send_keys('s')
primaryKeyField.send_keys(Keys.SHIFT, 'AMA')
primaryKeyField.send_keys('ccount')
primaryKeyField.send_keys(Keys.SHIFT, 'N')
primaryKeyField.send_keys('ame')
localPrimaryKeyField.send_keys('uid')
level.send_keys('0')

# Click links for server and baseDN, populate data
addServerAuthLink.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt248:j_idt250:j_idt252:0:fInput')))
baseDNAuthLink.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt275:j_idt277:j_idt279:0:fInput')))

addServerAuth = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt248:j_idt250:j_idt252:0:fInput')
baseDNAuth = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt275:j_idt277:j_idt279:0:fInput')

addServerAuth.send_keys('10.1.4.10:389')
baseDNAuth.send_keys('CN=Users,DC=team4,DC=wildeagle,DC=local')

# Set password for LDAP bind
changeBindPasswordAuthLink.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bindPasswordDialogId:changePasswordForm:pass')))
newPasswordAuthField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:pass')
newPasswordAgainAuthField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:conf')
setPasswordAuthButton = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:j_idt152')
newPasswordAuthField.send_keys('Change.me!')
newPasswordAgainAuthField.send_keys('Change.me!')
setPasswordAuthButton.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'customAuthenticationForm:sourceConfigsId:1:j_idt337')))
activateButton = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt337')
activateButton.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'customAuthenticationForm:j_idt539')))
updateAuthButton = driver.find_element_by_name('customAuthenticationForm:j_idt539')
updateAuthButton.click()

# Close driver and exit
driver.close()
