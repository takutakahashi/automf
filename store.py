import datetime
def persist(dct, cls):
    dct["created_at"] = str(datetime.datetime.now())
    with open("/mnt/{}.txt".format(cls), 'a') as f:
        f.write(dct)
