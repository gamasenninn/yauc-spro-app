import time
import os
from dotenv import load_dotenv
from selenium import webdriver
#import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
#import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
import sys
import re
import datetime
from webdriver_manager.chrome import ChromeDriverManager

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
#-----ヤフオクを開く------
print("try login.....")
try:
    driver.get(pro_url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'username')))
    search_box = driver.find_element_by_id("username")
    search_box.send_keys(login_id)
    driver.find_element_by_id("btnNext").click()
    time.sleep(1) #なぜかしら必要。waitのタイミング？
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'passwd')))
    search_box = driver.find_element_by_id("passwd")
    search_box.send_keys(login_password)
    driver.find_element_by_id("btnSubmit").click()
    print("OK log in!")
except Exception as e:
    print(e)
    driver.quit()
    sys.exit()

#-- get Order ID detail item ---
for id in ids:
    url = f'{order_base_url}{id}'
    driver.get(url)
    soup = bs4(driver.page_source,'html.parser')
    print (soup)

driver.quit()
sys.exit()
