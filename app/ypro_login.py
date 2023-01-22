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

#-----ヤフオクを開く------
def ypro_login(driver):

    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url= os.environ['PRO_URL']


    print("try login.....")
    try:
        driver.get(pro_url)
        driver.implicitly_wait(10)
        # input user id
        time.sleep(2)  #やはりこれ入れないと駄目みたい
        for i in range(3):
            search_box = driver.find_element(By.ID,"username")           
        search_box.clear()
        search_box.send_keys(login_id)
            
        driver.find_element(By.ID,"btnNext").click()
        # input password
        search_box = driver.find_element(By.ID,"passwd")
        search_box.send_keys(login_password)
        driver.find_element(By.ID,"btnSubmit").click()
        print("OK log in!")
    except Exception as e:
        print(e)
        driver.quit()
        sys.exit()

if __name__ == '__main__':

    load_dotenv()
    hub_url = os.environ['HUB_URL']

    dmode = "local" 
    #dmode = "remote"

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
        input("Press any key.")
    except Exception as e:
        print("Any error")
        print(e)
    finally:
        print("Termination in process.......")
        driver.quit()
        print(".....Finished")


#------implicite　waitに変更したあと
       #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
       #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwd')))
 
