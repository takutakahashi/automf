# coding: UTF-8
import sys
import os
import utils
import store

if __name__ == '__main__':
    cls = sys.argv[1]
    args = sys.argv[2:]
    must_reload = ["balance"]
    user = os.environ["MF_ID"]
    password = os.environ["MF_PASSWORD"]
    print("start login")
    driver = utils.login(user, password,
            force_reload=(cls in must_reload))
    print("login success")
    result = getattr(utils, cls)(driver, args=args)
    driver.quit()
    store.persist(result, cls)
    sys.exit()
