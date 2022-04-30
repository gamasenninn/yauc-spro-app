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

def fee_list(driver):

    pro_url = os.environ['PRO_URL']
    detail_day_base_url = os.environ['DETAIL_DAY_BASE_URL']
    data_dir = os.environ['DATA_DIR']
    order_filename = os.environ['ORDER_FILENAME']
    fee_list_filename = os.environ['FEE_LIST_FILENAME']

    # -- amount list---
    driver.get(pro_url+'/amount/clearing')
    soup = bs4(driver.page_source, 'html.parser')

    #---- recieve & payment
    tb = soup.find('table', class_='ycMdSysFeeTbl')
    tds = tb.find_all('td')
    recv_fee = re.sub(r'\D', '', tds[1].text)
    pay_fee = re.sub(r'\D', '', tds[2].text)

    # ---- use condition
    use_list = []
    tb = soup.find('table', class_='ycMdItemInfoHorInv')
    trs = tb.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if tds:
            close_date = ex_date(tds[0].text)
            recv_fee = re.sub(r'\D', '', tds[1].text.strip())
            pay_fee = re.sub(r'\D', '', tds[2].text.strip())
            carry_fee = re.sub(r'\D', '', tds[3].text.strip())
            amount_fee = re.sub(r'\D', '', tds[4].text.strip())
            transfer = tds[5].text.strip()
            status = tds[6].text.strip()
            use_list.append([close_date, recv_fee, pay_fee,
                            carry_fee, amount_fee, transfer, status])

    print(use_list)

    # ------ get order informatin -----
    order_file_path = os.path.join(
        data_dir, datetime.datetime.now().strftime('%y%m%d')+'_'+order_filename)

    if os.path.isfile(order_file_path):
        df_order = pd.read_csv(order_file_path, encoding='cp932')
    else:
        print("order data can't load....abort!")
        driver.quit()
        sys.exit()

    # ------ make detail list  ------
    detail_l = []
    for use in reversed(use_list):
        day_key = re.sub(r'\D', '', use[0])
        close_date = use[0]
        status = use[6]
        url = f'{detail_day_base_url}/{day_key}'
        print(day_key, url)
        driver.get(url)
        soup = bs4(driver.page_source, 'html.parser')

        tb = soup.find('table', class_='ycMdDataTbl')
        trs = tb.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if tds:
                if 'Date' in tds[0].attrs['class']:
                    use_date = ex_date(tds[0].text)
                    order_id = tds[1].text.strip()
                    pay_item = tds[2].text.strip()
                    pay_fee = int(re.sub(r'\D', '', tds[3].text.strip()) or 0)
                    recv_item = tds[4].text.strip()
                    recv_fee = int(re.sub(r'\D', '', tds[5].text.strip()) or 0)
                    row = df_order[df_order['Id'] == order_id]
                    title = row.loc[:, 'Title'].iloc[-1].replace("L1=","")
                    yauc_id = row.loc[:, 'YahooAuctionId'].iloc[-1]
                    scode = row.loc[:, 'YahooAuctionMerchantId'].iloc[-1]
                    bill_name = row.loc[:, 'BillName'].iloc[-1]
                    detail_l.append([
                        close_date,
                        status,
                        use_date,
                        order_id,
                        pay_item,
                        pay_fee,
                        recv_item,
                        recv_fee,
                        title,
                        yauc_id,
                        scode,
                        bill_name
                    ])
        # break
    #print(detail_l)

    df = pd.DataFrame(detail_l,
                    columns=[
                        "close_date",
                        "status",
                        "use_date",
                        "order_id",
                        "pay_item",
                        "pay_fee",
                        "recv_item",
                        "recv_fee",
                        "title",
                        "yauc_id",
                        "scode",
                        "bill_name"
                    ])
    save_filename = datetime.datetime.now().strftime('%y%m%d')+'_'+fee_list_filename
    os.makedirs(data_dir, exist_ok=True)
    save_path = os.path.join(data_dir, save_filename)
    df.to_csv(save_path, encoding='cp932')



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
    fee_list(driver)

    driver.quit()
    print("Complete!!")
