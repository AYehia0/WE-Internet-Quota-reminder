This is a simple script i use to get the quota usage (Remaining/Consumed GBs and how many days left) just when i turn on my PC.

The Script works on linux, i don't think it will work on Window (who uses windows anyways)
i have tried to optimize the speed of the script and the resources needed as far as i could went from ```30sec``` to ```10sec```, i tried using the old way to scrape the website but failed due to some shit ```awt tokens``` and other required headers.

The login method i made, tries 2 times to login as i found out that it works the second try ,most of the time, maybe i will try to brute force login :3 



# Things to do before executing

1) Install selenium for WebAutomation : ```pip install selenium```
2) Download chromium webdriver :
3) Add a job to your ```crontab``` : ```sudo crontab -u <usr> -e```
4) Add the path to the script as : ```@reboot sleep 40; screen -d -m -S none python ~/Desktop/testWE/WE-Internet-Quota-reminder/we.py 2>/dev/null```
5) Customize the time as your pc boot speed.


# configs 
Don't forget to add these to ```account_configs.py``` 
* Username/ServiceNumber
* password 

# ToDo

* Draw the useage at the end of the month using ```matplotlib```
* Speed it up
* Correct the login method that i used.

