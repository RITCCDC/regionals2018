from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

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

# Add source attribute mappings
for i in xrange(5):
    sourceAttributeMappingButton = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt252')
    sourceAttributeMappingButton.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cacheRefreshForm:j_idt212:j_idt216:j_idt252')))
    sleep(0.75)

sourceMap1 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:0:fInput')
destinationMap1 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:0:sInput1')
sourceMap2 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:1:fInput')
destinationMap2 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:1:sInput1')
sourceMap3 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:2:fInput')
destinationMap3 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:2:sInput1')
sourceMap4 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:3:fInput')
destinationMap4 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:3:sInput1')
sourceMap5 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:4:fInput')
destinationMap5 = driver.find_element_by_id('cacheRefreshForm:j_idt212:j_idt216:j_idt218:4:sInput1')

#sAMAccountName
sourceMap1.send_keys('s')
sourceMap1.send_keys(Keys.SHIFT, 'AMA')
sourceMap1.send_keys('ccount')
sourceMap1.send_keys(Keys.SHIFT, 'N')
sourceMap1.send_keys('ame')
destinationMap1.send_keys('uid')
sourceMap2.send_keys('cn')
destinationMap2.send_keys('cn')
sourceMap3.send_keys('sn')
destinationMap3.send_keys('sn')
sourceMap4.send_keys('mail')
destinationMap4.send_keys('mail')
#givenName
sourceMap5.send_keys('given')
sourceMap5.send_keys(Keys.SHIFT, 'N')
sourceMap5.send_keys('ame')
destinationMap5.send_keys('given')
destinationMap5.send_keys(Keys.SHIFT, 'N')
destinationMap5.send_keys('ame')

# Move to next tab
backendKeyAttributesTab.click()

# Find form elements for second tab
keyAttributeButton = driver.find_element_by_name('cacheRefreshForm:j_idt536:j_idt538:j_idt550')
objectClassButton = driver.find_element_by_name('cacheRefreshForm:j_idt563:j_idt565:j_idt577')

# Populate second tab form data
# Add key attribute
keyAttributeButton.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cacheRefreshForm:j_idt536:j_idt538:j_idt540:0:fInput')))
keyAttributeField = driver.find_element_by_id('cacheRefreshForm:j_idt536:j_idt538:j_idt540:0:fInput')
# sAMAccountName
keyAttributeField.send_keys('s')
keyAttributeField.send_keys(Keys.SHIFT, 'AMA')
keyAttributeField.send_keys('ccount')
keyAttributeField.send_keys(Keys.SHIFT, 'N')
keyAttributeField.send_keys('ame')

# Add object class
objectClassButton.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cacheRefreshForm:j_idt563:j_idt565:j_idt567:0:fInput')))
objectClassField = driver.find_element_by_id('cacheRefreshForm:j_idt563:j_idt565:j_idt567:0:fInput')
objectClassField.send_keys('user')

# Add source attributes
for i in xrange(5):
    sourceAttributesButton = driver.find_element_by_name('cacheRefreshForm:j_idt590:j_idt592:j_idt604')
    sourceAttributesButton.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'cacheRefreshForm:j_idt590:j_idt592:j_idt604')))
    sleep(0.75)

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

# Populate form elements
addSourceServerLink = driver.find_element_by_id('cacheRefreshForm:j_idt808')
addSourceServerLink.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'cacheRefreshForm:sourceConfigsId:0:j_idt632:name:j_idt637')))

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
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt717:j_idt719:j_idt721:0:fInput')))
baseDNLink.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt744:j_idt746:j_idt748:0:fInput')))

# Find newly created fields and populate data
serverAndPortField = driver.find_element_by_id('cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt717:j_idt719:j_idt721:0:fInput')
baseDNField = driver.find_element_by_id('cacheRefreshForm:sourceConfigsId:0:j_idt632:j_idt744:j_idt746:j_idt748:0:fInput')
serverAndPortField.send_keys('10.1.4.10:389')
baseDNField.send_keys('CN=Users,DC=team4,DC=wildeagle,DC=local')

# Open "change bind password" frame, input password twice
changeBindPasswordLink.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bindPasswordDialogId:changePasswordModalPanel_container')))
changeBindPasswordWindow = driver.find_element_by_id('bindPasswordDialogId:changePasswordModalPanel_container')
changeBindPasswordWindow.click()
newPasswordField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:pass')
newPasswordAgainField = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:conf')
setPasswordButton = driver.find_element_by_id('bindPasswordDialogId:changePasswordForm:j_idt154')
newPasswordField.send_keys('Change.me!')
newPasswordAgainField.send_keys('Change.me!')
setPasswordButton.click()

# Move back to first tab
ActionChains(driver).move_to_element(cacheRefreshTab).click().perform()
#cacheRefreshTab.click()

# Enable and update
enabledDropdown = Select(driver.find_element_by_id('cacheRefreshForm:vdsCacheRefreshState:vdsCacheRefreshStateId'))
enabledDropdown.select_by_visible_text('Enabled')
updateButton = driver.find_element_by_name('cacheRefreshForm:j_idt999')
updateButton.click()

driver.close()
