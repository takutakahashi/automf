# coding: UTF-8
import sys
import os
import utils
import store
import parser

if __name__ == '__main__':
    args = parser.get_args()
    cls = args.func
    print(args.add_type)
    must_reload = ["balance"]
    user = os.environ["MF_ID"]
    password = os.environ["MF_PASSWORD"]
    print("start login")
    driver = utils.login(user, password,
            force_reload=(cls in must_reload))
    print("login success")
    utils.set_group(driver, args.group)
    result = getattr(utils, cls)(driver, args)
    driver.quit()
    store.persist(result, cls)
    sys.exit()
