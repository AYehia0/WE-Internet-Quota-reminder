from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(chrome_options=chrome_options)

Notify.init('New')

#The required phoneNumber and Password to sign in
MobileNumber = ""
Password = ""

#To Run chrome in the background
# options = Options()
# options.headless =True
# driver = webdriver.Chrome()

#To send password char by char to avoid char dropping
def sendPassword(password):
	key = driver.find_element_by_id('PasswordID')
	for i in password:
		key.send_keys(i)


#Open file to save the data in 
fh = open('WE.txt', 'a')

#The xPaths 
#//*[@id="content-block"]/div/app-usage/div/div[2]/div[1]/ngx-carousel/div[1]/div/div[1]/ngx-item/div[3]/div
#//*[@id="tab7"]/donut-chart/div/div/div/div[2]/div/div/div/div/div/div/span[1]
#//*[@id="tab7"]/donut-chart/div/div/div/div[2]/div/div/div/div/div/div/span[2]

#signin page
driver.get('https://my.te.eg/#/home/signin/UnAuthorized')

#getting the username input field
username = driver.find_element_by_id('MobileNumberID')
#sending the phonenumber (no need to send char by char idk why it works here)
try :
	username.send_keys(MobileNumber)
	#time.sleep(5)

	#sending the password char by char
	sendPassword(Password)
	time.sleep(2)

	#clicking the signIn button
	driver.find_element_by_id('singInBtn').click()
	#Waiting for the page to reload 
	time.sleep(8)

	#For getting all the info
	moreInfo = driver.find_element_by_xpath('//button[text()="عرض التفاصيل"]')
	
except :
	key = driver.find_element_by_id('PasswordID')
	key.clear()
	sendPassword(Password)
	time.sleep(5)

	#clicking the signIn button
	driver.find_element_by_id('singInBtn').click()
	moreInfo = driver.find_element_by_xpath('//button[text()="عرض التفاصيل"]')

moreInfo.click()
time.sleep(8)

#grabbing all the info needed
days = driver.find_element_by_xpath('//*[@id="content-block"]/div/app-usage/div/div[2]/div[1]/ngx-carousel/div[1]/div/div[1]/ngx-item/div[3]/div')
quota = driver.find_element_by_xpath('//*[@id="tab7"]/donut-chart/div/div/div/div[2]/div/div/div/div/div/div/span[1]')
availableQuota = driver.find_element_by_xpath('//*[@id="tab7"]/donut-chart/div/div/div/div[2]/div/div/div/div/div/div/span[2]')

remainingDays = days.text.strip('يوم')
consumedQuota = quota.text
remainingQuota = availableQuota.text.strip('المتبقي')

info = f'You consumed {consumedQuota} Gb, remaining{remainingQuota} Gb and there are still {remainingDays} days! \n'

#wrinting to the file
fh.write(info)

#creating new notification
notification_msg = Notify.Notification.new('WE-Data', info)

#setting urgency '2' means that it will always appear till user close it
notification_msg.set_urgency(2)

#showing the notification
notification_msg.show()

#print(finfo)

#closing the file and quitting the browser
fh.close()
driver.quit()