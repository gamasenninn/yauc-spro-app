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
from lxml import html


LXS = []

expect_path = '//*[@id="__next"]/div[1]/div/main/div/div/div[3]/section/div/div[3]/div/div[1]/div/p[1]'

ul_path = '//*[@id="__next"]/div[1]/div/main/div/div/div[3]/section/div/div[4]/div/div/ul'

def ex_date(date_text):
    return date_text.strip().replace('年', '/').replace('月', '/').replace('日', '')

def exbt_list(driver):

    pro_url = os.environ['PRO_URL']
    detail_day_base_url = os.environ['DETAIL_DAY_BASE_URL']
    data_dir = os.environ['DATA_DIR']
    order_filename = os.environ['ORDER_FILENAME']
    fee_list_filename = os.environ['FEE_LIST_FILENAME']
    exbt_url = os.environ['EXBT_URL']
    exbt_list_filenmae = os.environ['EXBT_LIST_FILENAME']

    # -- exhbit lisr URL---
    driver.get(exbt_url)
    driver.implicitly_wait(30)
    #driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div/main/div/div/div[3]/section/div/div[4]/div/div[1]/div/p[1]')
    driver.find_element_by_xpath(expect_path)
    soup = bs4(driver.page_source, 'html.parser')
    lx = html.fromstring(str(soup))
    global LXS
    LXS.append(lx)

    #---- recieve & payment  sc-cMljjf kSOPKl
    #total = soup.find('span', class_='PageIndicator__total')
    #total = soup.find('p', class_='sc-cMljjf kSOPKl')
    #total = lx.xpath('//*[@id="__next"]/div[1]/div/main/div/div/div[3]/section/div/div[4]/div/div[1]/div/p[1]')[0].text
    total = lx.xpath(expect_path)[0].text
    itemCount = int(re.sub(r'\D', '', total))

    page_max = int(itemCount/100 + 0.999999999)
    print('page_max:',page_max )


    # ---- use condition
    exbt_list = []
    all_count = 0
    for page in range(1,page_max+1):
        if page > 1 :
            driver.get(f'{exbt_url}?page={page}')
            #driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div/main/div/div/div[3]/section/div/div[5]/div/div/ul')
            driver.find_element_by_xpath(ul_path)
            soup = bs4(driver.page_source, 'html.parser')
            lx = html.fromstring(str(soup))
            LXS.append(lx)
            

        #tb = soup.find('div', class_='Table__body')
        #tuls = tb.find_all('ul',class_='Table__line')
        #tuls = lx.xpath('//*[@id="__next"]/div[1]/div/main/div/div/div[3]/section/div/div[5]/div/div/ul')
        tuls = lx.xpath(ul_path)

        tul_count = 0
        for tul in tuls:
            if tul_count == 0:
                tul_count += 1
                continue
            title = tul.xpath('./li[3]/div/div/p[1]/a')[0].text
            auc_id = tul.xpath('./li[3]/div/div/p[2]')[0].text.replace('オークションID','').strip()
            scode = tul.xpath('./li[3]/div/div/p[3]')[0].text.replace('管理番号','').strip()
            tx_prices = tul.xpath('./li[5]/div/div/p/text()')
            start_price = re.sub(r'\D','',tx_prices[0].strip())
            try:
                bid_price = re.sub(r'\D','',tx_prices[1].strip())
            except:
                bid_price = 0
            pv = re.sub(r'\D','',tul.xpath('./li[7]/div')[0].text.strip())
            bid = re.sub(r'\D','',tul.xpath('./li[8]/div')[0].text.strip())
            watch = re.sub(r'\D','',tul.xpath('./li[9]/div')[0].text.strip())
            close_count = re.sub(r'\D','',tul.xpath('./li[10]/div')[0].text.strip())
            #print(all_count,auc_id,scode,title,start_price,bid_price,pv,bid,watch,close_count)
            exbt_list.append([scode,auc_id,title,start_price,bid_price,
                                pv, bid, watch, close_count])
            
            tul_count += 1
            all_count += 1

    #print(exbt_list)

    df = pd.DataFrame(exbt_list,
                    columns=[
                        "scode","auc_id","title","start_price","bid_price",
                                "pv", "bid", "watch", "close_count"
                    ])
    save_filename = datetime.datetime.now().strftime('%y%m%d') + '_' + exbt_list_filenmae 
    os.makedirs(data_dir, exist_ok=True)
    save_path = os.path.join(data_dir, save_filename)
    df.to_csv(save_path, encoding='cp932')
    print("Data saved:",all_count)

    return


if __name__ == '__main__':

    load_dotenv()
    hub_url = os.environ['HUB_URL']
    dmode = "local" # "remote"
    

    options = webdriver.ChromeOptions()
    if dmode == "remote":
        driver = webdriver.Remote(
            command_executor=hub_url,
            desired_capabilities=options.to_capabilities(),
            options=options,
        )
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        

    ypro_login(driver)
    exbt_list(driver)

    driver.quit()
    print("Complete!!")
