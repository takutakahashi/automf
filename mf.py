# coding: UTF-8
import sys
import os
import utils
import store

if __name__ == '__main__':
    cls = sys.argv[1]
    user = os.environ["MF_ID"]
    password = os.environ["MF_PASSWORD"]
    driver = utils.login(user, password)
    result = getattr(utils, cls)(driver)
    driver.quit()
    store.persist(result, cls)
    sys.exit()
