import csv
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains
#from bs4 import BeautifulSoup as bs4
#import pandas as pd
import sys
#import re
#import datetime
#import datetime
#import shutil
import prefect
from prefect import task, Flow
from prefect.run_configs import LocalRun

dir_name = os.path.dirname(os.path.abspath(__file__))
#print("dir_name:",dir_name)

#sys.path.append(dir_name)
from phpmyadmin import php_login,download_db
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
def t_pma_login():

    logger = prefect.context.get("logger")
    driver = init_driver()
    php_login(driver)
    logger.info("phpMyAdmin_login!")

    #download_order(driver)
    return driver

@task
def t_download_db(driver):
    download_db(driver)
    return driver

@task
def t_driver_end(driver):
    driver.quit()
    return True

with Flow("db-backup",run_config=LocalRun(working_dir=dir_name)) as flow:
    #init_driver()
    driver1 = t_pma_login()
    driver2 = t_download_db(driver1)
    ext_end = t_driver_end(driver2)

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
