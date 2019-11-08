# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

def login(user, password):
  surl = "https://moneyforward.com/users/sign_in"

  try:
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
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
    reload(driver)
  except ValueError:
      return None
  return driver

def reload(driver):
    driver.get("https://moneyforward.com/")
    for e in driver.find_elements_by_css_selector(".refresh.btn.icon-refresh"):
        if e.text == "一括更新":
            e.click()
    while True:
        length = len([l for l in driver.find_elements_by_tag_name("li") if l.text == "更新中"])
        if length == 0:
            break
        sleep(10)
    return


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

def b_list(driver):
  account_list = []
  try:
    driver.get("https://moneyforward.com/")
    account_type = ""
    l = driver.find_elements_by_css_selector(".facilities.accounts-list")[1]
    for li in l.find_elements_by_tag_name('li'):
        if li.get_attribute("class") == "heading-category-name heading-normal":
            account_type = li.text
        elif li.get_attribute("class") == "account facilities-column border-bottom-dotted":
            account_name = li.find_element_by_tag_name("a").text
            show_href = li.find_elements_by_tag_name("a")[0].get_attribute("href")
            account_id = show_href.split("/show/")[1]
            if account_type == "カード":
                amount = show_href
            else:
                amount = li.find_element_by_class_name("amount").find_element_by_class_name("number").text
            _dict = {
                    "account_id": account_id,
                    "name": account_name,
                    "type": account_type,
                    "amount": amount
                    }
            account_list.append(_dict)

  except ValueError:
      return None
  for a in account_list:
      if a["amount"][:4] == 'http':
          driver.get(a["amount"])
          h1s = [h for h in driver.find_elements_by_tag_name("h1") if h.text[:4] == "負債総額"]
          if len(h1s) == 1:
              a["amount"] = h1s[0].text.split(" ")[1]
              continue
          a["amount"] = driver.find_element_by_id("TABLE_3").find_element_by_class_name("number").text
  return account_list

