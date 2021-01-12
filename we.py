import account_configs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time


start = time.time()

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)

#The required phoneNumber and Password to sign in
MobileNumber = account_configs.MobileNumber
Password = account_configs.MobileNumber


#To send password char by char to avoid char dropping
def sendPassword(password):
	key = driver.find_element_by_id('PasswordID')
	for i in password:
		key.send_keys(i)

#tries to connect then saves the login things
def save_login():
	username = driver.find_element_by_id('MobileNumberID')
	first_flag = False

	username.send_keys(MobileNumber)
	#time.sleep(5)

	#sending the password char by char
	sendPassword(Password)
	time.sleep(2)

	#clicking the signIn button
	driver.find_element_by_id('singInBtn').click()
	#Waiting for the page to reload 
	time.sleep(2)
	try: 
		moreInfo = driver.find_element_by_xpath('//*[@id="content-block"]/div/account-overview/div[2]/div/div/button')
		#print(moreInfo.text)
	except:
		first_flag = True

	if first_flag:
		key = driver.find_element_by_id('PasswordID')
		key.clear()
		sendPassword(Password)
		driver.find_element_by_id('singInBtn').click()
		time.sleep(3)

#Open file to save the data in 
fh = open('WE.txt', 'a')


#signin page
driver.get('https://my.te.eg/#/home/signin/UnAuthorized')
save_login()

#getting to the usage page, where all the data exists (shortcut)
driver.get('https://my.te.eg/#/offering/usage')

#moreInfo = driver.find_element_by_xpath('/html/body/ecare-app/div/main/div/div/div/account-overview/div[2]/div/donut-chart/div/div/div/div/div/circle-progress')
consumed = driver.find_element_by_xpath('//*[@id="tab7"]/donut-chart/div/div/div/div[2]/div/div/div/div/div/div/span[1]')

days = driver.find_element_by_xpath('//*[@id="content-block"]/div/app-usage/div/div[2]/div[1]/ngx-carousel/div[1]/div/div[1]/ngx-item/div[3]/div')

rem_days = days.text.strip('يوم')

final_data = f"'You consumed : {consumed.text}gb , Remaining : {140 - float(consumed.text)}gb , Remaining Days : {rem_days}'\n"
print(final_data)

#sending notification 
os.system(f"notify-send -u critical -t 10000 " + final_data)


#wrinting to the file
fh.write(final_data)


#closing the file and quitting the browser
fh.close()
driver.quit()
#end = time.time()
#print(f"This took : {end- start}s")
