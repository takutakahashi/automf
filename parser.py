import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('func', help="set function name you want to execute", choices=['add', 'clean', 'balance', 'reload', 'wallets', 'investments', 'test'])
    parser.add_argument("--group", "-g", help="moneyforward group")
    parser.add_argument("--add_type", choices=['income', 'expense'])
    parser.add_argument("--member")
    parser.add_argument("--item")
    parser.add_argument("--amount")
    parser.add_argument("--comment")
    args = parser.parse_args()
    return args

def get_local_args(cls):
    return getattr("{}_args".format(cls))()
