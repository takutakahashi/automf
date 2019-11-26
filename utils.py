# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

def login(user, password, force_reload=False):
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
    print("email sent")
    elem = driver.find_element_by_id("sign_in_session_service_password")
    print("assword sent")
    elem.clear()
    elem.send_keys(password)
    elem = driver.find_element_by_id("login-btn-sumit")
    elem.click()
    sleep(3)
    print("login successful")
    if force_reload:
      reload(driver)
  except ValueError:
      return None
  return driver

def set_group(driver, group):
    print("set {}".format(group))
    driver.get("https://moneyforward.com/")
    s = driver.find_element_by_id("group_id_hash")
    s.click()
    [o for o in s.find_elements_by_tag_name("option") if group == o.text].pop().click()
    return

def reload(driver):
    driver.get("https://moneyforward.com/")
    for e in driver.find_elements_by_css_selector(".refresh.btn.icon-refresh"):
        if e.text == "一括更新":
            e.click()
            print("reload clicked")
    while True:
        length = len([l for l in driver.find_elements_by_tag_name("li") if l.text == "更新中"])
        if length == 0:
            break
        print("sleep...")
        sleep(10)
    return

def balance(driver, args=None):
  account_list = []
  print("start getting balance")
  try:
    driver.get("https://moneyforward.com/")
    account_type = ""
    print("fetch account list")
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

def add(driver, args):
    add_type = args.add_type
    member = args.member
    item = args.item
    amount = args.amount
    comment = args.comment
    print("start add")
    if None in [add_type, member, item, amount]:
        return False
    if comment == None:
        comment = ""
    add_type = {"expense": "important", "income": "info"}[add_type]
    print("add_type: {}".format(add_type))
    large_item, middle_item = item.split("/")
    print("load cf")
    driver.get("https://moneyforward.com/cf")
    print("loaded")
    driver.find_element_by_css_selector(".cf-new-btn.btn.modal-switch.btn-warning").click()
    print("create button pressed")
    sleep(1)
    driver.find_element_by_class_name("tab-menu").find_element_by_id(add_type).click()
    print("tab pressed")
    driver.find_element_by_id("appendedPrependedInput").send_keys(amount)
    print("ammount sent")
    s = driver.find_element_by_id("user_asset_act_sub_account_id_hash")
    s.click()
    [opt for opt in s.find_elements_by_tag_name("option") if member in opt.text].pop().click()
    driver.find_element_by_id("js-large-category-selected").click()
    li = driver.find_element_by_css_selector(".dropdown-menu.main_menu.minus")
    [a for a in li.find_elements_by_class_name("l_c_name") if a.text == large_item].pop().click()
    driver.find_element_by_id("js-middle-category-selected").click()
    li = driver.find_element_by_css_selector(".dropdown-menu.sub_menu")
    [a for a in li.find_elements_by_class_name("m_c_name") if a.text == middle_item].pop().click()
    print("category selected")
    driver.find_element_by_id("js-content-field").send_keys("[{}] {}".format(member, comment))
    print("comment sent")
    driver.find_element_by_id("submit-button").click()
    print("end")
