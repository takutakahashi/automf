# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import re
import os

def to_sub(s):
    return re.match("[-\d,.]+",s).group()

def to_yen(s):
    return int(to_sub(s).replace(",", ""))

def to_f(s):
    return float(to_sub(s))

def test(driver, args):
    return _portfolio(driver, "q8yTAb5dxyTJmbnyWqri3Q")

def login(user, password, force_reload=False):
  surl = "https://moneyforward.com/sign_in"

  try:
    options = Options()
    if not os.environ.get("DISABLE_HEADLESS"):
      options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.implicitly_wait(10)
    driver.get(surl)
  
    # login
    elem = driver.find_element_by_css_selector(".ssoText")
    elem.click()
    elem = driver.find_element_by_css_selector(".inputItem")
    elem.clear()
    elem.send_keys(user)
    debug("email sent")
    elem = driver.find_element_by_css_selector(".submitBtn.homeDomain")
    elem.click()
    elem = driver.find_element_by_css_selector(".inputItem")
    debug("password sent")
    elem.clear()
    elem.send_keys(password)
    elem = driver.find_element_by_css_selector(".submitBtn.homeDomain")
    elem.click()
    sleep(3)
    debug("login successful")
    if force_reload:
      reload(driver)
  except ValueError:
      return None
  return driver

def set_group(driver, group=None):
    if not group:
        return
    driver.get("https://moneyforward.com/")
    s = driver.find_element_by_id("group_id_hash")
    s.click()
    [o for o in s.find_elements_by_tag_name("option") if group == o.text].pop().click()
    return

def reload(driver, args=None):
    driver.get("https://moneyforward.com/")
    for e in driver.find_elements_by_css_selector(".refresh.btn.icon-refresh"):
        if e.text == "一括更新":
            e.click()
            debug("reload clicked")
    return


def _portfolio(driver, account_id):
    driver.get("https://moneyforward.com/accounts/show/{}".format(account_id))
    portfolio_section = driver.find_element_by_id("portfolio_det_mf")

    theader = portfolio_section.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
    tbody = portfolio_section.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    header = [t.text for t in theader]
    return [ { header[i]: content.text for i, content in enumerate(t.find_elements_by_tag_name("td"))} for t in tbody]

def _detail(driver, account_name):
  driver.get("https://moneyforward.com/")
  l = driver.find_elements_by_css_selector(".facilities.accounts-list")[0]
  for li in l.find_elements_by_tag_name('li'):
      if li.get_attribute("class") == "account facilities-column border-bottom-dotted" and li.find_element_by_tag_name("a").text == account_name:
          show_href = li.find_elements_by_tag_name("a")[0].get_attribute("href")
          return show_href

def clean(driver, args):
    member = args.member
    amount_delta = args.amount
    if None in [member, amount_delta]:
        return False
    driver.get(_detail(driver, member))
    [b for b in driver.find_elements_by_css_selector(".btn.btn-success") if b.text == "残高修正"].pop().click()
    sleep(2)
    a_str = driver.find_element_by_css_selector("span.control-label").text[:-1]
    before_amount = int(a_str)
    if before_amount >= 0:
        amount = before_amount - int(amount_delta)
    else:
        amount = before_amount + int(amount_delta)
    driver.find_element_by_id("rollover_info_value").send_keys(amount)
    c = driver.find_element_by_id("rollover_info_transaction_flag")
    if c.is_selected():
        c.click()
    [b for b in driver.find_elements_by_name("commit") if b.get_attribute("value") == "この内容で登録する"].pop().click()
    return {"before": before_amount, "after": amount}

def balance(driver, args=None):
    return _balance(driver, args, 0) + _balance(driver, args, 1)

def wallets(driver, args=None):
    return _balance(driver, args, 0)


def _balance(driver, args=None, index=1):
  account_list = []
  delimiter = ["/show_manual/", "/show/"]
  debug("start getting balance")
  try:
    driver.get("https://moneyforward.com/")
    account_type = ""
    debug("fetch account list")
    l = driver.find_elements_by_css_selector(".facilities.accounts-list")[index]
    for li in l.find_elements_by_tag_name('li'):
        if li.get_attribute("class") == "heading-category-name heading-normal":
            account_type = li.text
        elif li.get_attribute("class") == "account facilities-column border-bottom-dotted":
            account_name = li.find_element_by_tag_name("a").text
            show_href = li.find_elements_by_tag_name("a")[0].get_attribute("href")
            account_id = show_href.split(delimiter[index])[1]
            if account_type == "カード":
                amount = show_href
            else:
                amount = li.find_element_by_class_name("number").text
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
              a["amount"] = int(h1s[0].text.split(" ")[1].replace(",","").replace("円", ""))
              continue
          a["amount"] = int(driver.find_element_by_id("TABLE_3").find_element_by_class_name("number").text.replace(",","").replace("円", ""))
      else:
          a["amount"] = int(a["amount"].replace(",","").replace("円", ""))

  return account_list

def investments(driver, args=None):
    account_list = []
    try:
      driver.get("https://moneyforward.com/")
      account_type = ""
      l = driver.find_elements_by_css_selector(".facilities.accounts-list")[1]
      for li in l.find_elements_by_tag_name('li'):
          if li.get_attribute("class") == "heading-category-name heading-normal":
              account_type = li.text
          elif li.get_attribute("class") == "account facilities-column border-bottom-dotted":
              if account_type != "証券":
                  continue
              account_name = li.find_element_by_tag_name("a").text
              show_href = li.find_elements_by_tag_name("a")[0].get_attribute("href")
              account_id = show_href.split("/show/")[1]
              amount = li.find_element_by_class_name("number").text
              _dict = {
                      "account_id": account_id,
                      "name": account_name,
                      "type": account_type,
                      "amount": amount
                      }
              account_list.append(_dict)
    except ValueError:
        return None
    result_list = []
    for a in account_list:
        a["details"] = []
        driver.get("https://moneyforward.com/accounts/show/{}".format(a["account_id"]))
        # cash table
        cash_table = driver.find_element_by_id("portfolio_det_depo")
        body = cash_table.find_element_by_tag_name("tbody")
        for tr in body.find_elements_by_tag_name("tr"):
            tds = tr.find_elements_by_tag_name("td")
            result_list.append({
                    "account_id": a["account_id"],
                    "name": a["name"],
                    "type": tds[0].text,
                    "profit": 0,
                    "amount": to_yen(tds[1].text),
                    })
        # // cash teble
        # // investment table
        cash_table = driver.find_element_by_id("portfolio_det_eq")
        body = cash_table.find_element_by_tag_name("tbody")
        for tr in body.find_elements_by_tag_name("tr"):
            tds = tr.find_elements_by_tag_name("td")
            result_list.append({
                    "account_id": a["account_id"],
                    "name": a["name"],
                    "type": tds[0].text,
                    "profit": to_yen(tds[7].text),
                    "amount": to_yen(tds[5].text),
                    })
        # // investment table
    return result_list

def add(driver, args):
    add_type = args.add_type
    member = args.member
    item = args.item
    amount = args.amount
    comment = args.comment
    debug("start add")
    if None in [add_type, member, item, amount]:
        return False
    if comment == None:
        comment = ""
    category_type = {
            "expense": ".dropdown-menu.main_menu.minus",
            "income": ".dropdown-menu.main_menu.plus"
            }[add_type]
    add_type = {"expense": "important", "income": "info"}[add_type]
    debug("add_type: {}".format(add_type))
    large_item, middle_item = item.split("/")
    debug("load cf")
    driver.get("https://moneyforward.com/cf")
    debug("loaded")
    driver.find_element_by_css_selector(".cf-new-btn.btn.modal-switch.btn-warning").click()
    debug("create button pressed")
    sleep(1)
    driver.find_element_by_class_name("tab-menu").find_element_by_id(add_type).click()
    debug("tab pressed")
    driver.find_element_by_id("appendedPrependedInput").send_keys(amount)
    debug("ammount sent")
    s = driver.find_element_by_id("user_asset_act_sub_account_id_hash")
    s.click()
    [opt for opt in s.find_elements_by_tag_name("option") if member in opt.text].pop().click()
    driver.find_element_by_id("js-large-category-selected").click()
    li = driver.find_element_by_css_selector(category_type)
    [a for a in li.find_elements_by_class_name("l_c_name") if a.text == large_item].pop().click()
    driver.find_element_by_id("js-middle-category-selected").click()
    li = driver.find_element_by_css_selector(".dropdown-menu.sub_menu")
    [a for a in li.find_elements_by_class_name("m_c_name") if a.text == middle_item].pop().click()
    debug("category selected")
    driver.find_element_by_id("js-content-field").send_keys("[{}] {}".format(member, comment))
    debug("comment sent")
    driver.find_element_by_id("submit-button").click()
    debug("end")

def debug(s):
    if os.environ.get("DEBUG") == "true":
        print(s)
