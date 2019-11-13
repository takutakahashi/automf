import os
import datetime

def persist(dct, cls):
    if dct is None:
        return
    try:
        os.makedirs("/mnt/{}".format(cls))
    except FileExistsError:
        pass
    with open("/mnt/{}/{}.txt".format(cls, datetime.datetime.now().strftime('%Y%m%d%H%M')), 'a') as f:
        f.write(str(dct))
