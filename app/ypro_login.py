import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle

#-----ヤフオクを開く------
def init_driver(mode=''):

    load_dotenv()
    hub_url = os.environ['HUB_URL']
    if not mode: 
        run_mode = os.environ['RUN_MODE']
    else:
        run_mode = mode

    options = webdriver.ChromeOptions()
    dc = DesiredCapabilities.CHROME.copy() #Cert エラー回避のため、でも効かないみたいなぜか？
    #dc['acceptSslCerts'] = True
    dc['acceptInsecureCerts'] = True

    if run_mode== "remote":
        driver = webdriver.Remote(
            command_executor=hub_url,
            desired_capabilities=options.to_capabilities(),
            #desired_capabilities=dc,se
            options=options,
        )
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options,desired_capabilities=dc)

    return driver

def ypro_login_pickle(driver):
    load_dotenv()
    pro_url= os.environ['PRO_URL']
    run_mode = os.environ['RUN_MODE']
    
    driver.get(pro_url)
    try:
        cookies = pickle.load(open(f"cookies_{run_mode}.pkl","rb"))
    except Exception as e:
        print(e)
        return False
    for cookie in cookies:
        if cookie['domain'] == ".yahoo.co.jp":
            driver.add_cookie(cookie)
            #print("cookie")

    driver.get(pro_url)
    print(driver.find_element(By.XPATH,'//*[@id="ygmhlog"]').get_attribute("alt"))
    try:
        if "ストアクリエイター" in driver.find_element(By.XPATH,'//*[@id="ygmhlog"]').get_attribute("alt"):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def ypro_login(driver):

    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url= os.environ['PRO_URL']

    driver.implicitly_wait(10)

    print("try login via pickle.....")
    if ypro_login_pickle(driver):
        return True

    print("try login.....")
    try:
        # input user id
        for i in range(3):
            driver.get(pro_url)
            time.sleep(3)  #やはりこれ入れないと駄目みたい
            try:
                search_box = driver.find_element(By.ID,"login_handle")           
                search_box.clear()
                search_box.send_keys(login_id)
            except Exception as e:
                print(e)
                time.sleep(1)
                print("error retry")
            else:
                break
        #time.sleep(30)            
        driver.find_element(By.XPATH,'//*[@id="content"]/div[1]/div/form/div[1]/div[1]/div[2]/div/button').click()        
        # input password
        search_box = driver.find_element(By.ID,"password")
        search_box.send_keys(login_password)
        #time.sleep(10)
        driver.find_element(By.XPATH,'//*[@id="content"]/div[1]/div/form/div[2]/div/div[1]/div[2]/div[3]/button').click()
        print("OK log in!")

        return True
        

    except Exception as e:
        print(e)
        driver.quit()
        sys.exit()

if __name__ == '__main__':
    load_dotenv()
    run_mode = os.environ['RUN_MODE']
    #run_mode = "local"

    try:
        driver = init_driver(run_mode)
        ypro_login(driver)
        while(1):
            cmd_str = input("command q=exit>> ")
            if not cmd_str:
                continue             
            cmds = cmd_str.split()
            if "send_keys" in cmds[0]:
                # 認証入力対応
                driver.find_element(By.ID,"inputText").send_keys(cmds[1])
            if "pickle_dump" in cmds[0]:
                pickle.dump(driver.get_cookies() , open(f"cookies_{run_mode}.pkl","wb"))
            if "q" in cmds[0]:
                break

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
 
