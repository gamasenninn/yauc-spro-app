#  2023/01/21
#  再出品のための処理。
#　DBから出品データを読み、ストアクリエータープロの再出品処理に埋め込む。
#　項目が間違っていないかを目視で確認するため、手動で更新ボタンをクリックして更新すること。
#
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
from webdriver_manager.chrome import ChromeDriverManager
from ypro_login import ypro_login,init_driver
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import time

expect_path = '//*[@id="__next"]/div[1]/div/main/div/fieldset[1]/div[2]/div/div/label/input'

def ex_date(date_text):
    return date_text.strip().replace('年', '/').replace('月', '/').replace('日', '')

def set_attribute(driver,xpath,attribute,value):
    elm = driver.find_element(By.XPATH,xpath)
    driver.execute_script(f"arguments[0].{attribute} = arguments[1];", elm,value)

def re_exbt(driver,aucid,dict):
    exbt_url = os.environ['RE_EXBT_URL']

    # -- exhbit lisr URL---
    driver.get(exbt_url+aucid)
    driver.implicitly_wait(10)

    try:
        driver.find_element(By.XPATH,expect_path)
        time.sleep(3) #これを入れないと反映されないかも

        #タイトル
        #set_attribute(driver,'//fieldset[2]/div[2]/div/label/input','value',dict['title'])
        driver.find_element(By.XPATH,'//fieldset[2]/div[2]/div/label/input').clear()
        driver.find_element(By.XPATH,'//fieldset[2]/div[2]/div/label/input').send_keys(dict['title'])  
        #カテゴリ
        driver.find_element(By.XPATH,'//fieldset[3]/div[2]/div/div/div[2]/div/label/input').clear  
        driver.find_element(By.XPATH,'//fieldset[3]/div[2]/div/div/div[2]/div/label/input').send_keys(dict['category'])  
        #set_attribute(driver,'//fieldset[3]/div[2]/div/div/div[2]/div/label/input','value',dict['category'])
        #driver.find_element(By.XPATH,'//fieldset[3]/div[2]/div/div/div[2]/div/label/input').clear()
        #driver.find_element(By.XPATH,'//fieldset[3]/div[2]/div/div/div[2]/div/label/input').send_keys(dict['category'])  
        #商品説明
        set_attribute(driver,'//*[@id="textMode"]/div[2]/textarea','value',dict['description'])
        driver.find_element(By.XPATH,'//*[@id="textMode"]/div[2]/textarea').send_keys(' ')
        #状態
        sts = int(int(re.sub(r"\D","",dict['status']))/10)
        driver.find_element(By.XPATH,f'//fieldset[10]/div[2]/div/ul/li[{sts}]/div/label/span[2]').click()
        #消費税
        tax = 3
        driver.find_element(By.XPATH,f'//fieldset[11]/div[2]/div/ul/li[{tax}]/div/label/span[2]').click()
        #税込み=税抜きでやる 何もしないようにしてみる
        driver.find_element(By.XPATH,f'//fieldset[12]/div[2]/div/div/div[1]/div/label/input').click()
        #set_attribute(driver,'//fieldset[12]/div[2]/div/div/div[1]/div/label/input','value','1')
        #time.sleep(1)
        #開始価格
        #set_attribute(driver,'//fieldset[12]/div[2]/div/div/div[2]/div/div[2]/div/label/input','value',dict['start_price'])
        driver.find_element(By.XPATH,'//fieldset[12]/div[2]/div/div/div[2]/div/div[2]/div/label/input').clear()
        driver.find_element(By.XPATH,'//fieldset[12]/div[2]/div/div/div[2]/div/div[2]/div/label/input').send_keys(dict['start_price'])  
        #即決価格
        #set_attribute(driver,'//fieldset[12]/div[2]/div/div/div[3]/div/div[2]/div/label/input','value',dict['end_price'])
        driver.find_element(By.XPATH,'//fieldset[12]/div[2]/div/div/div[3]/div/div[2]/div/label/input').clear()
        driver.find_element(By.XPATH,'//fieldset[12]/div[2]/div/div/div[3]/div/div[2]/div/label/input').send_keys(dict['end_price'])  
        #個数
        set_attribute(driver,'//fieldset[13]/div[2]/div/div/div/label/input','value','1')
        #driver.find_element(By.XPATH,'//fieldset[13]/div[2]/div/div/div/label/input').clear()
        #driver.find_element(By.XPATH,'//fieldset[13]/div[2]/div/div/div/label/input').send_keys('1')  
        #開催期間
        day_period = dict['period']
        time_priod = 17
        driver.find_element(By.XPATH,f'//fieldset[14]/div[2]/div/div/div[1]/label/select/option[{day_period-1}]').click()
        driver.find_element(By.XPATH,f'//fieldset[14]/div[2]/div/div/div[2]/label/select/option[{time_priod}]').click()

        # 再出品ボタンをクリック(確認段階)
        #driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div/main/div/div[3]/ul/li[2]/button').click()

    except Exception as e:
        print("該当するオークションに問題があります")
        print(e)
        return False

    return True

def get_target_data(aucid):

    if not aucid:
        return ""

    DB_URL = os.environ['DB_URL']
    TMP_PATH = os.environ['TMP_PATH']

    Base = automap_base()
    engine = create_engine(DB_URL, echo=False)
    Base.prepare(engine,reflect=True)
    Exhibit = Base.classes.出品商品管理票
    session = Session(engine)

    q = session.query(Exhibit)\
        .filter(Exhibit.オークションID==aucid)\
        .order_by(Exhibit.管理番号.desc())\
        .first()

    #if not q == None:
    if q:
        dict = {
            "pname" : q.商品名,
            "title" : q.タイトル,
            "scode" : q.仕切書No,
            "maker" : q.メーカー,
            "model" : q.型式,
            "width" : str(q.梱包サイズ横),
            "long" : str(q.梱包サイズ縦),
            "height" : str(q.梱包サイズ高),
            "category" : q.カテゴリID,
            "period" : q.出品日数,
            "status" : q.商品状態,
            "start_price" : int(q.開始価格),
            "end_price" : int(q.即決価格),
            "shipping" : q.発送,
            "description" : q.出品詳細,
        }
        #print(dict)
        with open(TMP_PATH.format(dict['shipping']),'r') as f:
            tmp_str = f.read()
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

def quit():
    driver.quit()

if __name__ == '__main__':

    load_dotenv()
    hub_url = os.environ['HUB_URL']
    is_driver_quit = True

    dmode = "local" # "remote"

    if len(sys.argv) > 1 :
        aucid=sys.argv[1]
    else:
        print("パラメータエラー: IDを入力してください")
        sys.exit(0)
        
    dict = get_target_data(aucid)
    if dict:
        try:
            driver = init_driver(dmode)
            ypro_login(driver)
            if re_exbt(driver,aucid,dict) == True:
                print("当該オークションの値をセットできました。\n再出品処理を行ってください。")

            #sys.exit(0)

            input("なにかキーを入力するか、ctrl-Cで処理を終了してください")


        except KeyboardInterrupt:
            print("ctrl-Cが入力されました。")
        except  Exception as e:
            print("例外が発生しました")
            print(e)
        finally:
            print("処理を終了してます。しばらくお待ちを・・・")
            if is_driver_quit :
                print("ドライバーを終了します")
                driver.quit()
            print("・・・・終了しますた!!")
    else:
        print("該当するオークションはありません")