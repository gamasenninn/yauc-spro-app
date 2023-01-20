import os
import sys
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs4
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from ypro_login import ypro_login
from lxml import html
from sqlalchemy import create_engine

TMP_PATH = "S:/プログラム関連/直接.txt"


LXS = []

expect_path = '//*[@id="__next"]/div[1]/div/main/div/fieldset[1]/div[2]/div/div/label/input'


def ex_date(date_text):
    return date_text.strip().replace('年', '/').replace('月', '/').replace('日', '')

def set_attribute(driver,xpath,attribute,value):
    elm = driver.find_element(By.XPATH,xpath)
    driver.execute_script(f"arguments[0].{attribute} = '{value}';", elm)

def set_value(driver,xpath,value):
    elm = driver.find_element(By.XPATH,xpath)
    driver.execute_script(f"arguments[0].value = arguments[1];", elm,value)


def re_exbt(driver,aucid,dict):
    exbt_url = os.environ['RE_EXBT_URL']

    # -- exhbit lisr URL---
    driver.get(exbt_url+aucid)
    driver.implicitly_wait(10)

    driver.find_element(By.XPATH,expect_path)
    #タイトル
    set_attribute(driver,'//fieldset[2]/div[2]/div/label/input','value',dict['title'])
    #カテゴリ
    set_attribute(driver,'//fieldset[3]/div[2]/div/div/div[2]/div/label/input','value',dict['category'])
    #商品説明
    desc = dict['description']
    set_value(driver,'//*[@id="textMode"]/div[2]/textarea',desc)
    #状態
    sts = int(int(re.sub(r"\D","",dict['status']))/10)
    driver.find_element(By.XPATH,f'//fieldset[10]/div[2]/div/ul/li[{sts}]/div/label/span[2]').click()
    #消費税
    tax = 3
    driver.find_element(By.XPATH,f'//fieldset[11]/div[2]/div/ul/li[{tax}]/div/label/span[2]').click()
    #税込み
    #開始価格
    set_attribute(driver,'//fieldset[12]/div[2]/div/div/div[2]/div/div[2]/div/label/input','value',dict['start_price'])
    #即決価格
    set_attribute(driver,'//fieldset[12]/div[2]/div/div/div[3]/div/div[2]/div/label/input','value',dict['end_price'])
    #個数
    set_attribute(driver,'//fieldset[13]/div[2]/div/div/div/label/input','value','1')
    #開催期間
    day_period = dict['period']
    time_priod = 17
    driver.find_element(By.XPATH,f'//fieldset[14]/div[2]/div/div/div[1]/label/select/option[{day_period-1}]').click()
    driver.find_element(By.XPATH,f'//fieldset[14]/div[2]/div/div/div[2]/label/select/option[{time_priod}]').click()

    # 再出品ボタンをクリック(確認段階)
    #driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div/main/div/div[3]/ul/li[2]/button').click()


    return

def get_target_data(aucid):

    if not aucid:
        return ""

    DB_URL = os.environ['DB_URL']
    SQL_STR = "select * from 出品商品管理票 where オークションID = '{:}' order by 管理番号 desc limit 10"

    engine = create_engine(DB_URL, echo=False)
    df = pd.read_sql(sql=SQL_STR.format(aucid),  con=engine)
    if not df.empty:
        dict = {
            "pname" : df.loc[0,"商品名"],
            "title" : df.loc[0,"タイトル"],
            "scode" : df.loc[0,"仕切書No"],
            "maker" : df.loc[0,"メーカー"],
            "model" : df.loc[0,"型式"],
            "width" : str(df.loc[0,"梱包サイズ横"]),
            "long" : str(df.loc[0,"梱包サイズ縦"]),
            "height" : str(df.loc[0,"梱包サイズ高"]),
            "category" : df.loc[0,"カテゴリID"],
            "period" : df.loc[0,"出品日数"],
            "status" : df.loc[0,"商品状態"],
            "start_price" : int(df.loc[0,"開始価格"]),
            "end_price" : int(df.loc[0,"即決価格"]),
            "description" : df.loc[0,"出品詳細"],
        }
        with open(TMP_PATH,'r') as f:
            tmp_str = f.read()
        #print(tmp_str)
        desc = dict["description"]
        bikou = ''
        setsumei = ''
        if "<!--詳細備考-->" in desc:
            ds = desc.split('<!--詳細備考-->')
            for i,d in enumerate(ds): 
                if i == 0:
                    setsumei = ds[i]
                else:
                    bikou = bikou+ ds[i]
        tmp_str = tmp_str.replace("%%SHOHIN_NAME%%",dict["pname"])
        tmp_str = tmp_str.replace("%%MAKER%%",dict["maker"])
        tmp_str = tmp_str.replace("%%KATASHIKI%%",dict["model"])
        tmp_str = tmp_str.replace("%%SETSUMEI%%",setsumei)
        tmp_str = tmp_str.replace("%%BIKOU%%",bikou)
        tmp_str = tmp_str.replace("%%SIZE_TATE%%",dict["long"])
        tmp_str = tmp_str.replace("%%SIZE_YOKO%%",dict["width"])
        tmp_str = tmp_str.replace("%%SIZE_TAKASA%%",dict["height"])
        tmp_str = tmp_str.replace("%%KANRI_NO%%",dict["scode"])
        dict["description"] = tmp_str
        return dict
    return ""

if __name__ == '__main__':

    load_dotenv()
    hub_url = os.environ['HUB_URL']

    dmode = "local" # "remote"
    is_test = False

    if len(sys.argv) > 0 :
        aucid=sys.argv[1]

    if is_test:
        aucid  = "s1064874767"
        dict = get_target_data(aucid)
        #print(dict)
        sys.exit()



    options = webdriver.ChromeOptions()
    if dmode == "remote":
        driver = webdriver.Remote(
            command_executor=hub_url,
            desired_capabilities=options.to_capabilities(),
            options=options,
        )
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        
    dict = get_target_data(aucid)

    if dict:
        ypro_login(driver)
        re_exbt(driver,aucid,dict)

    #driver.quit()
    print("Complete!!")
