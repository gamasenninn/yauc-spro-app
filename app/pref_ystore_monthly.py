import os
from dotenv import load_dotenv
import sys
import prefect
from prefect import task, Flow
from prefect.run_configs import LocalRun

dir_name = os.path.dirname(os.path.abspath(__file__))

#sys.path.append(dir_name)
from ypro_login import ypro_login,init_driver
from fee_list_before_month import fee_list_before_montth
from csv2gsp_feelist_before_month import csv2gsp_feelist_before_month
from download_order import download_order


#os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
@task
def t_ylogin():

    logger = prefect.context.get("logger")
    driver = init_driver()
    ypro_login(driver)
    logger.info("ypro_login!")
    return driver
"""

@task
def t_download_order():
    logger = prefect.context.get("logger")
    driver = init_driver()
    ypro_login(driver)
    logger.info("ypro_login!")

    download_order(driver)

    driver.quit()
    return True

@task
def t_load_feelist_bm(t):
    logger = prefect.context.get("logger")
    driver = init_driver()
    ypro_login(driver)
    logger.info("ypro_login!")

    fee_list_before_montth(driver)

    driver.quit()    
    return True

@task
def t_trans_feelist_bm(t):
    csv2gsp_feelist_before_month()
    return True

@task
def t_final(t):
    print('Task all end....!')
    #driver.quit()
    return True


with Flow("ystore-monthly",run_config=LocalRun(working_dir=dir_name)) as flow:
    #init_driver()
    #driver1 = t_ylogin()
    end_t_download_order = t_download_order()

    end_t_load_feelist_bm = t_load_feelist_bm(end_t_download_order)
    end_t_trans_feelist_bm  = t_trans_feelist_bm(end_t_load_feelist_bm)
    final = t_final(end_t_trans_feelist_bm)

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
