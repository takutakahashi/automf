# coding: UTF-8
from selenium import webdriver
from time import sleep

def login(user, password):
  surl = "https://moneyforward.com/users/sign_in"

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
    sleep(3)
  except ValueError:
      return None
  return driver

def balance(driver):
  account_dict = {}
  try:
    driver.get("https://moneyforward.com/accounts")
    for t in driver.find_elements_by_id("registration-table"):
        cls = t.get_attribute("class")
        if cls == "real-estate-property-accounts":
            break
        elif cls == "manual_accounts":
            path = "/accounts/show_manual"
        else:
            path = "/accounts/show"
        for tr in t.find_elements_by_tag_name("tr"):
            account_id = tr.get_attribute("id")
            if len(account_id) != 0:
              name = tr.find_element_by_xpath("//a[@href='{}/{}']".format(path, account_id)).text
              num = tr.find_element_by_class_name("number").text
              if len(num) == 0:
                  num = '0円'
              account_dict[name] = int(num.replace("円", "").replace(",", ""))
  except ValueError:
      return None
  return account_dict
