import csv
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
#import pandas as pd
import sys
#import re
#import datetime
import datetime
import shutil
import prefect
from prefect import task, Flow
from prefect.run_configs import LocalRun

dir_name = os.path.dirname(os.path.abspath(__file__))
#print("dir_name:",dir_name)

#sys.path.append(dir_name)
from ypro_login import ypro_login
from fee_list_before_month import fee_list_before_montth
from csv2gsp_feelist_before_month import csv2gsp_feelist_before_month
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

#g_driver = ''


def init_driver():
    load_dotenv()
    hub_url = os.environ['HUB_URL']

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=hub_url,
        desired_capabilities=options.to_capabilities(),
        options=options,
    )
    return driver

@task
def t_ylogin():

    logger = prefect.context.get("logger")
    driver = init_driver()
    ypro_login(driver)
    logger.info("ypro_login!")

    #download_order(driver)
    return driver

@task
def t_load_feelist_bm(driver):
    fee_list_before_montth(driver)
    return driver

@task
def t_trans_feelist_bm(driver):
    csv2gsp_feelist_before_month()
    return driver


@task
def t_final(driver):
    print('Task all end....!')
    driver.quit()
    return True


with Flow("ystore-monthly",run_config=LocalRun(working_dir=dir_name)) as flow:
    #init_driver()
    driver1 = t_ylogin()
    driver2 = t_load_feelist_bm(driver1)
    driver3  = t_trans_feelist_bm(driver2)
    final = t_final(driver3)

if __name__ == '__main__':

    args = sys.argv

    dir_name = os.path.dirname(os.path.abspath(__file__))
    print(dir_name)


    #flow.run_config = LocalRun(working_dir=dir_name)
    if len(args) >1 :
        if args[1] == 'reg':
            flow.register(project_name="test")
    else:
        flow.run()
    pass
#
#
# docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:4.1.3-20220405
# docker run -d -p 4444:4444 -p 7900:7900 -v C:/Users/user/Downloads:/home/seluser/Downloads --shm-size="2g" selenium/standalone-chrome:4.1.3-20220405
#
#
#
