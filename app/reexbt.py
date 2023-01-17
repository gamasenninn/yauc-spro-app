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

expect_path = '//*[@id="__next"]/div[1]/div/main/div/fieldset[1]/div[2]/div/div/label/input'
#ul_path = '//*[@id="__next"]/div[1]/div/main/div/div/div[3]/section/div/div[4]/div/div/ul'

aucid  = "s1064874767"

def ex_date(date_text):
    return date_text.strip().replace('年', '/').replace('月', '/').replace('日', '')

def set_attribute(driver,xpath,attribute,value):
    elm = driver.find_element_by_xpath(xpath)
    driver.execute_script(f"arguments[0].{attribute} = '{value}';", elm)


def re_exbt(driver):

    exbt_url = os.environ['RE_EXBT_URL']

    # -- exhbit lisr URL---
    driver.get(exbt_url+aucid)
    driver.implicitly_wait(30)

    driver.find_element_by_xpath(expect_path)
    soup = bs4(driver.page_source, 'html.parser')
    lx = html.fromstring(str(soup))
    global LXS
    LXS.append(lx)

    # タイトルへ値をセット
    title = driver.find_element_by_xpath('//fieldset[2]/div[2]/div/label/input')
    title_val = 'テストタイトル'
    driver.execute_script(f"arguments[0].value = '{title_val}';", title)
    #タイトル
    set_attribute(driver,'//fieldset[2]/div[2]/div/label/input','value','テストタイトル２')
    #カテゴリ
    set_attribute(driver,'//fieldset[3]/div[2]/div/div/div[2]/div/label/input','value','2084244314')
    #商品説明
    driver.find_element_by_xpath('//*[@id="textMode"]/div[2]/textarea').clear()
    driver.find_element_by_xpath('//*[@id="textMode"]/div[2]/textarea').send_keys("aaaaaaddddddddddd")
    #状態
    sts = 4
    driver.find_element_by_xpath(f'//fieldset[10]/div[2]/div/ul/li[{sts}]/div/label/span[2]').click()
    #消費税
    tax = 3
    driver.find_element_by_xpath(f'//fieldset[11]/div[2]/div/ul/li[{tax}]/div/label/span[2]').click()
    #税込み
    #tax_include = 1
    #tax_current = driver.find_element_by_xpath(f'//fieldset[12]/div[2]/div/div/div[1]/div/label/input').get_attribute('value')
    #if tax_include:
    #    if tax_current != '1':
    #        driver.find_element_by_xpath(f'//fieldset[12]/div[2]/div/div/div[1]/div/label').click()
    #else:
    #    if tax_current == '1':
    #        driver.find_element_by_xpath(f'//fieldset[12]/div[2]/div/div/div[1]/div/label').click()
    #開始価格
    set_attribute(driver,'//fieldset[12]/div[2]/div/div/div[2]/div/div[2]/div/label/input','value','12345')
    #即決価格
    set_attribute(driver,'//fieldset[12]/div[2]/div/div/div[3]/div/div[2]/div/label/input','value','12345')
    #個数
    set_attribute(driver,'//fieldset[13]/div[2]/div/div/div/label/input','value','1')
    #開催期間
    day_priod = 2
    time_priod = 17
    driver.find_element_by_xpath(f'//fieldset[14]/div[2]/div/div/div[1]/label/select/option[{day_priod-1}]').click()
    driver.find_element_by_xpath(f'//fieldset[14]/div[2]/div/div/div[2]/label/select/option[{time_priod}]').click()

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
    re_exbt(driver)

    #driver.quit()
    print("Complete!!")
