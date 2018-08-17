from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Set up driver, allow unverified TLS certs
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities['acceptSslCerts'] = True
driver = webdriver.Firefox(capabilities=capabilities)

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

# Go to cache refresh page
driver.get('https://spade/identity/organization/cacherefresh')

# Find form elements for first tab, elements for tabs
pollingInterval = driver.find_element_by_name('cacheRefreshForm:j_idt267:vdsCacheRefreshPollingIntervalId')
serverIP = driver.find_element_by_name('cacheRefreshForm:j_idt278:cacheRefreshServerIpAddressId')
cacheRefreshTab = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div[1]/div/div[1]/ul/li[1]/a')
backendKeyAttributesTab = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div[1]/div/div[1]/ul/li[2]/a')
sourceLDAPServersTab = driver.find_element_by_xpath('/html/body/div[1]/div/div/section[2]/div/form/div[1]/div/div[1]/ul/li[3]/a')


# Populate first tab form data
pollingInterval.send_keys('1')
serverIP.clear()
serverIP.send_keys('10.0.1.105')

# Move to next tab
backendKeyAttributesTab.click()

# Find form elements for second tab
keyAttributeButton = driver.find_element_by_name('cacheRefreshForm:j_idt536:j_idt538:j_idt550')
objectClassButton = driver.find_element_by_name('cacheRefreshForm:j_idt563:j_idt565:j_idt577')
sourceAttributesButton = driver.find_element_by_name('cacheRefreshForm:j_idt590:j_idt592:j_idt604')

# Populate second tab form data
# Add key attribute
keyAttributeButton.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cacheRefreshForm:j_idt536:j_idt538:j_idt540:0:fInput')))
keyAttributeField = driver.find_element_by_id('cacheRefreshForm:j_idt536:j_idt538:j_idt540:0:fInput')
keyAttributeField.send_keys('sAMAccountName')

# Add object class
objectClassButton.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cacheRefreshForm:j_idt563:j_idt565:j_idt567:0:fInput')))
objectClassField = driver.find_element_by_id('cacheRefreshForm:j_idt563:j_idt565:j_idt567:0:fInput')
objectClassField.send_keys('user')

# Add source attributes
for i in xrange(5):
    sourceAttributesButton.click()
sourceAttribute1 = driver.find_element_by_id('cacheRefreshForm:j_idt590:j_idt592:j_idt594:0:fInput')
sourceAttribute2 = driver.find_element_by_id('cacheRefreshForm:j_idt590:j_idt592:j_idt594:1:fInput')
sourceAttribute3 = driver.find_element_by_id('cacheRefreshForm:j_idt590:j_idt592:j_idt594:2:fInput')
sourceAttribute4 = driver.find_element_by_id('cacheRefreshForm:j_idt590:j_idt592:j_idt594:3:fInput')
sourceAttribute5 = driver.find_element_by_id('cacheRefreshForm:j_idt590:j_idt592:j_idt594:4:fInput')

sourceAttribute1.send_keys('cn')
sourceAttribute2.send_keys('sn')
sourceAttribute3.send_keys('mail')
sourceAttribute4.send_keys('givenName')
sourceAttribute5.send_keys('displayName')

# Move to next tab
sourceLDAPServersTab.click()

# Find form elements
connectionName = driver.find_element_by_name('cacheRefreshForm:sourceConfigsId:0:j_idt632:name:j_idt637')
bindDN = driver.find_element_by_name('cacheRefreshForm:sourceConfigsId:0:j_idt632:bindDn:j_idt659')
maxConnections = driver.find_element_by_name('cacheRefreshForm:sourceConfigsId:0:j_idt632:useSSL:j_idt670')
serverAndPortLink = driver.find_element_by_id('cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt717:j_idt719:j_idt731')
baseDNLink = driver.find_element_by_id('cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt744:j_idt746:j_idt758')
changeBindPasswordLink = driver.find_element_by_id('cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt771:j_idt772')

# Populate data that doesn't need link clicking
connectionName.send_keys('Wildeagle AD')
bindDN.send_keys('CN=GLUU,CN=Users,DC=team4,DC=wildeagle,DC=local')
maxConnections.send_keys('5')

# Click links to open up two forms
serverAndPortLink.click()
baseDNLink.click()

# Find newly created fields and populate data
serverAndPortField = driver.find_element_by_id('cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt717:j_idt719:j_idt721:0:fInput')
baseDNField = driver.find_element_by_id('cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt744:j_idt746:j_idt748:0:fInput')
serverAndPortField.send_keys('10.1.4.10:389')
baseDNField.send_keys('CN=Users,DC=team4,DC=wildeagle,DC=local')

# Open "change bind password" frame, input password twice
changeBindPasswordLink.click()
newPasswordField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:pass')
newPasswordAgainField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:conf')
setPasswordButton = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:j_idt154')
newPasswordField.send_keys('Change.me!')
newPasswordAgainField.send_keys('Change.me!')
setPasswordButton.click()

# Move back to first tab
cacheRefreshTab.click()

# Enable and update
enabledDropdown = Select(driver.find_element_by_id('cacheRefreshForm:vdsCacheRefreshState:vdsCacheRefreshStateId'))
enabledDropdown.select_by_visible_text('Enabled')
updateButton = driver.find_element_by_name('cacheRefreshForm:j_idt999')
updateButton.click()

# Wait for page to refresh
WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.PARTIAL_LINK_TEXT, 'Cache configuration updated'))

# Go to authentication page
driver.get('https://spade/identity/authentication/configuration')
WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.NAME, 'customAuthenticationForm:sourceConfigsId:0:j_idt163:name:j_idt168'))

# Populate authentication data
addServerLink = driver.find_element_by_name('customAuthenticationForm:j_idt342')
addServerLink.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.NAME, 'customAuthenticationForm:sourceConfigsId:1:j_idt163:name:j_idt168'))

nameField = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:name:j_idt168')
bindDNField = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:bindDn:j_idt190')
maxConnectionsAuth = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:useSSL:j_idt201')
primaryKeyField = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt212:j_idt213')
localPrimaryKeyField = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt224:j_idt225')
level = driver.find_element_by_name('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt236:j_idt237')
addServerAuthLink = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt248:j_idt250:j_idt262')
baseDNAuthLink = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt275:j_idt277:j_idt289')
changeBindPasswordAuthLink = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt302:j_idt303')
activateButton = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt337')
updateAuthButton = driver.find_element_by_name('customAuthenticationForm:j_idt539')

nameField.send_keys('auth_ldap_server')
bindDNField.send_keys('CN=GLUU,CN=Users,DC=team4,DC=wildeagle,DC=local')
maxConnectionsAuth.send_keys('5')
primaryKeyField.send_keys('sAMAccountName')
localPrimaryKeyField.send_keys('uid')
level.send_keys('0')

# Click links for server and baseDN, populate data
addServerAuthLink.click()
baseDNAuthLink.click()

addServerAuth = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt248:j_idt250:j_idt252:0:fInput')
baseDNAuth = driver.find_element_by_id('customAuthenticationForm:sourceConfigsId:1:j_idt163:j_idt275:j_idt277:j_idt279:0:fInput')

addServerAuth.send_keys('10.1.4.10:389')
baseDNAuth.send_keys('CN=Users,DC=team4,DC=wildeagle,DC=local')

# Set password for LDAP bind
changeBindPasswordAuthLink.click()
newPasswordAuthField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:pass')
newPasswordAgainAuthField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:conf')
setPasswordAuthButton = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:j_idt152')
newPasswordAuthField.send_keys('Change.me!')
newPasswordAgainAuthField.send_keys('Change.me!')
setPasswordAuthButton.click()

activateButton.click()
updateAuthButton.click()

# Close driver and exit
driver.close()
