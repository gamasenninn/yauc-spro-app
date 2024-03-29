import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs4
import sys
import prefect
from prefect import task, Flow
from prefect.run_configs import LocalRun


dir_name = os.path.dirname(os.path.abspath(__file__))
#print("dir_name:",dir_name)

#sys.path.append(dir_name)
from ypro_login import ypro_login
from download_order import download_order
from fee_list import fee_list
from csv2db_order import csv2db_order
from csv2db_feelist import csv2db_feelist
from csv2gsp_feelist import csv2gsp_feelist
from csv2gsp_order import csv2gsp_order
from exbt_list import exbt_list
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_driver():
    load_dotenv()
    hub_url = os.environ['HUB_URL']
    run_mode = os.environ['RUN_MODE']

    options = webdriver.ChromeOptions()
    if run_mode == "remote":
        driver = webdriver.Remote(
            command_executor=hub_url,
            #desired_capabilities=options.to_capabilities(),
            #desired_capabilities=dc,
            options=options,
        )
    else:
        driver = webdriver.Chrome(options=options)

    return driver

@task
def t_download_order():
    logger = prefect.context.get("logger")
    driver = init_driver()
    ypro_login(driver)
    logger.info("ypro_login!")

    logger.info("download start.....")
    download_order(driver)
    logger.info(".....end download")
    driver.quit()

    return True

@task
def t_fee_list(t):
    logger = prefect.context.get("logger")
    driver = init_driver()
    ypro_login(driver)
    logger.info("ypro_login!")

    logger.info("fee_list start.....")
    fee_list(driver)
    logger.info(".....end fee_list")
    driver.quit()

    return True

@task
def t_exbt_list(t):
    logger = prefect.context.get("logger")
    driver = init_driver()
    ypro_login(driver)
    logger.info("ypro_login!")

    logger.info("exbt_list start.....")
    exbt_list(driver)
    logger.info(".....end exbt_list")
    driver.quit()

    return True

@task
def t_tran_order(t):
    csv2db_order()
    return True

@task
def t_tran_feelist(t):
    csv2db_feelist()
    return True

@task
def t_load_feelist(t):
    csv2gsp_feelist()
    csv2gsp_order()
    return True

@task
def t_final(t):
    print('Task all end....!')
    pass
    return True


with Flow("ystore-flow",run_config=LocalRun(working_dir=dir_name)) as flow:

    end_t_download_order = t_download_order()
    tran_end_1 = t_tran_order(end_t_download_order)
    end_t_fee_list = t_fee_list(end_t_download_order)
    end_t_exbt_list = t_exbt_list(end_t_fee_list)
    end_t_tran_feelist = t_tran_feelist(end_t_fee_list)
    end_t_load_feelist = t_load_feelist(end_t_tran_feelist)
    final = t_final([tran_end_1,end_t_exbt_list,end_t_load_feelist])

if __name__ == '__main__':

    args = sys.argv

    dir_name = os.path.dirname(os.path.abspath(__file__))
    print(dir_name)


    #flow.run_config = LocalRun(working_dir=dir_name)
    if len(args) >1 :
        if args[1] == 'reg':
            flow.register(project_name="hks")
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
