import time
import os
from dotenv import load_dotenv
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
import sys
import re
import datetime
#import gspread
#import gspread_dataframe as gs_df
from webdriver_manager.chrome import ChromeDriverManager
from ypro_login import ypro_login


load_dotenv()

login_id = os.environ['YLOGINID']
login_password = os.environ['YPASSWORD']
pro_url= os.environ['PRO_URL']
detail_day_base_url = os.environ['DETAIL_DAY_BASE_URL']
#options = webdriver.ChromeOptions()
#driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=options.to_capabilities(),
    options=options,
)
#-----ヤフオクを開く------
ypro_login(driver)

#-- amount list---
driver.get(pro_url+'/amount/clearing')
soup = bs4(driver.page_source,'html.parser')

#---- recieve & payment 
tb = soup.find('table',class_='ycMdSysFeeTbl')
tds = tb.find_all('td')
recv_fee = re.sub(r'\D','',tds[1].text)
pay_fee = re.sub(r'\D','',tds[2].text)


print("recv_fee:",recv_fee)
print("pay_fee:",pay_fee)

#---- use condition
use_list=[]
tb = soup.find('table',class_='ycMdItemInfoHorInv')
trs = tb.find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    if tds:
        sime_date =  tds[0].text.strip().replace('年','/').replace('月','/')
        recv_fee = re.sub(r'\D','',tds[1].text.strip())
        pay_fee = re.sub(r'\D','',tds[2].text.strip())
        kuri_fee = re.sub(r'\D','',tds[3].text.strip())
        uketori = re.sub(r'\D','',tds[4].text.strip())
        furikomi = tds[5].text.strip()
        use_list.append( [sime_date,recv_fee,pay_fee,kuri_fee,uketori,furikomi])

print(use_list)

detail_l = []
for use in reversed(use_list):
    day_key = re.sub(r'\D','',use[0])
    sime_date = use[0]
    url = f'{detail_day_base_url}/{day_key}'
    print (day_key,url)
    driver.get(url)
    soup = bs4(driver.page_source,'html.parser')

    tb = soup.find('table',class_='ycMdDataTbl')
    trs = tb.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if tds:
            if 'Date' in tds[0].attrs['class']:
                use_date = tds[0].text.strip()
                order_id = tds[1].text.strip()
                pay_item = tds[2].text.strip()
                pay_fee = re.sub(r'\D','',tds[3].text.strip())
                recv_item = tds[4].text.strip()
                recv_fee = re.sub(r'\D','',tds[5].text.strip())
                detail_l.append([sime_date,use_date,order_id,pay_item,use_date,pay_fee,recv_item,recv_fee])
                print(detail_l)
    break

driver.quit()
print("Complete!!")
