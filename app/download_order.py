import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs4
import pandas as pd
import sys
import re
import datetime
#from webdriver_manager.chrome import ChromeDriverManager
from ypro_login import ypro_login

load_dotenv()

login_id = os.environ['YLOGINID']
login_password = os.environ['YPASSWORD']
pro_url= os.environ['PRO_URL']
order_base_url = os.environ['ORDER_BASE_URL']

options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=options.to_capabilities(),
    options=options,
)
#-----login-------
ypro_login(driver)

#-- jump search page  ---
url = f'{pro_url}/order/manage/index'
driver.get(url)

#from_day = driver.find_element_by_id("OrderTimeFromDayE")
#from_day.send_keys("2022/03/09")

btns = driver.find_elements_by_class_name("btnBlL")
btns[1].find_element_by_tag_name('a').click()

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'ycWrContentsFix')))
link = driver.find_element_by_class_name("fileNum")
link.find_element_by_tag_name('a').click()

time.sleep(20) #ダウンロード終わらないうちに終わらないため。ここをなんとかしないといけん。

driver.quit()
sys.exit()


'''
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:4.1.3-20220405

docker run -d -p 4444:4444 -p 7900:7900 -v C:/Users/user/Downloads:/home/seluser/Downloads --shm-size="2g" selenium/standalone-chrome:4.1.3-20220405

'''
