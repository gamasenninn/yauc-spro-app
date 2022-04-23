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

load_dotenv()

login_id = os.environ['YLOGINID']
login_password = os.environ['YPASSWORD']
pro_url= os.environ['PRO_URL']

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
'''
driver.get('https://auctions.yahoo.co.jp/')
print(driver.current_url)
#time.sleep(2)

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'TextBold-sc-1u4qbnp')))

e = driver.find_element_by_class_name("TextBold-sc-1u4qbnp")
'''
print("try login.....")
#driver.get('https://login.yahoo.co.jp/config/login')
#time.sleep(2)
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
        sime_date =  tds[0].text.strip()
        recv_fee = re.sub(r'\D','',tds[1].text.strip())
        pay_fee = re.sub(r'\D','',tds[2].text.strip())
        kuri_fee = re.sub(r'\D','',tds[3].text.strip())
        uketori = re.sub(r'\D','',tds[4].text.strip())
        furikomi = tds[5].text.strip()
        use_list.append( [sime_date,recv_fee,pay_fee,kuri_fee,uketori,furikomi])

print(use_list)





#time.sleep(30)
#driver.quit()
sys.exit()


driver.get('https://onavi.auctions.yahoo.co.jp/onavi/show/storelist?select=won&page=1&op=9&od=2&rpp=100')


elms = driver.find_element_by_id("td4_0")

df = pd.DataFrame()
for row in range(100):
    dic ={}
    for col in range(3,6):
        tid = "td"+str(col)+"_"+str(row)
        elm = driver.find_element_by_id(tid)
        if (elm) : 
            elms_tr = elm.find_elements_by_tag_name("tr")
            for tr in elms_tr:
                elms_td = tr.find_elements_by_tag_name("td")
                k = elms_td[0].text.replace('（税込）','')
                v = elms_td[1].text.replace('\n','')
                print ("["+k+"] "+v)
                dic[k] =v
        else:
            break
    #print(dic)
    df = df.append(dic, ignore_index=True)

df['オークションID'] = df['オークションID'].str.replace('（商品ページ）','')
df['郵便番号'] = df['お届け先住所'].str.split(pat=' ',expand=True)[0]
df['住所'] = df['お届け先住所'].str.split(pat=' ',expand=True)[1]
df['氏名'] = df['お届け先氏名'].str.split(pat='（|） ',expand=True)[0]
df['フリガナ'] = df['お届け先氏名'].str.split(pat='（|） ',expand=True)[1]


df2 = df[['管理番号','オークションID','タイトル','落札日時','落札者',
          '氏名','フリガナ','郵便番号','住所','お届け先電話','落札者氏名',
          '落札者メール','落札金額','かんたん決済支払期限']]
df2.to_csv('won\\wonlist_'+str(datetime.date.today())+'.csv')

driver.quit()

