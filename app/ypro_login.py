import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle
from selenium.webdriver.chrome.options import Options

#-----open target url ------
def init_driver(mode=''):

    load_dotenv()
    hub_url = os.environ['HUB_URL']
    if not mode: 
        run_mode = os.environ['RUN_MODE']
    else:
        run_mode = mode

    options = webdriver.ChromeOptions()
    #dc = DesiredCapabilities.CHROME.copy() #Cert エラー回避のため、でも効かないみたいなぜか？
    #dc['acceptSslCerts'] = True
    #dc['acceptInsecureCerts'] = True
    options.set_capability('acceptInsecureCerts', True)


    if run_mode== "remote":
        driver = webdriver.Remote(
            command_executor=hub_url,
            #desired_capabilities=options.to_capabilities(),
            #desired_capabilities=dc,se
            options=options,
        )
    else:
        try:
            #driver = webdriver.Chrome(ChromeDriverManager().install(),options=options,desired_capabilities=dc)
            driver = webdriver.Chrome(options=options)

        except Exception as e:
            print(f"ドライバーの初期化中にエラーが発生しました: {e}")
            sys.exit(1)

    return driver

def ypro_login_pickle(driver):
    load_dotenv()
    pro_url= os.environ['PRO_URL']
    run_mode = os.environ['RUN_MODE']
    target_domain = [".yahoo.co.jp"]
    expect_str = "ストアクリエイター"
    
    driver.get(pro_url)
    try:
        pkl_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),f"cookies_{run_mode}.pkl")
        print("pkl_file:",pkl_filepath)
        cookies = pickle.load(open(pkl_filepath,"rb"))
    except Exception as e:
        print("in ",e)
        return False
    for cookie in cookies:
        #print(cookie)
        if cookie['domain'] in target_domain:
            driver.add_cookie(cookie)

    driver.get(pro_url)
    print("PRO URL:",pro_url)
    #print(driver.find_element(By.XPATH,'//*[@id="ygmhlog"]').get_attribute("alt"))
    try:
        if expect_str in driver.find_element(By.XPATH,'//*[@id="ygmhlog"]').get_attribute("alt"):
            return True
        else:
            return False
    except Exception as e:
        print("ypro_login_pickle.....: ",e)
        return False

def ypro_login(driver):

    load_dotenv()
    login_id = os.environ['YLOGINID']
    login_password = os.environ['YPASSWORD']
    pro_url = os.environ['PRO_URL']
    is_pkl = os.environ['IS_PKL']

    driver.implicitly_wait(20)

    if is_pkl == "TRUE":
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

    args = sys.argv
    if len(args) >1 :
        if args[1] == 'remote':
            run_mode = 'remote'
        else:
            run_mode = 'local'

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
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains

       #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
       #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwd')))
 
