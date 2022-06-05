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
import datetime
import shutil


from webdriver_manager.chrome import ChromeDriverManager

def php_login(driver):

    load_dotenv()
    login_id = os.environ['PHPMYADMIN_USER']
    login_password = os.environ['PHPMYADMIN_PASSWORD']
    phpMyAdmin_server = os.environ['PHPMYADMIN_SERVER']
    phpMyAdmin_url = os.environ['PHPMYADMIN_URL']

    print("try login.....")
    try:
        driver.get(phpMyAdmin_url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, 'pma_username')))
        search_box = driver.find_element_by_name("pma_servername")
        search_box.send_keys(phpMyAdmin_server)
        search_box = driver.find_element_by_name("pma_username")
        search_box.send_keys(login_id)
        search_box = driver.find_element_by_name("pma_password")
        search_box.send_keys(login_password)
        driver.find_element_by_id("input_go").click()
        print("OK log in!")
    except Exception as e:
        print(e)
        driver.quit()
        sys.exit()

def download_db(driver):

    load_dotenv()
    phpmyadmin_url = os.environ['PHPMYADMIN_URL']
    download_dir = os.environ['DOWNLOAD_DIR']
    db_filename = os.environ['DB_FILENAME']
    data_dir = os.environ['DATA_DIR']
    backup_dir = os.environ['BACKUP_DIR']
    download_tinmeout = int(os.environ['DOWNLOAD_TIMEOUT'])

    driver.get(f'{phpmyadmin_url}/index.php?route=/server/export')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'buttonGo')))
    driver.find_element_by_id('buttonGo').click()

    file_path = os.path.join(download_dir, db_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    for i in range(download_tinmeout):
        if os.path.isfile(file_path):
            break
        time.sleep(1)
    else:
        print("Time out wating for download...")
        sys.exit(-1)

    # save to ./data
    save_filename = datetime.datetime.now().strftime('%y%m%d')+'_'+db_filename
    os.makedirs(backup_dir, exist_ok=True)
    save_path = os.path.join(backup_dir, save_filename)
    shutil.copy(file_path, save_path)

if __name__ == '__main__':

    load_dotenv()
    hub_url = os.environ['HUB_URL_TEST']

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #driver = webdriver.Remote(
    #    command_executor=hub_url,
    #    desired_capabilities=options.to_capabilities(),
    #    options=options,
    #)

    php_login(driver)
    download_db(driver)

    driver.quit()


