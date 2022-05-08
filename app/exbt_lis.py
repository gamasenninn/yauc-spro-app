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
    soup = bs4(driver.page_source, 'html.parser')

    #---- recieve & payment
    total = soup.find('span', class_='PageIndicator__total')
    itemCount = int(re.sub(r'\D', '', total.text))

    page_max = int(itemCount/100 + 0.999999999)
    print('page_max:',page_max )


    # ---- use condition
    exbt_list = []
    for page in range(1,page_max+1):
        if page > 1 :
            driver.get(f'{exbt_url}?page={page}')
            soup = bs4(driver.page_source, 'html.parser')

        tb = soup.find('div', class_='Table__body')
        tuls = tb.find_all('ul',class_='Table__line')
        for tul in tuls:
            tlis = tul.find_all('li')
            if tlis:
                title = tul.find('p',class_="Table__title").text.strip()
                auc_id = tul.find('p',class_="Table__auctionId").text.replace('オークションID','').strip()
                scode = tul.find('p',class_="Table__manageId").text.replace('管理番号','').strip()
                start_price = re.sub(r'\D','',tul.find('p',class_="Table__startPrice").text.strip())
                bid_price = re.sub(r'\D','',tul.find('p',class_="Table__bidPrice").text.strip())
                pv = re.sub(r'\D','',tul.find('li',class_="Table__pv").text.strip())
                bid = re.sub(r'\D','',tul.find('li',class_="Table__bid").text.strip())
                watch = re.sub(r'\D','',tul.find('li',class_="Table__watch").text.strip())
                close_count = re.sub(r'\D','',tul.find('li',class_="Table__closeTime").text.strip())
                exbt_list.append([scode,auc_id,title,start_price,bid_price,
                                pv, bid, watch, close_count])

    print(exbt_list)

    df = pd.DataFrame(exbt_list,
                    columns=[
                        "scode","auc_id","title","start_price","bid_price",
                                "pv", "bid", "watch", "close_count"
                    ])
    save_filename = datetime.datetime.now().strftime('%y%m%d') + '_' + exbt_list_filenmae 
    os.makedirs(data_dir, exist_ok=True)
    save_path = os.path.join(data_dir, save_filename)
    df.to_csv(save_path, encoding='cp932')

    return


if __name__ == '__main__':

    load_dotenv()
    hub_url = os.environ['HUB_URL']

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=hub_url,
        desired_capabilities=options.to_capabilities(),
        options=options,
    )

    ypro_login(driver)
    exbt_list(driver)

    driver.quit()
    print("Complete!!")
