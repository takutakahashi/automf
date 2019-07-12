# coding: UTF-8
import sys
import os
from selenium import webdriver

def do():

  surl = "https://moneyforward.com/users/sign_in"
  user = os.environ["MF_ID"]
  password = os.environ["MF_PASSWORD"]

  try:
    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(10)
    driver.get(surl)
  
    # login
    elem = driver.find_element_by_id("sign_in_session_service_email")
    elem.clear()
    elem.send_keys(user)
    elem = driver.find_element_by_id("sign_in_session_service_password")
    elem.clear()
    elem.send_keys(password)
    elem = driver.find_element_by_id("login-btn-sumit")
    elem.click()
  
    driver.quit()

  except ValueError:
    print("Oops! Some Error are occured.")

  return 1 

if __name__ == '__main__':
  sys.exit(do())
