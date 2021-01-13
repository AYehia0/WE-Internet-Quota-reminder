import account_configs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time

#for waiting elements
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


start = time.time()

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)


#init wait time 
sec = 5 
home_page = 'https://my.te.eg/#/offering/usage'
time_to_wait = WebDriverWait(driver, sec)


#The required phoneNumber and Password to sign in
MobileNumber = account_configs.MobileNumber
Password = account_configs.Password

#required xpaths and IDs
consumed_xpath = '//*[@id="tab7"]/donut-chart/div/div/div/div[2]/div/div/div/div/div/div/span[1]'
remaining_days_xpath = '//*[@id="content-block"]/div/app-usage/div/div[2]/div[1]/ngx-carousel/div[1]/div/div[1]/ngx-item/div[3]/div'
moreInfo_xpath = '//*[@id="content-block"]/div/account-overview/div[2]/div/div/button'
remain_q_xpath = '//*[@id="tab7"]/donut-chart/div/div/div/div[2]/div/div/div/div/div/div/span[2]'
password_id = 'PasswordID'
mobile_id = 'MobileNumberID'
signIn_id = 'singInBtn'


#To send password char by char to avoid char dropping
def sendPassword(password):
	key = driver.find_element_by_id(password_id)
	for i in password:
		key.send_keys(i)

#tries to connect then saves the login things
def save_login():
	username = driver.find_element_by_id(mobile_id)
	first_flag = False

	username.send_keys(MobileNumber)

	#sending the password char by char
	sendPassword(Password)

	#waiting for the sign in and clicking the signIn button
	#driver.find_element_by_id(signIn_id).click()

	time_to_wait.until(EC.presence_of_element_located((By.ID, signIn_id))).click()
	#Waiting for the page to reload 
	#time.sleep(2)
	try: 
		#moreInfo = driver.find_element_by_xpath(moreInfo_xpath)
		moreInfo = time_to_wait.until(EC.presence_of_element_located((By.XPATH, moreInfo_xpath)))
	except:
		first_flag = True

	if first_flag:
		key = driver.find_element_by_id('PasswordID')
		key.clear()
		sendPassword(Password)
		driver.find_element_by_id(signIn_id).click()
		time.sleep(3)

#Open file to save the data in 
fh = open('data.txt', 'a')


#signin page
driver.get(home_page)
save_login()

#getting to the usage page, where all the data exists (shortcut)
driver.get(home_page)
#time.sleep(3)

#moreInfo = driver.find_element_by_xpath('//*[@id="content-block"]/div/account-overview/div[2]/div/div/button').click()
#consumed = driver.find_element_by_xpath(counsumed_xpath)
consumed = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, consumed_xpath)))
remained = time_to_wait.until(EC.presence_of_element_located((By.XPATH, remain_q_xpath)))
days = time_to_wait.until(EC.visibility_of_element_located((By.XPATH, remaining_days_xpath)))

rem_days = days.text.strip('يوم')

final_data = f"'You consumed : {consumed.text}gb , Remaining : {remained.text.strip('المتبقي')}gb , Remaining Days : {rem_days}'"

#sending notification 
os.system(f"notify-send -u critical -t 10000 " + final_data)


#wrinting to the file
os.system("echo " + final_data + " >> ~/Desktop/testWE/WE-Internet-Quota-reminder/data.txt") 

#quitting the browser
driver.quit()
