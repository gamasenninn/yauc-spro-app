import pytest
import sys
if True:  # 自動成形で順番が変えられないようにダミー処理
    sys.path.append("../app")
    from ypro_login import ypro_login,init_driver

def test_ypro_login_local():
    driver = init_driver('local')
    assert ypro_login(driver) == True
    driver.quit()

def test_ypro_login_remote():
    driver = init_driver('remote')
    assert ypro_login(driver) == True
    driver.quit()


