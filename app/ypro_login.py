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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#-----ヤフオクを開く------
def ypro_login_test(driver):
    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url= os.environ['PRO_URL']

    print("try login.....")
    driver.get(pro_url)



def ypro_login(driver):

    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url= os.environ['PRO_URL']

    driver.implicitly_wait(10)

    print("try login.....")
    try:
        # input user id
        for i in range(3):
            driver.get(pro_url)
            time.sleep(3)  #やはりこれ入れないと駄目みたい
            try:
                search_box = driver.find_element(By.ID,"username")           
                search_box.clear()
                search_box.send_keys(login_id)
            except Exception as e:
                print(e)
                time.sleep(1)
                print("error retry")
            else:
                break
            
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
    dc = DesiredCapabilities.CHROME.copy() #Cert エラー回避のため、でも効かないみたいなぜか？
    dc['acceptSslCerts'] = True

    if dmode == "remote":
        driver = webdriver.Remote(
            command_executor=hub_url,
            #desired_capabilities=options.to_capabilities(),
            desired_capabilities=dc,
            options=options,
        )
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options,desired_capabilities=dc)

    try:
        ypro_login(driver)
        #ypro_login_test(driver)
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
 
