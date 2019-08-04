# coding: UTF-8
import sys
import os
from time import sleep
import utils

class M():
  def balance(driver):
    print(utils.balance(driver))
    driver.get("https://moneyforward.com/cf/csv?year=2019&month=06")
    sleep(10)
    driver.quit()
    return 1

if __name__ == '__main__':
    cls = sys.argv[1]
    print(cls)
    user = os.environ["MF_ID"]
    password = os.environ["MF_PASSWORD"]
    driver = utils.login(user, password)
    sys.exit(getattr(M, cls)(driver))
