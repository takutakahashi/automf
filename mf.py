# coding: UTF-8
import sys
import os
import utils
import store
import parser

if __name__ == '__main__':
    args = parser.get_args()
    cls = args.func
    must_reload = []
    user = os.environ["MF_ID"]
    password = os.environ["MF_PASSWORD"]
    driver = utils.login(user, password,
            force_reload=(cls in must_reload))
    utils.set_group(driver, args.group)
    result = getattr(utils, cls)(driver, args)
    driver.quit()
    store.persist(result, cls)
    sys.exit()
