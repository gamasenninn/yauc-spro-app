import pytest
import sys
import os
from dotenv import load_dotenv

if True:  # 自動成形で順番が変えられないようにダミー処理
    sys.path.append("../app")
    from reexbt import get_target_data,re_exbt
    from ypro_login import ypro_login,init_driver

def test_get_target_ok():
    load_dotenv()
    aucid  =os.environ['TEST_AUCID']
    expect_title = 'こまめ'
    data_dict = get_target_data(aucid)
    print (data_dict)
    assert expect_title in data_dict['title']

def test_get_target_invalid():
    load_dotenv()
    aucid  ='99999999'
    data_dict = get_target_data(aucid)
    assert not data_dict

def test_re_exbt():
    load_dotenv()
    aucid  =os.environ['TEST_AUCID']
    expect_title = 'こまめ'
    data_dict = get_target_data(aucid)
    assert expect_title in data_dict['title']
    driver = init_driver('local')
    ypro_login(driver)
    assert re_exbt(driver,aucid,data_dict)
    driver.quit()
