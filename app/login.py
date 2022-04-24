import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import sys

#-----ヤフオクを開く------
def ypro_login(driver):

    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url= os.environ['PRO_URL']


    print("try login.....")
    try:
        driver.get(pro_url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'username')))
        search_box = driver.find_element_by_id("username")
        search_box.send_keys(login_id)
        driver.find_element_by_id("btnNext").click()
        time.sleep(1) #なぜかしら必要。waitのタイミング？
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'passwd')))
        search_box = driver.find_element_by_id("passwd")
        search_box.send_keys(login_password)
        driver.find_element_by_id("btnSubmit").click()
        print("OK log in!")
    except Exception as e:
        print(e)
        driver.quit()
        sys.exit()

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
