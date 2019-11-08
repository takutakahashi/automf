def persist(dct, cls):
    if dct is None:
        return
    with open("/mnt/{}.txt".format(cls), 'a') as f:
        f.write(dct)
