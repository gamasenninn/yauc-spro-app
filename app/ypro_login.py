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
from webdriver_manager.chrome import ChromeDriverManager

#def set_attribute(driver,xpath,attribute,value):
#    elm = driver.find_element(By.XPATH,xpath)
#    driver.execute_script(f"arguments[0].value = arguments[1];", elm,value)

#-----ヤフオクを開く------
def ypro_login(driver):

    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url= os.environ['PRO_URL']


    print("try login.....")
    try:
        driver.get(pro_url)
        time.sleep(2) #なぜかしら必要。waitのタイミング？
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        search_box = driver.find_element(By.ID,"username")
        search_box.clear()
        search_box.send_keys(login_id)
        #driver.execute_script(f"arguments[0] = arguments[1];", search_box,login_id)        
        driver.find_element(By.ID,"btnNext").click()
        time.sleep(1) #なぜかしら必要。waitのタイミング？
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwd')))
        search_box = driver.find_element(By.ID,"passwd")
        search_box.send_keys(login_password)
        #driver.execute_script(f"arguments[0] = arguments[1];", search_box,login_password)        
        driver.find_element(By.ID,"btnSubmit").click()
        print("OK log in!")
    except Exception as e:
        print(e)
        driver.quit()
        sys.exit()

def ypro_login_new(driver):

    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url= os.environ['PRO_URL']


    print("try login.....")
    try:
        driver.get(pro_url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'username')))
        search_box = driver.find_element(By.ID,"username")
        #search_box.send_keys(login_id)
        driver.execute_script(f"arguments[0] = arguments[1];", search_box,login_id)        
        '''
        driver.find_element(By.ID,"btnNext").click()
        time.sleep(1) #なぜかしら必要。waitのタイミング？
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'passwd')))
        search_box = driver.find_element(By.ID,"passwd")
        search_box.send_keys(login_password)
        #driver.execute_script(f"arguments[0] = arguments[1];", search_box,login_password)        
        driver.find_element(By.ID,"btnSubmit").click()
        print("OK log in!")
        '''
    except Exception as e:
        print(e)
        driver.quit()
        sys.exit()

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

    try:
        ypro_login(driver)
        input("なにかキーをおしてください")
    except Exception as e:
        print("error")
        print(e)
    finally:
        print("終了処理中")
        driver.quit()
        print("終了しました。")