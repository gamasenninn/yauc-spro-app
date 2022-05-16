import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs4
#import pandas as pd
#import sys
#import re
#import datetime
from ypro_login import ypro_login
import datetime
import shutil


def download_order(driver):

    pro_url = os.environ['PRO_URL']
    download_dir = os.environ['DOWNLOAD_DIR']
    order_filename = os.environ['ORDER_FILENAME']
    data_dir = os.environ['DATA_DIR']
    download_tinmeout = int(os.environ['DOWNLOAD_TIMEOUT'])

    # -- jump search page  ---
    url = f'{pro_url}/order/manage/index'
    driver.get(url)

    start_day = driver.find_element_by_id("OrderTimeFromDayE")
    start_day.send_keys(Keys.CONTROL+ "a")
    start_day.send_keys("2022/03/01")

    btns = driver.find_elements_by_class_name("btnBlL")
    btns[1].find_element_by_tag_name('a').click()

    # remove down load file
    file_path = os.path.join(download_dir, order_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # download
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'ycWrContentsFix')))
    link = driver.find_element_by_class_name("fileNum")
    link.find_element_by_tag_name('a').click()

    is_not_timeout = True
    for i in range(download_tinmeout):
        if os.path.isfile(file_path):
            break
        time.sleep(1)
    else:
        print("Time out wating for download...")
        return False

    # save to ./data
    save_filename = datetime.datetime.now().strftime('%y%m%d')+'_'+order_filename
    os.makedirs(data_dir, exist_ok=True)
    save_path = os.path.join(data_dir, save_filename)
    shutil.copy(file_path, save_path)

    print("file save OK!!")
    return True


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
    download_order(driver)

    driver.quit()

#
#
# docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:4.1.3-20220405
# docker run -d -p 4444:4444 -p 7900:7900 -v C:/Users/user/Downloads:/home/seluser/Downloads --shm-size="2g" selenium/standalone-chrome:4.1.3-20220405
#
#
#
