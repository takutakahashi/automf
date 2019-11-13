import os
import datetime

def persist(dct, cls):
    if dct is None:
        return
    try:
        os.makedirs("/mnt/{}".format(cls))
    except FileExistsError:
        pass
    with open("/mnt/{}/{}.txt".format(cls, datetime.datetime.now().strftime('%Y%m%d')), 'w') as f:
        f.write(str(dct))
