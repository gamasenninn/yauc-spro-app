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
import sys
import re
import datetime
#from webdriver_manager.chrome import ChromeDriverManager

from ypro_login import ypro_login


ids =[10000007,10000008]

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

ypro_login(driver)

#-- get Order ID detail item ---
for id in ids:
    url = f'{order_base_url}{id}'
    driver.get(url)
    soup = bs4(driver.page_source,'html.parser')
    print (soup)

driver.quit()
sys.exit()
