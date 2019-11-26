import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('func', help="set function name you want to execute", choices=['add', 'balance'])
    parser.add_argument("--group", "-g", help="moneyforward group", required=True)
    parser.add_argument("--add_type", choices=['income', 'expense'])
    parser.add_argument("--member")
    parser.add_argument("--item")
    parser.add_argument("--amount")
    parser.add_argument("--comment")
    args = parser.parse_args()
    return args

